# Docker 部署指南

本文档提供了使用 Docker 快速部署 Coze-on-Wechat 项目的步骤。

## 前提条件

- 安装 [Docker](https://docs.docker.com/get-docker/)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)
- 在 [Coze 平台](https://www.coze.cn/) 注册账号并创建机器人
- 获取 [个人访问令牌](https://www.coze.cn/open/oauth/pats)

## 部署步骤

### 1. 克隆项目

```bash
git clone https://github.com/JC0v0/Coze-on-Wechat
cd Coze-on-Wechat
```

### 2. 准备配置文件

如果您想在启动前配置好 `config.json`，可以复制模板并编辑：

```bash
cp config-template.json config.json
# 编辑 config.json 文件，填入您的 Coze 访问令牌和其他配置
```

```json
{
    "gewechat_base_url": "http://gewechat:2531/v2/api",  // docker部署时需要这样配置
    "gewechat_callback_url": "http://coze-on-wechat:9919/v2/api/callback/collect", // docker部署时需要这样配置
    "gewechat_download_url": "http://gewechat:2532/download", // docker部署时需要这样配置
}
```

或者，您也可以在 Web 界面启动后进行配置。

### 3. 创建必要的目录

```bash
mkdir -p gewechat/data
```

### 4. 使用 Docker Compose 启动服务

```bash
docker-compose up -d
```

### 5. 访问 Web 界面

在浏览器中访问：`http://您的服务器IP:8501`

通过 Web 界面完成配置并登录微信。

## 常用命令

- 查看日志：
  ```bash
  docker-compose logs -f
  ```

- 停止服务：
  ```bash
  docker-compose down
  ```

- 重启服务：
  ```bash
  docker-compose restart
  ```

- 更新镜像并重新部署：
  ```bash
  git pull
  docker-compose down
  docker-compose up -d --build
  ```

## 数据持久化

以下数据通过 volumes 挂载实现持久化：

- `config.json`：配置文件
- `gewechat/data`：微信登录数据

## 注意事项

1. 首次登录微信时，需要通过 Web 界面扫描二维码
2. 确保服务器防火墙开放了 8501、2531 和 2532 端口
