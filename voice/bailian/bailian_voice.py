# coding=utf-8
from common.log import logger
from config import conf
from bridge.reply import Reply, ReplyType
import datetime
import random
from voice.voice import Voice
import dashscope
from dashscope.audio.tts_v2 import *

class BailianVoice(Voice):
    def textToVoice(self, text):
        dashscope.api_key = conf().get("dashscope_api_key")
        model = conf().get("dashscope_model")
        voice = conf().get("dashscope_voice")
        synthesizer = SpeechSynthesizer(model=model, voice=voice)

        audio = synthesizer.call(text)
        file_path = "tmp/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 1000)) + ".mp3"
        if audio:
            with open(file_path, 'wb') as f:
                f.write(audio)

            logger.info(f"Create speech of voice: {voice} to file: {file_path}")
            return Reply(ReplyType.VOICE, file_path)
        else:
            logger.error(f"Failed to create speech for voice: {voice}")
            return Reply(ReplyType.ERROR, "我暂时还无法听清您的语音，请稍后再试吧~")