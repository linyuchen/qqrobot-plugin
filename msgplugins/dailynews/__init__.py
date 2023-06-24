from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .news import get_news2


class ExamplePlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("每日新闻", param_len=0, alias=["今日新闻", "今天新闻", "早报"]).az(msg.msg):
            img_path = get_news2()
            if img_path:
                msg.reply(MessageSegment.image_path(img_path))
                msg.destroy()
