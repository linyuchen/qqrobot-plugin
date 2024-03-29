import re
import time

import config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment, FriendMsg
from .browser_screenshot import search_baidu, ZhihuPreviewer, github_readme, wx_article, moe_wiki

zhihu_previewer = ZhihuPreviewer()

url_history = {}  # {"g群号": {"http://xxx": "最后一次获取时间戳"}}


def check_url_recent(qq: str, url: str) -> bool:
    now = time.time()
    if qq not in url_history:
        url_history[qq] = {}

    if url not in url_history[qq]:
        url_history[qq][url] = now
        return False
    if now - url_history[qq][url] > 5 * 60:
        url_history[qq][url] = now
        return False
    else:
        return True


@on_command("百度",
            param_len=1,
            desc="获取百度搜索结果截图",
            example="百度 猫娘",
            cmd_group_name="百度"
            )
def baidu(msg: GeneralMsg, params: list[str]):
    """
    百度搜索
    """
    img_path = search_baidu(params[0])
    msg.reply(MessageSegment.image_path(img_path))
    img_path.unlink()


@on_command("", cmd_group_name="知乎预览",
            desc="知乎链接获取预览图",
            example="https://www.zhihu.com/question/123456",
            auto_destroy=False
            )
def zhihu_preview(msg: GeneralMsg, params: list[str]):
    qq_id = msg.friend.qq if isinstance(msg, FriendMsg) else msg.group.qq
    if "//www.zhihu.com/question" in msg.msg:

        """
        怎样搭配才能显得腿长？ - 知乎
        https://www.zhihu.com/question/27830729/answer/49839659
        https://www.zhihu.com/question/27830729
        """
        # 匹配知乎问题链接
        question_url = re.findall(r"https?://www.zhihu.com/question/\d+", msg.msg)
        question_url = question_url[0] if question_url else None
        # 匹配知乎回答链接
        answer_url = re.findall(r"https?://www.zhihu.com/question/\d+/answer/\d+", msg.msg)
        answer_url = answer_url[0] if answer_url else None
        url = answer_url or question_url
        if url:
            if check_url_recent(qq_id, url):
                return
            img_path = zhihu_previewer.zhihu_question(url)
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(url), at=False, quote=False)
                img_path.unlink()

    elif "//zhuanlan.zhihu.com/p/" in msg.msg:
        zhuanlan_url = re.findall(r"https://zhuanlan.zhihu.com/p/\d+", msg.msg)
        zhuanlan_url = zhuanlan_url[0] if zhuanlan_url else None
        if zhuanlan_url:
            if check_url_recent(qq_id, zhuanlan_url):
                return
            img_path = zhihu_previewer.zhihu_zhuanlan(zhuanlan_url)
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(zhuanlan_url),
                          at=False, quote=False)
                img_path.unlink()


@on_command("", cmd_group_name="github预览",
            desc="github链接获取README预览图",
            example="https://github.com/linyuchen/qqrobot-plugin",
            auto_destroy=False,
            )
def github_preview(msg: GeneralMsg, params: list[str]):
    if "//github.com/" in msg.msg:
        # 获取github链接
        url = re.findall(r"https://github.com/[a-zA-Z0-9_/-]+", msg.msg)
        url = url[0] if url else None
        if url:
            qq_id = msg.friend.qq if isinstance(msg, FriendMsg) else msg.group.qq
            if check_url_recent(qq_id, url):
                return
            img_path = github_readme(url, http_proxy=config.get_config("GFW_PROXY"))
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(url), at=False, quote=False)
                img_path.unlink()


@on_command("萌娘百科", param_len=1,
            desc="萌娘百科搜索预览图",
            example="萌娘百科 猫娘",
            )
def moe_wiki_cmd(msg: GeneralMsg, params: list[str]):
    msg.reply("正在为您搜索萌娘百科...")
    img_path = moe_wiki(params[0])
    if img_path:
        msg.reply(MessageSegment.image_path(img_path))
        img_path.unlink()


@on_command("", cmd_group_name="微信文章预览",
            desc="微信文章链接获取预览图",
            example="https://mp.weixin.qq.com/s/xa33f",
            auto_destroy=False
            )
def wx_article_preview(msg: GeneralMsg, params: list[str]):
    if "mp.weixin.qq.com" in msg.msg:
        # 获取github链接
        url = re.findall(r"https://mp.weixin.qq.com/s[/a-zA-Z0-9%?&=_-]+", msg.msg)
        url = url[0] if url else None
        if url:
            qq_id = msg.friend.qq if isinstance(msg, FriendMsg) else msg.group.qq
            if check_url_recent(qq_id, url):
                return
            img_path = wx_article(url)
            if img_path:
                msg.reply(MessageSegment.image_path(img_path) + MessageSegment.text(url), at=False, quote=False)
                img_path.unlink()
