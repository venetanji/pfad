import base64
import io
import logging
import os
import wave
import base64

import numpy as np
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager

# This is one of the speaker voices that comes with xtts
SPEAKER_NAME = "Wulf Carlevaro"


class XttsStreamer:
    def __init__(self, **kwargs):
        self.model = None
        self.speaker = None

    def load(self):
        device = "cuda"
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        logging.info("⏳Downloading model")
        ModelManager().download_model(model_name)
        model_path = os.path.join(
            get_user_data_dir("tts"), model_name.replace("/", "--")
        )

        config = XttsConfig()
        config.load_json(os.path.join(model_path, "config.json"))
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config, checkpoint_dir=model_path, eval=True)
        self.model.to(device)

        self.speaker = {
            "speaker_embedding": self.model.speaker_manager.speakers[SPEAKER_NAME][
                "speaker_embedding"
            ]
            .cpu()
            .squeeze()
            .half()
            .tolist(),
            "gpt_cond_latent": self.model.speaker_manager.speakers[SPEAKER_NAME][
                "gpt_cond_latent"
            ]
            .cpu()
            .squeeze()
            .half()
            .tolist(),
        }
        self.speaker_embedding = (
            torch.tensor(self.speaker.get("speaker_embedding"))
            .unsqueeze(0)
            .unsqueeze(-1)
        )
        self.gpt_cond_latent = (
            torch.tensor(self.speaker.get("gpt_cond_latent"))
            .reshape((-1, 1024))
            .unsqueeze(0)
        )
        logging.info("🔥Model Loaded")

    def wav_postprocess(self, wav):
        """Post process the output waveform"""
        if isinstance(wav, list):
            wav = torch.cat(wav, dim=0)
        wav = wav.clone().detach().cpu().numpy()
        wav = np.clip(wav, -1, 1)
        wav = (wav * 32767).astype(np.int16)
        return wav
    
    def encode_audio_common(
            self, frame_input, encode_base64=True, sample_rate=24000, sample_width=2, channels=1
        ):
        """Return base64 encoded audio"""
        wav_buf = io.BytesIO()
        with wave.open(wav_buf, "wb") as vfout:
            vfout.setnchannels(channels)
            vfout.setsampwidth(sample_width)
            vfout.setframerate(sample_rate)
            vfout.writeframes(frame_input)

        wav_buf.seek(0)
        if encode_base64:
            b64_encoded = base64.b64encode(wav_buf.getbuffer()).decode("utf-8")
            return b64_encoded
        else:
            return wav_buf.read()

    def predict(self, model_input):
        text = model_input.get("text")
        language = model_input.get("language", "en")
        chunk_size = int(
            model_input.get("chunk_size", 10)
        )  # Ensure chunk_size is an integer
        #print("Model chunk size: ", chunk_size)
        add_wav_header = True


        with torch.inference_mode():
            streamer = self.model.inference_stream(
                text,
                language,
                self.gpt_cond_latent,
                self.speaker_embedding,
                stream_chunk_size=chunk_size,
                enable_text_splitting=True,
            )

            for i, chunk in enumerate(streamer):
                if i == 0 and add_wav_header:
                    yield self.encode_audio_common(b"", encode_base64=False)
                
                yield self.wav_postprocess(chunk).tobytes()