# coding=UTF8
import importlib
import os
import pathlib
import sys
import traceback
from abc import ABCMeta, abstractmethod

from common.logger import logger
from qqsdk import entity
from qqsdk.eventlistener import EventListener
from qqsdk.message import MsgHandler, BaseMsg
from qqsdk.message.segment import MessageSegment


class QQClientBase(EventListener, metaclass=ABCMeta):

    def __init__(self):
        super(QQClientBase, self).__init__()
        self.qq_user = entity.QQUser(friends=[], groups=[])
        self.online = True
        self.msg_handlers = self.setup_plugins()
        self.msg_history: list[BaseMsg] = []
        self.sent_group_msg_ids: dict[str, list[str]] = {}  # key group qq, value [msg id,...]

    def setup_plugins(self) -> list[MsgHandler]:
        plugins_path = pathlib.PurePath(__file__).parent.parent / "msgplugins"
        sys.path.append(str(plugins_path))
        for p in os.listdir(plugins_path):
            module_path = pathlib.Path(plugins_path) / p
            if module_path.is_file() and module_path.suffix == ".py" and module_path.stem != "__init__":
                module_name = module_path.stem
            elif (module_path / "__init__.py").exists():
                module_name = p
            else:
                continue
            try:
                importlib.import_module(f".{module_name}", "msgplugins")
            except Exception as e:
                logger.error(f"加载插件{module_name}时出现异常：{e}, \n{traceback.format_exc()}")
                continue
        for i in MsgHandler.__subclasses__():
            i(qq_client=self)
        self.msg_handlers = MsgHandler.instances
        # 按照优先级排序
        self.msg_handlers.sort(key=lambda x: x.priority, reverse=True)
        return self.msg_handlers

    def start(self) -> None:
        super().start()

    def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        content_str = content
        if isinstance(content, MessageSegment):
            content_str = content.get_text()
        if "出脚本" in content_str:
            return

        self._send_msg(qq, content, is_group)

    @abstractmethod
    def _send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        pass

    def send_mass_group(self, content: str | MessageSegment):
        """
        群发消息
        """
        for group in self.qq_user.groups:
            self._send_msg(group.qq, content, is_group=True)

    @abstractmethod
    def get_friends(self) -> list[entity.Friend]:
        """
        获取好友，结果将放在self.qq_user.friends里面
        """

    @abstractmethod
    def get_groups(self) -> list[entity.Group]:
        """
        结果保存在 self.qq_user.groups
        """

    @abstractmethod
    def get_msg(self, data: dict):
        raise NotImplementedError

    def __get_group(self, group_qq: str) -> entity.Group:
        result = list(filter(lambda g: str(g.qq) == str(group_qq), self.qq_user.groups))
        return result and result[0] or None

    def get_group(self, group_qq: str) -> entity.Group:
        group = self.__get_group(group_qq)
        if not group:
            self.get_groups()
            group = self.__get_group(group_qq)
        return group

    def __get_friend(self, qq: str) -> entity.Friend | None:
        result = list(filter(lambda f: f.qq == qq, self.qq_user.friends))
        return result and result[0] or None

    def get_friend(self, qq: str) -> entity.Friend:
        friend = self.__get_friend(qq)
        if not friend:
            self.get_friends()
            friend = self.__get_friend(qq)
        return friend

    def add_msg(self, msg: BaseMsg):
        self.msg_history.append(msg)
        super().add_msg(msg)

    def get_history_msg(self, msg_id: str | int):
        for msg in self.msg_history:
            if str(getattr(msg, "msg_id")) == str(msg_id):
                return msg
        return None

    def recall_msg(self, msg_id: str):
        pass