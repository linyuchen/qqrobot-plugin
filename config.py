import json
from pathlib import Path

config_path = Path(__file__).parent / "config.json"


def save_config():
    with config_path.open("w", encoding="utf-8") as fw:
        json.dump(config_data, fw, indent=4, ensure_ascii=False)


config_data = {
    "GFW_PROXY": "http://192.168.1.4:7890",
    "ONEBOT_HTTP_API": "http://localhost:3000",
    "MIRAI_HTTP_API": "http://localhost:8080",
    "MIRAI_HTTP_API_VERIFY_KEY": "1234567890",
    "QQ": [721011692],
    "ADMIN_QQ": [379450326],  # 机器人主人的QQ号,
    "LISTEN_PORT": 5000,
    "SEND2TIM": False,
    "SEND2TIM_HTTP_API": "http://localhost:8088/",
    "SD_HTTP_API": "http://192.168.1.4:7860",
    "VITS_GRADIO_SPACE": "zomehwh/vits-uma-genshin-honkai",
    "BV2_FASTAPI": "http://localhost:5001",
    "BING_AI_API": "http://localhost:9000",
    "TTS_ENABLED": True,
    "MJ_DISCORD_TOKEN": "",
    "MJ_DISCORD_CHANNEL_ID": "",
    "MJ_DISCORD_GUILD_ID": "",
    "MJ_DISCORD_CHANNEL_URL": "",
    "BAIDU_TRANSLATE_APPID": "",
    "BAIDU_TRANSLATE_SECRETKEY": "",
    "TUSI_TOKENS": [

    ],
    "CHATGPT": [
        {
            "key": "API_KEY",
            "api": "https://api.openai.com/v1",
            "model": "gpt-3.5-turbo-0613"
        }
    ]
}

if config_path.exists():
    with config_path.open("r", encoding="utf-8") as fr:
        config_data.update(json.load(fr))
    save_config()
else:
    save_config()


def __getattr__(name):
    return config_data.get(name)


def __setattr__(name, value):
    config_data[name] = value
    save_config()


def get_config(key: str, default=None):
    result = config_data.get(key, default)
    match key:
        case "ADMIN_QQ":
            result = list(map(str, result))
    return result


def set_config(key: str, value):
    __setattr__(key, value)
