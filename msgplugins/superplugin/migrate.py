# -*- coding: UTF8 -*-

import django_setup
import os
django_setup.sys.path.append(os.path.dirname(django_setup.CURRENT_PATH))
from sqliteclient import Sqlite
from group.models import GroupUser, SignRecord
from account.models import MyUser
from django.utils import timezone

sqlite = Sqlite("group_manager.db")
rpg_sqlite = Sqlite("rpgdata.db")


def migrate_point():
    # 处理群活跃度
    t_name = "t_point"
    values = sqlite.get_value(table_name=t_name, key_list=["group_qq", "member_qq", "name", "point"])
    for value in values:
        group_qq = value[0]
        qq = value[1]
        nick = value[2]
        if not nick:
            nick = u"匿名"
        point = value[3]
        point = "%d" % eval(point)
        # user = MyUser.get_user(qq)
        group_user = GroupUser.get_user(group_qq, qq)
        if point == group_user.point:
            continue
        group_user.nick = nick
        group_user.point = point        
        if not point.isdigit() and not point.startswith("-"):
            print(point, "%d" % eval(point))
        group_user.save()


def migrate_sign():
    # 处理群签到
    t_name = "t_sign"
    values = sqlite.get_value(table_name=t_name, key_list=["group_qq", "member_qq", "continuous", "total", "sign_date"])
    for value in values:
        group_qq = value[0]
        qq = value[1]
        continuous = value[2]
        total = value[3]
        last_date = value[4]
        group_user = GroupUser.get_user(group_qq, qq)
        group_user.sign_continuous = continuous
        group_user.total_sign = total
        group_user.save()
        SignRecord(user=group_user, time=timezone.datetime.strptime(last_date, "%Y-%m-%d"), add_point="0").save()


def migrate_rpg():
    # 处理RPG游戏的数据
    t_name = "t_person"
    values = rpg_sqlite.get_value(table_name=t_name, key_list=["gold", "tag"])
    for value in values:
        gold = value[0]
        gold = "%d" % eval(gold)
        qq = value[1]
        user = MyUser.get_user(qq)
        if gold == user.point:
            continue
        user.point = gold
        user.save()


def migrate_clear_chance():
    t_name = "t_clear_chance"
    values = sqlite.get_value(table_name=t_name, key_list=["member_qq", "chance"])
    for value in values:
        qq = value[0]
        chance = value[1]
        print(qq, chance)
        user = MyUser.get_user(qq)
        user.clear_point_chance = chance
        user.save()


if __name__ == "__main__":
    # migrate_point()
    # migrate_sign()
    # migrate_rpg()
    migrate_clear_chance()
