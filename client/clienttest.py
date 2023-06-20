from qqsdk.entity import Group, GroupMember
from qqsdk.message import GroupMsg
from qqsdk.message.segment import MessageSegment
from qqsdk.qqclient import QQClientBase

TEST_GROUP_QQ = "123"
TEST_GROUP_NAME = "test group"
TEST_GROUP_MEMBER_QQ = "456"
TEST_GROUP_MEMBER_NAME = "test"


class ClientTest(QQClientBase):
    TEST_GROUP_MEMBER = GroupMember(qq=TEST_GROUP_MEMBER_QQ, nick=TEST_GROUP_MEMBER_NAME)
    TEST_GROUP = Group(qq=TEST_GROUP_QQ, name=TEST_GROUP_NAME,
                       members=[TEST_GROUP_MEMBER])

    def __init__(self):
        super().__init__()
        self.qq_user.groups.append(self.TEST_GROUP)

    # def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
    #     print(content)

    def get_msg(self):
        group_msg = GroupMsg(group=self.TEST_GROUP, group_member=self.TEST_GROUP_MEMBER,
                             msg=str(input("请输入消息:")))
        group_msg.reply = print
        self.add_msg(group_msg)

    def start(self) -> None:
        super().start()
        while True:
            self.get_msg()


if __name__ == "__main__":
    client = ClientTest()
    client.start()