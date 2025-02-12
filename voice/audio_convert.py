import os
import shutil
import wave
import ffmpeg
from common.log import logger


try:
    from pydub import AudioSegment
except ImportError:
    logger.warning("import pydub failed, wechat voice conversion will not be supported. Try: pip install pydub")

try:
    import pilk
except ImportError:
    logger.warning("import pilk failed, silk voice conversion will not be supported. Try: pip install pilk")

sil_supports = [8000, 12000, 16000, 24000, 32000, 44100, 48000]  # slk转wav时，支持的采样率


def find_closest_sil_supports(sample_rate):
    """
    找到最接近的支持的采样率
    """
    if sample_rate in sil_supports:
        return sample_rate
    closest = 0
    mindiff = 9999999
    for rate in sil_supports:
        diff = abs(rate - sample_rate)
        if diff < mindiff:
            closest = rate
            mindiff = diff
    return closest


def get_pcm_from_wav(wav_path):
    """
    从 wav 文件中读取 pcm

    :param wav_path: wav 文件路径
    :returns: pcm 数据
    """
    wav = wave.open(wav_path, "rb")
    return wav.readframes(wav.getnframes())


def any_to_mp3(any_path, mp3_path):
    """
    把任意格式转成mp3文件
    
    Args:
        any_path: 输入文件路径
        mp3_path: 输出的mp3文件路径
    """
    try:
        # 如果已经是mp3格式，直接复制
        if any_path.endswith(".mp3"):
            shutil.copy2(any_path, mp3_path)
            return
        
        # 如果是silk格式，使用pilk转换
        if any_path.endswith((".sil", ".silk", ".slk")):
            # 先转成PCM
            pcm_path = any_path + '.pcm'
            pilk.decode(any_path, pcm_path)
            
            # 再用pydub把PCM转成MP3
            # TODO: 下面的参数可能需要调整
            audio = AudioSegment.from_raw(pcm_path, format="raw", 
                                        frame_rate=24000,
                                        channels=1,
                                        sample_width=2)  # 16-bit PCM = 2 bytes
            audio.export(mp3_path, format="mp3")
            
            # 清理临时PCM文件
            import os
            os.remove(pcm_path)
            return
        
        # 其他格式使用pydub转换
        audio = AudioSegment.from_file(any_path)
        audio.export(mp3_path, format="mp3")

    except Exception as e:
        logger.error(f"转换文件到mp3失败: {str(e)}")
        raise


def any_to_wav(any_path, wav_path):
    """
    把任意格式转成wav文件
    """
    if any_path.endswith(".wav"):
        shutil.copy2(any_path, wav_path)
        return
    if any_path.endswith(".sil") or any_path.endswith(".silk") or any_path.endswith(".slk"):
        return sil_to_wav(any_path, wav_path)
    audio = AudioSegment.from_file(any_path)
    audio.set_frame_rate(8000)    # 百度语音转写支持8000采样率, pcm_s16le, 单通道语音识别
    audio.set_channels(1)
    audio.export(wav_path, format="wav", codec='pcm_s16le')



def mp3_to_silk(mp3_path: str, silk_path: str) -> int:
    """Convert MP3 file to SILK format"""
    try:
        # 生成临时PCM文件路径
        pcm_path = mp3_path + '.temp.pcm'
        
        # 使用ffmpeg将MP3转换为24kHz单声道PCM
        (
            ffmpeg.input(mp3_path)
            .output(pcm_path, format='s16le', ar=24000)
            .overwrite_output()
            .run(quiet=True)
        )
        
        # 使用pilk进行SILK编码并添加tencent参数
        duration = pilk.encode(pcm_path, silk_path, pcm_rate=24000, tencent=True)
        
        # 清理临时文件
        if os.path.exists(pcm_path):
            os.remove(pcm_path)
            
        return duration
    except Exception as e:
        # 确保异常时清理临时文件
        if 'pcm_path' in locals() and os.path.exists(pcm_path):
            os.remove(pcm_path)
        logger.error(f"MP3转SILK失败: {str(e)}")
        raise

def any_to_amr(any_path, amr_path):
    """
    把任意格式转成amr文件
    """
    if any_path.endswith(".amr"):
        shutil.copy2(any_path, amr_path)
        return
    if any_path.endswith(".sil") or any_path.endswith(".silk") or any_path.endswith(".slk"):
        raise NotImplementedError("Not support file type: {}".format(any_path))
    audio = AudioSegment.from_file(any_path)
    audio = audio.set_frame_rate(8000)  # only support 8000
    audio.export(amr_path, format="amr")
    return audio.duration_seconds * 1000

def sil_to_wav(silk_path, wav_path, rate: int = 24000):
    """
    silk 文件转 wav
    """
    # 创建临时PCM文件
    pcm_path = silk_path + '.pcm'
    
    try:
        # 解码SILK到PCM
        pilk.decode(silk_path, pcm_path)
        
        # 读取PCM数据
        with open(pcm_path, 'rb') as f:
            pcm_data = f.read()
        
        # 写入WAV文件
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(rate)
            wav_file.writeframes(pcm_data)
    finally:
        # 清理临时文件
        if os.path.exists(pcm_path):
            os.remove(pcm_path)


def split_audio(file_path, max_segment_length_ms=60000):
    """
    分割音频文件
    """
    audio = AudioSegment.from_file(file_path)
    audio_length_ms = len(audio)
    if audio_length_ms <= max_segment_length_ms:
        return audio_length_ms, [file_path]
    segments = []
    for start_ms in range(0, audio_length_ms, max_segment_length_ms):
        end_ms = min(audio_length_ms, start_ms + max_segment_length_ms)
        segment = audio[start_ms:end_ms]
        segments.append(segment)
    file_prefix = file_path[: file_path.rindex(".")]
    format = file_path[file_path.rindex(".") + 1 :]
    files = []
    for i, segment in enumerate(segments):
        path = f"{file_prefix}_{i+1}" + f".{format}"
        segment.export(path, format=format)
        files.append(path)
    return audio_length_ms, files
