import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from . import bilicard


class BiliCardPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        msg_text = msg.msg
        b32_url = bilicard.check_is_b23(msg_text)
        if b32_url:
            msg.pause()  # 因为b32链接有可能是不是视频链接，比如是专栏，用于被其他插件使用，所以这里先暂停
            msg_text = bilicard.b32_to_bv(b32_url[0])

        bvid = bilicard.get_bv_id(msg_text)
        avid = bilicard.get_av_id(msg_text)
        if bvid or avid:
            msg.destroy()
            msg.resume()
            # text = gen_text(bvid)
            # if text:
            #     msg.reply(text)
            msg.destroy()
            video_info = bilicard.get_video_info(bvid, avid)
            img_path = bilicard.gen_image(video_info)
            summary = bilicard.get_video_summary_by_ai(video_info["aid"], video_info["cid"])
            summary = "AI总结：" + summary if summary else ""
            url = f"https://www.bilibili.com/video/BV{bvid}" if bvid else f"https://www.bilibili.com/video/av{avid}"
            if img_path:
                reply_msg = MessageSegment.image_path(img_path) + \
                            MessageSegment.text("简介：" + video_info["desc"] + "\n\n" + summary +
                                                "\n\n" + url)
                msg.reply(reply_msg)
                os.remove(img_path)

        else:
            # 不是视频链接，所以这里要去掉暂停状态，让其他插件可以使用
            msg.resume()