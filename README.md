# ⚡️ UESTC-Energyfy 自动化部署版

> 基于原项目优化，支持 **GitHub Actions** 和 **云服务器** 一键部署

查询电子科技大学宿舍的电费余额，在低于阈值时自动发送邮件通知和 Server酱³ 推送。

**新功能：**
- ✅ 支持 GitHub Actions 自动运行（无需服务器！）
- ✅ 完整的部署文档和配置脚本
- ✅ 配置验证工具
- ✅ 云服务器一键部署脚本

---

## 📚 快速导航

| 文档 | 适用场景 | 难度 |
|------|---------|------|
| [⚡️ 快速开始](QUICKSTART.md) | **推荐！** GitHub Actions 5分钟部署 | ⭐ 简单 |
| [📖 完整部署指南](DEPLOYMENT.md) | GitHub Actions 详细配置 | ⭐⭐ 中等 |
| [☁️ 云服务器部署](CLOUDSERVER.md) | 有自己的服务器 | ⭐⭐⭐ 较难 |
| [📝 原版 README](README_ORIGINAL.md) | 本地电脑运行（原始方式） | ⭐⭐ 中等 |

---

## 🎯 推荐方案对比

### 🥇 GitHub Actions（推荐）

**优势：**
- ✅ 完全免费
- ✅ 无需服务器
- ✅ 自动运行，无需维护
- ✅ 配置简单，5分钟完成

**劣势：**
- ⚠️ 最短间隔 5 分钟
- ⚠️ 私有仓库有使用限制（公开仓库无限制）

**适合：** 所有用户，特别是没有服务器的同学

👉 [查看快速开始指南](QUICKSTART.md)

---

### 🥈 云服务器

**优势：**
- ✅ 稳定性高
- ✅ 响应及时
- ✅ 无间隔限制

**劣势：**
- ❌ 需要付费
- ❌ 需要配置环境

**适合：** 有云服务器的用户

👉 [查看云服务器部署指南](CLOUDSERVER.md)

---

### 🥉 本地电脑（不推荐）

**优势：**
- ✅ 完全掌控

**劣势：**
- ❌ 需要保持开机
- ❌ 关机服务停止
- ❌ 占用电脑资源

**适合：** 测试或短期使用

👉 [查看原版 README](README_ORIGINAL.md)

---

## 🚀 5分钟快速部署（GitHub Actions）

### 1️⃣ Fork 本仓库

点击右上角 **Fork** 按钮

### 2️⃣ 配置 Secrets

进入你的仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下配置（**必需**）：

| Name | Value | 示例 |
|------|-------|------|
| `UESTC_USERNAME` | 你的学号 | `2021010101` |
| `UESTC_PASSWORD` | 统一认证密码 | `yourPassword` |
| `ROOM_NAME` | 宿舍号 | `114514` |
| `ALERT_BALANCE` | 告警阈值 | `10` |
| `SMTP_SERVER` | SMTP服务器 | `smtp.qq.com` |
| `SMTP_PORT` | SMTP端口 | `465` |
| `SMTP_USERNAME` | 邮箱 | `your@qq.com` |
| `SMTP_PASSWORD` | 邮箱授权码 | `abcdefghijkl` |

> ⚠️ **重要**：`SMTP_PASSWORD` 是邮箱**授权码**，不是登录密码！
> 
> 如何获取授权码？
> - **QQ邮箱**：设置 → 账户 → POP3/IMAP/SMTP → 生成授权码
> - **163邮箱**：设置 → POP3/SMTP/IMAP → 设置授权密码

### 3️⃣ 启用 Actions

1. 点击 **Actions** 标签
2. 点击 **I understand my workflows, go ahead and enable them**
3. 选择 **UESTC Energy Monitor**
4. 点击 **Run workflow** 测试

### 4️⃣ 完成！

✅ 每 30 分钟自动检查一次  
✅ 余额不足自动发送邮件  
✅ 完全自动化，无需维护

---

## 📧 通知示例

