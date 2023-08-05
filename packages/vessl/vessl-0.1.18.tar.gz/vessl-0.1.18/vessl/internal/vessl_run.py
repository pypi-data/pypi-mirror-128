import atexit
import os
import re
import signal
import sys
import threading
import time
from typing import Any, Dict, List, Optional

from urllib3.exceptions import MaxRetryError

from openapi_client.models.experiment_metric_entry import ExperimentMetricEntry
from openapi_client.models.experiment_metrics_update_api_payload import (
    ExperimentMetricsUpdateAPIPayload,
)
from openapi_client.models.experiment_progress_update_api_payload import (
    ExperimentProgressUpdateAPIPayload,
)
from openapi_client.models.local_experiment_finish_api_payload import (
    LocalExperimentFinishAPIPayload,
)
from openapi_client.models.response_experiment_info import ResponseExperimentInfo
from vessl.cli._util import Endpoint
from vessl.internal.collector import (
    Collector,
    IOCollector,
    SystemMetricCollector,
    UserMetricCollector,
)
from vessl.util import logger
from vessl.util.api import VesslApi
from vessl.util.constant import VESSL_IMAGE_PATH, VESSL_PLOTS_FILETYPE_IMAGE
from vessl.util.exception import InvalidExperimentError, VesslApiException
from vessl.util.image import Image

MODE_TEST = "TEST"
MODE_NOT_STARTED = "NOT_STARTED"
MODE_LOCAL = "LOCAL"
MODE_MANAGED = "MANAGED"

SEND_INTERVAL_IN_SEC = 10
PROGRESS_UPDATE_INTERVAL_IN_SEC = 1

METRIC_KEY_REGEX = re.compile("^[a-zA-Z0-9/_-]+$")


class Sender(object):
    def __init__(self, api: VesslApi, experiment_id: int, collectors: List[Collector]):
        self._api = api
        self._experiment_id: int = experiment_id
        self._thread = threading.Thread(target=self._thread_body, daemon=True)
        self._exit = threading.Event()
        self._collectors = collectors

    def stop(self):
        for c in self._collectors:
            c.stop()

        self._exit.set()
        self._thread.join()

    def start(self):
        for c in self._collectors:
            c.start()
        self._thread.start()

    def _thread_body(self):
        while not self._exit.is_set():
            self._send()
            self._exit.wait(timeout=SEND_INTERVAL_IN_SEC)
        self._send()

    def _send(self):
        pairs = [(c, c.collect()) for c in self._collectors]
        for c, m in pairs:
            logger.debug(f"{c} / {m}", str(c), len(m))
        payload = [m for _, metrics in pairs for m in metrics]
        logger.debug(f"Sending {len(payload)} payloads")

        try:
            res = self._api.experiment_metrics_update_api(
                self._experiment_id,
                experiment_metrics_update_api_payload=ExperimentMetricsUpdateAPIPayload(
                    metrics=payload
                ),
            )
            if res.rejected:
                logger.warning(f"{res.rejected} payloads(s) were rejected.")

            for c, m in pairs:
                c.truncate(len(m))

        except (MaxRetryError, VesslApiException) as e:
            logger.exception("Failed to send metrics to server", exc_info=e)
        except Exception as e:
            logger.exception("Unexpected error", exc_info=e)


class ProgressUpdater(object):
    def __init__(self, api: VesslApi, experiment_id: int):
        self._api = api
        self._experiment_id = experiment_id
        self._thread = threading.Thread(target=self._thread_body, daemon=True)
        self._exit = threading.Event()

        self._progress = None

    def start(self):
        self._thread.start()

    def stop(self):
        self._exit.set()
        self._thread.join()

    def update(self, value: float):
        self._progress = value

    def _thread_body(self):
        while not self._exit.is_set():
            self._send()
            self._exit.wait(timeout=PROGRESS_UPDATE_INTERVAL_IN_SEC)
        self._send()

    def _send(self):
        if self._progress is None:
            return

        logger.debug(f"Sending experiment progress: {self._progress}")
        try:
            self._api.experiment_progress_update_api(
                self._experiment_id,
                experiment_progress_update_api_payload=ExperimentProgressUpdateAPIPayload(
                    progress_percent=self._progress,
                ),
            )
            self._progress = None  # Flush after sending

        except (MaxRetryError, VesslApiException) as e:
            logger.exception("Failed to send metrics to server", exc_info=e)

        except Exception as e:
            logger.exception("Unexpected error", exc_info=e)


