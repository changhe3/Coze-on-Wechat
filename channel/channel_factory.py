"""
channel factory
"""
from common import const
from .channel import Channel


def create_channel(channel_type) -> Channel:
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    ch = Channel()
    
    if channel_type == "gewechat":
        from channel.gewechat.gewechat_channel import GeWeChatChannel
        ch = GeWeChatChannel()
    else:
        raise RuntimeError
    ch.channel_type = channel_type
    return ch
