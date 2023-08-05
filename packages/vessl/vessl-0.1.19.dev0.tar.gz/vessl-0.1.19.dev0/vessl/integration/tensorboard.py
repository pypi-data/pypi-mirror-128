import importlib
import io

from PIL import Image

from vessl.internal import log
from vessl.util import logger
from vessl.util.image import Image as VesslImage


def _create_payload_from_event(event):
    payload = {}
    for proto_value in event.summary.value:
        key = proto_value.tag
        fields = set(f.name for f, _ in proto_value.ListFields())

        if "image" in fields:
            image = Image.open(io.BytesIO(proto_value.image.encoded_image_string))
            payload[key] = VesslImage(data=image, caption=key)

        elif "simple_value" in fields:
            payload[key] = proto_value.simple_value

        else:
            continue
    return payload


def _patch_event_file_writer(writer_module):
    old_writer_class = writer_module.EventFileWriter

    class CustomEventFileWriter(old_writer_class):
        def add_event(self, event, *args, **kwargs):
            super(CustomEventFileWriter, self).add_event(event, *args, **kwargs)

            if not event.HasField("summary"):
                return

            payload = _create_payload_from_event(event)
            log(payload=payload, step=event.step)

    # Patch module writer
    writer_module.EventFileWriter = CustomEventFileWriter


def tensorboard():
    """Integrate tensorboard"""
    # "tensorflow.python.ops.gen_summary_ops"  # TODO: support this module
    module_names = [
        "tensorflow.python.summary.writer.writer",
        "tensorboard.summary.writer.event_file_writer",
        "torch.utils.tensorboard.writer",
        "tensorboardX.writer",
    ]

    is_patched = False
    for name in module_names:
        try:
            module = importlib.import_module(name)
        except Exception as e:
            logger.debug(f"Module {name} not found. Skipping patch...")
            continue

        _patch_event_file_writer(module)
        is_patched = True

    if not is_patched:
        logger.warning(
            "Failed to integrate tensorboard because no Tensorboard modules were found."
        )
