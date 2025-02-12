"""
channel factory
"""
from common import const


def create_bot(bot_type):
    """
    create a bot_type instance
    :param bot_type: bot type code
    :return: bot instance
    """
    if bot_type == const.COZE:
        from bot.Coze.bot import CozeBot
        return CozeBot()
 
    raise RuntimeError
