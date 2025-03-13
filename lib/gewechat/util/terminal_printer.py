import os
import qrcode
from common.log import logger

def print_green(text):
    logger.info(text)

def print_yellow(text):
    logger.warning(text)

def print_red(text):
    logger.error(text)

def make_and_print_qr(url):
    """生成并打印二维码

    Args:
        url: 需要生成二维码的URL字符串

    Returns:
        str: 生成的二维码图片路径
    """
    logger.info(f"您可以访问下方链接获取二维码:\nhttps://api.qrserver.com/v1/create-qr-code/?data={url}")
    logger.info("也可以扫描下方二维码登录")
    
    # 二维码仍然需要在终端显示，所以保留print
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)

    # 确保tmp目录存在（使用绝对路径）
    # 获取当前工作目录（项目根目录）
    current_dir = os.getcwd()
    tmp_dir = os.path.join(current_dir, 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    # 生成二维码图片并保存（使用绝对路径）
    img = qrcode.make(data=url)
    qr_image_path = os.path.join(tmp_dir, 'login.png')
    with open(qr_image_path, 'wb') as f:
        img.save(f)
    
    logger.info(f"二维码已保存至 {qr_image_path}")
    
    # 返回二维码图片绝对路径，以便在网页中显示
    return qr_image_path