| 邮件通知 | Server酱推送 |
|---------|-------------|
| ![邮件通知](https://cloud.athbe.cn/f/Bef9/9USEFCXMK2QMH%602KP%28GX%7DTP.png) | ![Server酱推送](https://cloud.athbe.cn/f/RNtB/578d16a600844487c70255a8e49b6911.jpg) |

---

## 🛠️ 高级配置

### 监控多个宿舍

在 `ROOM_NAME` Secret 中用逗号分隔：
```
114514,214514,314514
```

### 调整检查频率

编辑 `.github/workflows/energy-monitor.yml`：
```yaml
schedule:
  - cron: '*/30 * * * *'  # 每30分钟（默认）
  # - cron: '0 * * * *'     # 每小时
  # - cron: '0 8,20 * * *'  # 每天8点和20点
```

### 启用 Server酱³推送

1. 访问 [Server酱官网](https://sc3.ft07.com/) 注册
2. 获取 UID 和 SendKey
3. 添加 Secrets：
   - `SERVER_CHAN_ENABLED`: `true`
   - `SERVER_CHAN_UID`: 你的UID
   - `SERVER_CHAN_SENDKEY`: 你的SendKey

---

## 🧪 配置验证工具

在提交到 GitHub 之前，可以本地测试配置：

```bash
# 创建配置文件
cp config.example.json config.json
nano config.json  # 编辑配置

# 运行验证脚本
python3 scripts/test_config.py
```

验证脚本会检查：
- ✅ 配置文件格式
- ✅ 必需字段完整性
- ✅ SMTP 连接和认证
- ✅ Server酱 连接（如果启用）

---

## 📂 项目结构

```
UESTC-Energyfy/
├── .github/
│   └── workflows/
│       └── energy-monitor.yml    # GitHub Actions 工作流
├── scripts/
│   ├── generate_config.py        # 从环境变量生成配置
│   └── test_config.py            # 配置验证工具
├── utils/                         # 工具模块
│   ├── Config.py                 # 配置读取
│   ├── RoomInfo.py               # 房间信息查询
│   ├── NotificationManager.py    # 通知管理
│   └── ...
├── Energyfy.py                   # 主程序
├── requirements.txt              # Python 依赖
├── schema.json                   # 配置文件 Schema
├── QUICKSTART.md                 # ⚡️ 快速开始
├── DEPLOYMENT.md                 # 📖 完整部署指南
├── CLOUDSERVER.md                # ☁️ 云服务器部署
└── README.md                     # 本文件
```

---

## ❓ 常见问题

### Q: 免费吗？

**A:** GitHub Actions 对公开仓库完全免费，私有仓库每月 2000 分钟免费额度。

### Q: 安全吗？

**A:** 
- ✅ 使用 GitHub Secrets 加密存储敏感信息
- ✅ 建议将仓库设为私有
- ✅ 不会泄露你的密码

### Q: 登录失败 401 错误

**A:** 
1. 检查学号和密码
2. 到官网手动登录一次
3. 等待几分钟后重试

### Q: 邮件发送失败

**A:** 
1. 确认使用**授权码**不是密码
2. 检查 SMTP 服务是否开启
3. 验证 SMTP 服务器地址和端口

### Q: 如何停止监控？

**A:** Actions → UESTC Energy Monitor → ... → Disable workflow

---

## 📜 更新日志

### v1.3.0 (2024-01-XX)

- ✨ 新增 GitHub Actions 支持
- ✨ 新增配置生成脚本
- ✨ 新增配置验证工具
- 📝 新增完整的部署文档
- 🐛 优化错误处理

### v1.2.0 (原版)

- ✨ 支持 Server酱³推送
- ✨ 支持多房间监控
- ✨ 并发发送通知

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目基于原仓库进行优化，继承原许可证。

---

## 🙏 致谢

- 原项目作者：[AthBe1337](https://github.com/AthBe1337/UESTC-Energyfy)
- Server酱³：[ft07.com](https://sc3.ft07.com/)

---

## 📞 支持

- 📖 [查看文档](QUICKSTART.md)
- 🐛 [提交 Issue](../../issues)
- 💬 [讨论区](../../discussions)

---

**开始使用：** [⚡️ 5分钟快速部署](QUICKSTART.md)
