import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .cmdaz import CMD


class GlobalPluginManager(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        qq = msg.group_member.qq if isinstance(msg, GroupMsg) else msg.friend.qq
        if qq != str(config.ADMIN_QQ):
            return
        if CMD("全局插件", alias=["查看全局插件"]).az(msg.msg):
            res = "全局插件列表\n"
            for plugin in config.plugins:
                summary = config.plugins[plugin].get('summary', '')
                res += f"插件名:{plugin}: {summary}, {config.plugins[plugin].get('enabled', True)}\n"
            msg.reply(res)
            msg.destroy()
            return
        cmd_open = CMD("开启全局插件", param_len=1, sep="")
        cmd_close = CMD("关闭全局插件", param_len=1, sep="")
        enabled = True
        plugin_name = ""
        if cmd_open.az(msg.msg):
            cmd_param = cmd_open.get_param_list()
            plugin_name = cmd_param[0]
        elif cmd_close.az(msg.msg):
            cmd_param = cmd_close.get_param_list()
            plugin_name = cmd_param[0]
            enabled = False
            if plugin_name == "global_plugin_manager":
                msg.reply("不能关闭全局插件管理器")
                msg.destroy()
        else:
            return

        if plugin_name not in config.plugins:
            msg.reply(f"插件名有误，插件【{plugin_name}】不存在")
            msg.destroy()
            return
        config.plugins[plugin_name]["enabled"] = enabled
        config.save_config()
        msg.reply(f"已{'开启' if enabled else '关闭'}插件{plugin_name}")
        msg.destroy()