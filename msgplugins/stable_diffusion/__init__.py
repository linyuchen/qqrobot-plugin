import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sd import txt2img, get_models, set_model


class SDPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True
    desc = "发送 画图+空格+描述 进行AI画图\n" + \
        "发送 查看画图模型 获取模型列表\n发送 设置画图模型+空格+模型名 设置模型"

    def handle(self, msg: GroupMsg | FriendMsg):
        get_models_cmd = CMD("查看画图模型", alias=["画图模型"], param_len=0)
        set_model_cmd = CMD("设置画图模型", alias=["画图模型"], param_len=1, sep=" ")
        draw_cmd = CMD("画图", alias=["sd", "画画", "绘图", "画一个"], param_len=1, sep=" ")
        draw_hd_cmd = CMD("画图hd", param_len=1, sep=" ")
        draw_txt = ""
        if get_models_cmd.az(msg.msg):
            msg.reply(get_models())
            msg.destroy()
            return
        elif set_model_cmd.az(msg.msg):
            model_name = set_model_cmd.get_original_param().strip()
            msg.reply(set_model(model_name))
            msg.destroy()
        elif draw_cmd.az(msg.msg) or draw_hd_cmd.az(msg.msg):
            draw_txt = draw_cmd.get_original_param()
        if draw_txt:
            if draw_hd_cmd.az(msg.msg):
                width = 1024
                height = 768
            else:
                width = 600
                height = 800
            msg.reply("正在努力画画中（吭哧吭哧~），请稍后...")
            image_path = txt2img(draw_txt, width, height)
            reply_msg = MessageSegment.image_path(image_path)
            msg.reply(reply_msg)
            os.remove(image_path)
            msg.destroy()
            return



