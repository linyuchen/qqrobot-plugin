from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg, MessageSegment
from .genshinvoice_top import tts, speakers


@on_command("tts列表", param_len=0,
            desc="获取文字转语音角色列表",
            cmd_group_name="tts")
def tts_list(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("语音可用的人物列表:\n" + ", ".join(speakers))


@on_command("tts", param_len=-1,
            desc="文字转语音, 可以指定角色声音",
            example="tts 你好 或 tts 可莉 你好",
            cmd_group_name="tts")
def tts_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    default_speaker = "可莉"
    if len(params) == 0:
        msg.reply("请输入要转换的文字")
        return

    text = params[0]
    speaker = default_speaker
    if len(params) > 1:
        if params[0] in speakers:
            speaker = params[0]
            text = " ".join(params[1:])
        else:
            text = " ".join(params)

    max_len = 200
    if len(text) > max_len:
        msg.reply(f"文字长度超过{max_len}字")
        return
    try:
        voice_path = tts(text, speaker)
    except Exception as e:
        msg.reply(f"语音转换失败: {e}")
        return
    msg.reply(MessageSegment.voice_path(voice_path))
