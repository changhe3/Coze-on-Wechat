import os
import json
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf, save_config


@plugins.register(
    name="SetVoice",
    desire_priority=-1,
    hidden=True,
    desc="设置语音功能开关，包括语音识别、语音回复等功能",
    version="0.1",
    author="JC",
)
class SetVoice(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[SetVoice] inited")
            
        except Exception as e:
            logger.error(f"[SetVoice]初始化异常：{e}")
            raise Exception("[SetVoice] init failed, ignore ")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        
        content = e_context["context"].content.strip()
        if not content.startswith("#voice"):
            return
        
        msg: ChatMessage = e_context["context"]["msg"]
        reply = self.handle_voice_command(content)
        
        if reply:
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def handle_voice_command(self, content: str) -> Reply:
        """处理语音相关命令"""
        try:
            params = content.split()
            if len(params) < 2:
                return Reply(ReplyType.TEXT, self.get_help_text())
            
            command = params[1].lower()
            
            if command == "语音识别":
                if len(params) < 3:
                    return Reply(ReplyType.TEXT, "请指定开关状态：on/off")
                status = params[2].lower()
                if status == "on":
                    conf().set("speech_recognition", True)
                    save_config()
                    return Reply(ReplyType.TEXT, "语音识别功能已开启")
                elif status == "off":
                    conf().set("speech_recognition", False)
                    save_config()
                    return Reply(ReplyType.TEXT, "语音识别功能已关闭")
                else:
                    return Reply(ReplyType.TEXT, "无效的状态值，请使用 on/off")
                    
            elif command == "语音回复语音":
                if len(params) < 3:
                    return Reply(ReplyType.TEXT, "请指定开关状态：on/off")
                status = params[2].lower()
                if status == "on":
                    conf().set("voice_reply_voice", True)
                    save_config()
                    return Reply(ReplyType.TEXT, "语音回复功能已开启")
                elif status == "off":
                    conf().set("voice_reply_voice", False)
                    save_config()
                    return Reply(ReplyType.TEXT, "语音回复功能已关闭")
                else:
                    return Reply(ReplyType.TEXT, "无效的状态值，请使用 on/off")
                    
            elif command == "始终语音回复":
                if len(params) < 3:
                    return Reply(ReplyType.TEXT, "请指定开关状态：on/off")
                status = params[2].lower()
                if status == "on":
                    conf().set("always_reply_voice", True)
                    save_config()
                    return Reply(ReplyType.TEXT, "始终语音回复功能已开启")
                elif status == "off":
                    conf().set("always_reply_voice", False)
                    save_config()
                    return Reply(ReplyType.TEXT, "始终语音回复功能已关闭")
                else:
                    return Reply(ReplyType.TEXT, "无效的状态值，请使用 on/off")
                    
            elif command == "status":
                recognition = conf().get("speech_recognition", False)
                reply_voice = conf().get("voice_reply_voice", False)
                always_voice = conf().get("always_reply_voice", False)
                
                status = "语音功能状态：\n"
                status += f"1. 语音识别：{'开启' if recognition else '关闭'}\n"
                status += f"2. 语音回复：{'开启' if reply_voice else '关闭'}\n"
                status += f"3. 始终语音回复：{'开启' if always_voice else '关闭'}"
                return Reply(ReplyType.TEXT, status)
                
            else:
                return Reply(ReplyType.TEXT, self.get_help_text())
                
        except Exception as e:
            logger.error(f"处理语音命令时出错：{str(e)}")
            return Reply(ReplyType.TEXT, f"设置失败：{str(e)}")

    def get_help_text(self, **kwargs):
        help_text = "语音设置功能指令：\n"
        help_text += "1. #voice 语音识别 on/off - 开启/关闭语音识别\n"
        help_text += "2. #voice 语音回复语音 on/off - 开启/关闭语音回复\n"
        help_text += "3. #voice 始终语音回复 on/off - 开启/关闭始终语音回复\n"
        help_text += "4. #voice status - 查看语音功能状态"
        return help_text
