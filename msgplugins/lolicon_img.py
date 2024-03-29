import tempfile
from pathlib import Path

import requests

from common.utils.nsfw_detector import nsfw_detect
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("来点色图", alias=("色图", "涩图", "来点涩图"),
            desc="你懂的,后面可以跟关键词指定图片标签",
            example="来点色图 或者 来点色图 黑丝",
            param_len=-1, is_async=True, cmd_group_name="来点色图")
def lolicon_img(msg: GeneralMsg, msg_params: list[str]):
    try:
        api_url = "https://api.lolicon.app/setu/v2?size=regular"
        if msg_params:
            api_url += "&tag=" + "&tag=".join(msg_params)
        data = requests.get(api_url).json()["data"]
        img_url = data[0]["urls"].get("regular")
        if not img_url:
            return msg.reply("图片获取失败")
        img_data = requests.get(img_url).content
        img_path = tempfile.mktemp(".png")
        img_path = Path(img_path)
        with open(img_path, "wb") as f:
            f.write(img_data)
        if nsfw_detect(img_path):
            img_path.unlink()
            return msg.reply("图片违规，已删除~")
    except Exception as e:
        return msg.reply(f"图片获取失败 {e}")

    msg.reply(MessageSegment.image_path(img_path))
    img_path.unlink()
