import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="InviteMember",
    desire_priority=-1,
    desc="群聊邀请成员",
    version="0.1",
    author="JCOvO",
)
class InviteMember(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[InviteMember] inited")
        