<div align="center">
<img src="https://lf-coze-web-cdn.coze.cn/obj/coze-web-cn/obric/coze/favicon.1970.png" alt="Coze" width="100">
<h1>Coze on WeChat</h1>

本项目基于chatgpt-on-wechat和dify-on-wechat 二次开发，主要是对接 coze 平台

如果我的项目对您有帮助请点一个star吧~
</div>

## 功能展示
![微信截图_20250213101950](https://github.com/user-attachments/assets/aadf95b7-0291-4ff3-9f3d-1905e02eb93d)

# 文本聊天功能
继承自chatgpt-on-wechat和dify-on-wechat
![image](https://github.com/user-attachments/assets/96551277-dde1-4ccd-8cc6-418643cd9f83)

# 语音功能
支持语音识别，但是只支持发送20s以内语音，接收没有限制
![image](https://github.com/user-attachments/assets/e72329ed-dc35-47d4-bf18-8d4d672bec77)

语音回复

![image](https://github.com/user-attachments/assets/93625656-e77f-43d4-9cfb-dcdc7bc4abc4)

https://github.com/user-attachments/assets/e221d35b-e6bb-479c-9850-3c5d404511e5

# 插件功能
支持coze插件，支持插件卡片转微信链接

![image](https://github.com/user-attachments/assets/738fd3b9-6be4-407f-a60c-aa995268535b)

![image](https://github.com/user-attachments/assets/56934c06-64fd-43bf-8522-535edd5edfb0)


# 快速使用

## 1. 准备
本项目主要对接coze平台，所以需要在[Coze平台注册账号](https://www.coze.cn/)，并且创建机器人，创建完成后需要前往[个人访问令牌页面](https://www.coze.cn/open/oauth/pats)添加令牌

## 2.运行环境
基于[Gewechat](https://github.com/Devo919/Gewechat)项目实现的微信个人号通道,使用ipad协议登录,相比itchat协议更稳定。

### 部署gewechat服务

```bash
# 从阿里云镜像仓库拉取(国内)
docker pull registry.cn-hangzhou.aliyuncs.com/gewe/gewe:latest
docker tag registry.cn-hangzhou.aliyuncs.com/gewe/gewe gewe

# 创建数据目录并启动服务
mkdir -p /root/temp
docker run -itd -v /root/temp:/root/temp -p 2531:2531 -p 2532:2532 --privileged=true --name=gewe gewe /usr/sbin/init
```


**(1) 克隆项目代码：**

```bash
git clone https://github.com/JC0v0/Coze-on-Wechat
cd Coze-on-Wechat/
```

**(2) 安装核心依赖 (必选)：**

```bash
pip3 install -r requirements.txt
```

**(3) 拓展依赖 (可选，建议安装)：**

```bash
pip3 install -r requirements-optional.txt
```
> 如果某项依赖安装失败可注释掉对应的行再继续

## 3. 配置
> 配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的`config.json`文件：
```bash
cp config-template.json config.json
```
> 然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改（请去掉注释）：
```json
{
  // Bot 相关配置
  "channel_type": "gewechat",
  "model": "coze",
  // coze 相关配置
  "coze_api_base": "YOUR API KEY",
  "coze_api_key": "YOUR API KEY",
  "coze_bot_id": "",    //智能体ID。进入智能体的开发页面，开发页面 URL 中 bot 参数后的数字就是智能体ID。例如https://www.coze.cn/space/341****/bot/73428668*****，bot_id 为73428668*****。
  "coze_voice_id": "",  //音色的 ID，具体教程前往 https://www.coze.cn/open/docs/developer_guides/list_voices 查看
  "coze_space_id": "",   //空间的 ID
  // 私聊回复的前缀，用于区分真人
  "single_chat_prefix": [
    "bot",
    "@bot"
  ],
  
  "single_chat_reply_prefix": "[bot] ",
  // 群组聊天前缀，用于区分真人
  "group_chat_prefix": [
    "@bot"
  ],
  "group_name_white_list": [
    "ChatGPT测试群",
    "ChatGPT测试群2"
  ],
  // 语音回复配置
  "speech_recognition": false,
  "group_speech_recognition": false,
  "text_to_voice": "coze",
  "voice_reply_voice": false,
  // gewechat 相关配置
  "gewechat_app_id": "",
  "gewechat_base_url": "http://127.0.0.1:2531/v2/api",
  "gewechat_callback_url": "http://127.0.0.1:9919/v2/api/callback/collect",
  "gewechat_download_url": "http://127.0.0.1:2532/download",
  "gewechat_token": ""
}

```
## 4. 运行

###  本地运行
```bash
python3 app.py
```
### 服务器部署
```bash
# 启动
nohup python3 app.py & tail -f nohup.out  # 在后台运行程序并通过日志输出二维码
# 关闭
pkill -f app.py
```

### Web界面
```bash
cd Coze-on-Wechat/
streamlit run Home.py
```

[![Star History Chart](https://api.star-history.com/svg?repos=JC0v0/Coze-on-Wechat&type=Date)](https://star-history.com/#JC0v0/Coze-on-Wechat&Date)

## 联系我
![image](https://github.com/user-attachments/assets/d61764ec-c975-4b34-96c3-96bef668d67a)
