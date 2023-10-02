# lora的翻译和绑定

lora = {
    "op": {
        "多莉": "dorirdef",
        "多莉2": "dorirnd",
        "瑶瑶": "yaoyaordef",
        "瑶瑶2": "yaoyaornd",
        "安柏披萨": "amberpizza",
        "安柏五星": "amber5star",
        "安柏": "amberrnd",
        "芭芭拉": "barbaradef",
        "芭芭拉2": "barbararnd",
        "芭芭拉夏日": "barbarasum",
        "北斗": "beidoudef",
        "北斗2": "beidournd",
        "迪希亚": "dehyarnd",
        "迪奥娜": "dionadef",
        "迪奥娜2": "dionarnd",
        "优菈": "euladef",
        "优菈2": "eularnd",
        "菲谢尔": "fischldef",
        "菲谢尔2": "fischlrnd",
        "菲谢尔3": "fischlein",
        "甘雨": "ganyudef",
        "甘雨2": "ganyurnd",
        "胡桃": "hutaodef",
        "胡桃2": "hutaornd",
        "琴": "jeanrnd",
        "琴2": "jeangunnhildr",
        "琴海风": "jeanseabreeze",
        "神里绫华": "kamisatoayakadef",
        "神里绫华2": "kamisatoayakarnd",
        "神里绫华春节": "kamisatoayakaspring",
        "刻晴": "keqingdef",
        "刻晴2": "keqingopulent",
        "可莉": "kleedef",
        "可莉2": "kleernd",
        "珊瑚宫心海": "kokomidef",
        "珊瑚宫心海2": "kokomirnd",
        "九条裟罗": "kujousaradef",
        "九条裟罗2": "kujousararnd",
        "久岐忍": "kukishinobudef",
        "久岐忍2": "kukishinoburnd",
        "丽莎": "lisadef",
        "丽莎2": "lisarnd",
        "荧": "luminedef",
        "荧2": "luminernd",
        "莫娜": "monadef",
        "莫娜2": "monarnd",
        "莫娜3": "monastarpact",
        "纳西妲": "nahidadef",
        "纳西妲2": "nahidarnd",
        "尼露": "niloudef",
        "尼露2": "nilournd",
        "凝光": "ningguangdef",
        "凝光2": "ningguangrnd",
        "凝光3": "ningguangorc",
        "诺艾尔": "noelledef",
        "诺艾尔2": "noellernd",
        "诺艾尔KFC": "noellekfc",
        "七七": "qiqidef",
        "七七2": "qiqirnd",
        "雷电将军": "raidenshogundef",
        "雷电将军2": "raidenshogunrnd",
        "罗莎莉亚": "rosariadef",
        "罗莎莉亚2": "rosariarnd",
        "罗莎莉亚自由精神": "rosariafreespirit",
        "早柚": "sayudef",
        "早柚2": "sayund",
        "申鹤": "shenhedef",
        "申鹤2": "shenhernd",
        "砂糖": "sucrosedef",
        "砂糖2": "sucrosernd",
        "香菱": "xianglingdef",
        "香菱2": "xianglingrnd",
        "八重樱": "yaemikodef",
        "八重樱2": "yaemikornd",
        "烟绯": "yanfeidef",
        "烟绯2": "yanfeirnd",
        "夜兰": "yelandef",
        "夜兰2": "yelanrnd",
        "宵宫": "yoimiyadef",
        "宵宫2": "yoimiyarnd",
        "云堇": "yunjindef",
        "云堇2": "yunjinnd",
        "坎蒂丝": "candacedef",
        "坎蒂丝2": "candacend",
        "柯莱": "colleidef",
        "迪希雅": "dehyadef",
        "莱依拉": "laylardef",
        "莱依拉2": "laylarnd",
        "珐露珊": "faruzandef",
        "珐露珊2": "faruzannd",
        "辛焱": "xinyandef",
        "辛焱2": "xinyanrnd",
    },
    "laughing_finger": {
        "笑指": "laughing_finger",
    }
}


def get_lora() -> str:
    result = ""
    for lora_name in lora:
        result += f"{lora_name}:\n" + "，".join(lora[lora_name].keys()) + "\n\n"

    return result



def trans_lora(prompt: str) -> str:
    lora_prompt = []
    new_prompt = []
    for prompt in prompt.split(","):
        for key in lora:
            lora_keys = list(lora[key].keys())
            lora_keys.sort(key=len, reverse=True)
            for lora_key in lora_keys:
                lora_word = lora[key][lora_key]
                if lora_key in prompt:
                    if lora_word not in lora_prompt:
                        lora_prompt.append(f"<lora:{key}>")
                    prompt = prompt.replace(lora_key, lora_word + ",")

        new_prompt.append(prompt)

    return ",".join(lora_prompt) + "," + ",".join(new_prompt)


if __name__ == '__main__':
    print(trans_lora("刻晴泳装,水里"))
