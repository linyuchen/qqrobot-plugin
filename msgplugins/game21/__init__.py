# coding=UTF8

from ..msgcmd import cmdaz
from .import game21point
from ..superplugin import GroupPointAction
from qqsdk.message import MsgHandler, GroupMsg
CMD = cmdaz.CMD
Game21 = game21point.Game


class Game(GroupPointAction, Game21):

    def __init__(self):
        GroupPointAction.__init__(self)
        Game21.__init__(self)
        self.currency = "活跃度"


# 新建个事件类，继承于MsgEvent
class Game21Plugin(MsgHandler):
    __doc__ = u"""
    群游戏：21点
    """
    name = "21点"
    cmd_name = "21点"
    desc = "21点棋牌游戏"
    example = "21点 100, 100为下注点数"
    bind_msg_types = (GroupMsg, )

    def __init__(self, **kwargs):

        super(Game21Plugin, self).__init__(**kwargs)

        self.groupInstances = {}  # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def get_game_instance(self, group_qq):
        return self.groupInstances.setdefault(group_qq, Game())

    def handle(self, msg: GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.group_member

        game = self.get_game_instance(group_qq)
        cmd_start = CMD("21点")
        cmd_start_param = CMD("21点", param_len=1)
        cmd_update = CMD("21点换牌")
        result = ""
        param = ""
        if cmd_start.az(msg.msg):
            param = "100"
        elif cmd_start_param.az(msg.msg):
            param = cmd_start_param.get_param_list()[0]
        if param:
            msg.destroy()
            result += game.start_game(group_qq, member.qq, member.get_name(), param, msg.reply)
            result += "\n\n发送“21点换牌”可以换牌，换牌需要下注的十分之一费用\n"
        elif cmd_update.az(msg.msg):
            msg.destroy()
            result += game.update_poker_list(group_qq, member.qq, member.get_name())
 
        if result:
            msg.reply(result)

