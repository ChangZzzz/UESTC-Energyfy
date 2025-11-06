#!/usr/bin/env python3
"""
从环境变量生成配置文件
用于 GitHub Actions 自动化部署
"""
import os
import json
import sys


def get_env(key, default=None, required=False):
    """获取环境变量"""
    value = os.getenv(key, default)
    if required and not value:
        print(f"❌ 错误：缺少必需的环境变量 {key}", file=sys.stderr)
        sys.exit(1)
    return value


def parse_list(value, separator=','):
    """解析列表类型的环境变量"""
    if not value:
        return []
    return [item.strip() for item in value.split(separator) if item.strip()]


def parse_bool(value, default=False):
    """解析布尔类型的环境变量"""
    if not value:
        return default
    return value.lower() in ('true', 'yes', '1', 'on')


def main():
    print("🔧 开始生成配置文件...")
    
    # 读取基本配置
    username = get_env('UESTC_USERNAME', required=True)
    password = get_env('UESTC_PASSWORD', required=True)
    alert_balance = float(get_env('ALERT_BALANCE', '10'))
    check_interval = int(get_env('CHECK_INTERVAL', '0'))  # GitHub Actions 使用单次模式
    
    # Server酱配置（先读取，用于判断邮箱是否必需）
    server_chan_enabled = parse_bool(get_env('SERVER_CHAN_ENABLED', 'false'))
    
    # 读取 SMTP 配置（如果启用了 Server酱，邮箱配置可选）
    smtp_required = not server_chan_enabled  # 如果没启用 Server酱，邮箱必需
    smtp_server = get_env('SMTP_SERVER', required=smtp_required)
    smtp_port = int(get_env('SMTP_PORT', '465'))
    smtp_username = get_env('SMTP_USERNAME', required=smtp_required)
    smtp_password = get_env('SMTP_PASSWORD', required=smtp_required)
    smtp_security = get_env('SMTP_SECURITY', 'ssl')
    
    # 读取房间配置（支持多个房间）
    room_names = parse_list(get_env('ROOM_NAME', required=True))
    email_recipients = parse_list(get_env('EMAIL_RECIPIENTS', ''))
    server_chan_uid = get_env('SERVER_CHAN_UID', '')
    server_chan_sendkey = get_env('SERVER_CHAN_SENDKEY', '')
    
    # 支持多个 Server酱 收件人（可选）
    server_chan_uids = parse_list(get_env('SERVER_CHAN_UID', ''))
    server_chan_sendkeys = parse_list(get_env('SERVER_CHAN_SENDKEY', ''))
    
    # 构建 Server酱 收件人列表
    server_chan_recipients = []
    if server_chan_enabled and server_chan_uids and server_chan_sendkeys:
        for uid, sendkey in zip(server_chan_uids, server_chan_sendkeys):
            if uid and sendkey:
                server_chan_recipients.append({
                    "uid": uid,
                    "sendkey": sendkey
                })
    
    # 如果没有收件人但启用了 Server酱，添加一个空列表防止验证失败
    if server_chan_enabled and not server_chan_recipients:
        server_chan_recipients.append({
            "uid": "placeholder",
            "sendkey": "placeholder"
        })
    
    # 构建查询列表（支持多个房间）
    queries = []
    for room_name in room_names:
        query = {
            "room_name": room_name,
            "recipients": email_recipients if email_recipients else ["placeholder@example.com"],
            "server_chan": {
                "enabled": server_chan_enabled,
                "recipients": server_chan_recipients
            }
        }
        queries.append(query)
    
    # 构建完整配置
    config = {
        "username": username,
        "password": password,
        "check_interval": check_interval,
        "alert_balance": alert_balance,
        "smtp": {
            "server": smtp_server if smtp_server else "smtp.placeholder.com",
            "port": smtp_port,
            "username": smtp_username if smtp_username else "placeholder@example.com",
            "password": smtp_password if smtp_password else "placeholder",
            "security": smtp_security
        },
        "queries": queries
    }
    
    # 写入配置文件
    config_path = 'config.json'
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件已生成：{config_path}")
        print(f"📊 监控房间数：{len(room_names)}")
        print(f"📧 邮件收件人数：{len(email_recipients)}")
        print(f"📱 Server酱收件人数：{len(server_chan_recipients) if server_chan_enabled else 0}")
        return 0
    except Exception as e:
        print(f"❌ 生成配置文件失败：{e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