class VesslRun(object):
    class ExitHook(object):
        def __init__(self, orig_exit):
            self.orig_exit = orig_exit
            self.exit_code = 0

        def exit(self, code=0):
            self.exit_code = code
            self.orig_exit(code)

    __slots__ = [
        "api",
        "_mode",
        "_collectors",
        "_sender",
        "_progress_updater",
        "_experiment",
        "_logger",
        "_user_metric_collector",
        "_exit_hook",
    ]

    def __init__(self) -> None:
        self.api = VesslApi()
        self._experiment = self._get_experiment_from_environment()
        self._mode = MODE_NOT_STARTED if self._experiment is None else MODE_MANAGED

        self._user_metric_collector = UserMetricCollector()
        self._exit_hook = self.ExitHook(sys.exit)

    def _get_experiment_from_environment(self) -> Optional[ResponseExperimentInfo]:
        """Detect experiment from environment variables

        In a Vessl-managed experiment, these variables will be defined.
        """
        experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
        access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

        if experiment_id is None or access_token is None:
            return None

        self.api.configure_access_token(access_token)
        try:
            return self.api.experiment_read_by_idapi(experiment_id=experiment_id)
        except VesslApiException:
            return None

    def _get_experiment_from_args(
        self, experiment_name_or_number, message: str = None
    ) -> ResponseExperimentInfo:
        """Get or create a local experiment

        If experiment is specified, use it. Otherwise, create a new experiment.
        """
        # Create a new experiment
        if experiment_name_or_number is None:
            from vessl.experiment import create_local_experiment

            experiment = create_local_experiment(message=message)
            logger.debug(f"Created experiment {experiment.id}")
            return experiment

        # Continue with previous experiment
        from vessl.experiment import read_experiment

        experiment = read_experiment(experiment_name_or_number)
        if not experiment.is_local or experiment.local_execution_spec is None:
            raise InvalidExperimentError(
                f"{experiment.name}: cannot use Vessl-managed experiment."
            )
        if experiment.status != "running":
            raise InvalidExperimentError(
                f"{experiment.name}: experiment must be running."
            )

        return experiment

    def _signal_handler(self, signo, frames):
        sys.exit(130)  # job was terminated by the owner

    def _start(self):
        """Start sender and register hooks"""
        self._sender.start()

        sys.exit = self._exit_hook.exit
        atexit.register(self._stop)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _stop(self):
        """Stop sender and restore hooks"""
        if self._mode != MODE_LOCAL:
            return

        self._sender.stop()

        sys.exit = self._exit_hook.orig_exit
        self.api.local_experiment_finish_api(
            self._experiment.id,
            local_experiment_finish_api_payload=LocalExperimentFinishAPIPayload(
                exit_code=self._exit_hook.exit_code
            ),
        )

    def _send_without_collector(self, payloads):
        """Send metrics without using the collector

        In a Vessl-managed experiment, metrics are sent immediately instead of being queued.
        """
        assert self._mode == MODE_MANAGED
        res = self.api.experiment_metrics_update_api(
            self._experiment.id,
            experiment_metrics_update_api_payload=ExperimentMetricsUpdateAPIPayload(
                metrics=payloads
            ),
        )
        if res.rejected:
            logger.warning(f"{res.rejected} payloads(s) were rejected.")

    def init(self, experiment_name_or_number=None, message: str = None, is_test=False):
        """Main function to setup Vessl in a local setting

        If this is a Vessl-managed experiment or vessl.init has already been called,
        this will do nothing.

        Args:
            experiment_name_or_number (str | int): experiment name or number
            message (str): experiment message
            is_test (bool): internal use only
        """
        if self._mode != MODE_NOT_STARTED:
            return

        print(f"Initializing a new experiment...")
        self.api.configure()
        self._experiment = self._get_experiment_from_args(
            experiment_name_or_number, message
        )
        self._mode = MODE_LOCAL

        print(
            f"Connected to {self._experiment.name}.\n"
            f"For more info: {Endpoint.experiment.format(self._experiment.organization.name, self._experiment.project.name, self._experiment.number)}"
        )

        if is_test:
            return

        gpu_count = self._experiment.local_execution_spec.gpu_count or 0
        self._user_metric_collector = UserMetricCollector()
        collectors = [
            IOCollector(),
            SystemMetricCollector(gpu_count),
            self._user_metric_collector,
        ]
        self._sender = Sender(self.api, self._experiment.id, collectors)
        self._start()

    def upload(self, path: str):
        """Upload output files

        Args:
            path (str): path to upload
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        from vessl.experiment import upload_experiment_output_files

        upload_experiment_output_files(self._experiment.name, path)

    def finish(self):
        """Teardown Vessl settings

        Use this function to stop tracking your experiment mid-script. If not called,
        tracking is stopped automatically upon exit.

        Args:
            path (str): path to upload
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        if self._mode == MODE_MANAGED:
            return

        self._stop()
        experiment_name = self._experiment.name
        self._mode = MODE_NOT_STARTED
        self._experiment = None
        print(f"Experiment {experiment_name} completed.")

    def log(self, payload: Dict[str, Any], step: Optional[int] = None):
        """Log metrics to Vessl

        Args:
            payload (Dict[str, Any]): to log a scalar, value should be a number. To
                log an image, pass a single image or a list of images (type `vessl.util.image.Image`).
            step (int): step.
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        scalar_dict = {}
        image_dict = {}

        for k, v in payload.items():
            if isinstance(v, list) and all(isinstance(i, Image) for i in v):
                image_dict[k] = v
            elif isinstance(v, Image):
                image_dict[k] = [v]
            else:
                scalar_dict[k] = v

        # Update step if step is specified. If a scalar is defined but step wasn't,
        # step will be autoincremented.
        if scalar_dict or step is not None:
            self._user_metric_collector.handle_step(step)

        if image_dict:
            self._update_images(image_dict)

        if scalar_dict:
            self._update_metrics(scalar_dict)

    # This should mirror app/influx/metric_schema.go > `isValidMetricKey`
    def _is_metric_key_valid(self, key: str):
        if not METRIC_KEY_REGEX.match(key):
            return False
        if key.startswith("/") or key.endswith("/"):
            return False
        for i in range(1, len(key)):
            if key[i] == "/" and key[i - 1] == "/":
                return False
        return True

    def _update_metrics(self, payload: Dict[str, Any]):
        invalid_keys = [k for k in payload.keys() if not self._is_metric_key_valid(k)]
        if invalid_keys:
            logger.warning(
                f"Invalid metric keys: {' '.join(invalid_keys)}. This payload will be rejected."
            )

        payloads = [self._user_metric_collector.build_metric_payload(payload)]
        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
            return self._user_metric_collector.step
        return self._user_metric_collector.log_metrics(payloads)

    def _update_images(self, payload: Dict[str, List[Image]]):
        path_to_caption = {}
        for images in payload.values():
            for image in images:
                path_to_caption[image.path] = image.caption

        source_path = os.path.join(VESSL_IMAGE_PATH, "")
        assert self._experiment
        dest_volume_id = self._experiment.experiment_plot_volume
        dest_path = "/"

        from vessl.volume import copy_volume_file

        files = copy_volume_file(
            source_volume_id=None,
            source_path=source_path,
            dest_volume_id=dest_volume_id,
            dest_path=dest_path,
            recursive=True,
        )

        for images in payload.values():
            for image in images:
                image.flush()

        if files:
            plot_files = [
                {
                    "step": None,
                    "path": file.path,
                    "caption": path_to_caption[file.path],
                    "timestamp": time.time(),
                }
                for file in files
                if file.path in path_to_caption
            ]
        else:
            plot_files = []

        payloads: List[ExperimentMetricEntry] = []
        for f in plot_files:
            payload = {VESSL_PLOTS_FILETYPE_IMAGE: f}
            payloads.append(self._user_metric_collector.build_image_payload(payload))

        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
        else:
            self._user_metric_collector.log_images(payloads)

    def progress(self, value: float):
        """Update experiment progress

        Args:
            value (float): progress value as a decimal between 0 and 1
        """
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        if not 0 < value <= 1:
            logger.warning(f"Invalid progress value {value}. (0 < value <= 1)")
            return

        if not hasattr(self, "_progress_updater"):
            # Do not initialize in init() since ProgressUpdater might not be used at all
            self._progress_updater = ProgressUpdater(self.api, self._experiment.id)
            self._progress_updater.start()

        self._progress_updater.update(value)
        logger.debug(f"Experiment progress: {value}")
