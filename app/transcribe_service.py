import asyncio
from typing import Union
from faster_whisper import WhisperModel
from constants import enviroment


class TranscribeService:

    def __init__(self) -> None:
        device = enviroment.WHISPER_DEVICE
        model_type = enviroment.WHISPER_MODEL

        if device == "cpu":
            compute_type = "int8"
        else:
            compute_type = "float16"

        self._model = WhisperModel(model_type, device=device, compute_type=compute_type)

    async def transcribe(self, path_to_audio: str) -> Union[str, None]:
        try:
            segments, _ = await asyncio.to_thread(self._model.transcribe, path_to_audio)
            text = "\n".join([segment.text for segment in segments])
            return text
        except Exception as e:
            print(f"TranscribeService -> transcribe error:\n{e}")
            return None

transcribe_service = TranscribeService()