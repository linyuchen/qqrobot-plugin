# coding=UTF8

import asyncio
from qqsdk.eventlistener import EventListener
from archive.client.nonebot import QQClient
from qqsdk.message.friendmsg import FriendMsg
from qqsdk.message.groupmsg import GroupMsg
from aiocqhttp import Event


# 全局唯一
qq_client = QQClient()
qq_client.start()


# @on_notice()
# async def handle_request(session: NoticeSession):
#     if session.event.sub_type == "invite":
#         await qq_client.bot.set_group_add_request(sub_type="invite", approve=False, reason="联系Q 379450326")


@qq_client.bot.on_message
async def msg_handle(event: Event):
    sub_type = event.sub_type
    msg = event.raw_message
    loop = asyncio.get_event_loop()
    if sub_type == "friend":
        friend = qq_client.get_friend(str(event.user_id))
        msg = FriendMsg(friend=friend, msg=msg)
        msg.reply = lambda _msg: asyncio.run_coroutine_threadsafe(qq_client.send_msg(friend.qq, _msg), loop)
        qq_client.add_msg(msg)

    elif sub_type == "normal" or sub_type == "anonymous":
        group = qq_client.get_group(str(event.group_id))
        msg = GroupMsg(group=group, msg=msg, group_member=group.get_member(str(event.user_id)))
        msg.reply = lambda _msg: asyncio.run_coroutine_threadsafe(qq_client._send_msg(group.qq, _msg, is_group=True),
                                                                  loop)

        qq_client.add_msg(msg)