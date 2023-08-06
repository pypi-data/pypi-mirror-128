import os
from typing import Optional, Union

import shortuuid
import six
import soundfile as sf

from vessl.util import logger
from vessl.util.constant import VESSL_AUDIO_PATH, VESSL_MEDIA_PATH
from vessl.util.exception import InvalidParamsError


class Audio:
    def __init__(
        self,
        data_or_path: Union[str, "Audio"],
        sample_rate: int = None,
        caption: Optional[str] = None,
    ):
        self._audio = None
        self._sample_rate = None
        self._caption = None
        self._path = None

        self._init_meta(sample_rate, caption)
        self._init_audio(data_or_path)
        self._save_audio()

    def _init_meta(self, sample_rate, caption):
        self._sample_rate = sample_rate
        self._caption = caption

        audio_root = os.path.join(VESSL_MEDIA_PATH, VESSL_AUDIO_PATH)
        os.makedirs(audio_root, exist_ok=True)
        self._path = os.path.join(audio_root, Audio.generate_uuid() + ".wav")

    def _init_audio_from_path(self, path):
        self._audio, self._sample_rate = sf.read(path)

    def _init_audio_from_data(self, data):
        if self._sample_rate is None:
            raise InvalidParamsError("sample_rate is required for Vessl Audio class")
        self._audio = data

    def _init_audio(self, data_or_path):
        if isinstance(data_or_path, Audio):
            self._audio = data_or_path._audio
        elif isinstance(data_or_path, six.string_types):
            self._init_audio_from_path(data_or_path)
        else:
            self._init_audio_from_data(data_or_path)

    def _save_audio(self):
        sf.write(self._path, self._audio, self._sample_rate)

    def flush(self):
        if os.path.isfile(self._path):
            os.remove(self._path)
        else:
            logger.error(f"Error: {self._path} file not found")

    @property
    def path(self):
        return self._path

    @property
    def caption(self):
        return self._caption

    @classmethod
    def generate_uuid(cls):
        generated_uuid = shortuuid.ShortUUID(
            alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz")
        )
        return generated_uuid.random(8)
