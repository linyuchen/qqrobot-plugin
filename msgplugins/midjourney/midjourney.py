import asyncio
import re
import tempfile
from pathlib import Path
from typing import Callable

import aiohttp
import pandas as pd
from retry import retry

default_json = {
    "channelid": "1127887388648153121",
    "authorization": "MTAxMjQ5NTUxMTA2MTc5NDg0Ng.G0Cus3.1YfxrcY7KGqsx8_KhSUx91c2yGUNWpVyl8bdok",
    "application_id": "936929561302675456",
    "guild_id": "1127887388648153118",
    "session_id": "e7de53b801a3670887aa7cfb36d68de0",
    "version": "1118961510123847772",
    "id": "938956540159881230",
    "flags": "--v 5",
    # "http://127.0.0.1:10809"
    "proxy": "http://127.0.0.1:7890",
    "timeout": 120
}


class Sender:

    def __init__(self):

        self.sender_initializer()

    def sender_initializer(self):

        params = default_json

        self.channelid = params['channelid']
        self.authorization = params['authorization']
        self.application_id = params['application_id']
        self.guild_id = params['guild_id']
        self.session_id = params['session_id']
        self.version = params['version']
        self.id = params['id']
        self.flags = params['flags']
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None

    async def send(self, prompt):
        header = {
            'authorization': self.authorization
        }

        # prompt = prompt.replace('_', ' ')
        # prompt = " ".join(prompt.split())
        # prompt = re.sub(r'[^a-zA-Z0-9\s\-]+', '', prompt)
        prompt = prompt.lower()

        payload = {'type': 2,
                   'application_id': self.application_id,
                   'guild_id': self.guild_id,
                   'channel_id': self.channelid,
                   'session_id': self.session_id,
                   'data': {
                       'version': self.version,
                       'id': self.id,
                       'name': 'imagine',
                       'type': 1,
                       'options': [{'type': 3, 'name': 'prompt', 'value': prompt}],
                       'attachments': []}
                   }

        async with aiohttp.ClientSession() as session:
            retry = 3
            while retry >= 0:
                try:
                    async with session.post('https://discord.com/api/v9/interactions', json=payload, headers=header,
                                            proxy=self.proxy) as resp:
                        if resp.status == 204:
                            break

                        print(".", end="")
                except Exception as e:
                    print(e)
                retry -= 1

                if retry < 0:
                    return None

        # print(r.headers)
        # print(r.text)

        # print('prompt [{}] successfully sent!'.format(prompt))
        # prompt = prompt.replace(" ", "_")

        # 多个空格变一个空格
        prompt = re.sub(r'\s+', ' ', prompt)
        return prompt


class Receiver:

    def __init__(self,
                 prompt
                 ):

        self.prompt = prompt

        self.sender_initializer()

        self.df = pd.DataFrame(columns=['prompt', 'url', 'filename', 'is_downloaded'])

    def sender_initializer(self):

        params = default_json
        self.channelid = params['channelid']
        self.authorization = params['authorization']
        self.headers = {'authorization': self.authorization}
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None
        self.timeout = params['timeout']

    @retry(tries=3)
    async def retrieve_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={10}',
                                   headers=self.headers, proxy=self.proxy) as response:
                jsonn = await response.json()
        return jsonn

    async def collecting_results(self):
        # tmp_json = {
        #     "code": 0,
        #     "url": ""
        # }

        message_list = await self.retrieve_messages()
        self.awaiting_list = pd.DataFrame(columns=['prompt', 'status'])
        for message in message_list:
            try:
                # 如果这条消息是由"Midjourney Bot"发送的，并且包含双星号（**），则它是一个需要处理的请求
                # print(message)
                if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
                    # print("找到了消息")
                    if len(message['attachments']) > 0:
                        # 如果该消息包含图像附件，则获取该附件的URL和文件名，并将其添加到df DataFrame中
                        if (message['attachments'][0]['filename'][-4:] == '.png') or (
                                '(Open on website for full quality)' in message['content']):
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            # url = message['attachments'][0]['url']
                            url = message['attachments'][0]['proxy_url'] + "?width=1024&height=1024"
                            filename = message['attachments'][0]['filename']

                            # print(f"prompt2=[{prompt}]")

                            # 判断prompt是否匹配
                            if self.prompt == prompt:
                                # DataFrame的索引是消息ID，因此我们可以根据消息ID来确定哪个请求与哪个消息相对应
                                if id not in self.df.index:
                                    self.df.loc[id] = [prompt, url, filename, 0]
                                    # print("filename=" + filename)
                                    # print("url=" + url)
                                    # tmp_json["url"] = url
                                    return url
                        # 如果消息中没有图像附件，则将该请求添加到awaiting_list DataFrame中，等待下一次检索。
                        else:
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                                try:
                                    status = re.findall("(\w*%)", message['content'])[0]
                                except:
                                    status = 'unknown status'
                            self.awaiting_list.loc[id] = [prompt, status]

                    else:
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        if '(Waiting to start)' in message['content']:
                            status = 'Waiting to start'
                        self.awaiting_list.loc[id] = [prompt, status]
            except Exception as e:
                print(e)

        return None

    async def check_result(self):
        for i in range(int(self.timeout / 3)):
            try:
                ret = await self.collecting_results()
            except Exception as e:
                print(e)
                continue
            if ret != None:
                return ret
            # for i in self.df.index:
            #         return self.df.loc[i].url
            # 睡眠3s
            await asyncio.sleep(3)
        return None

    async def download_img(self, url) -> Path:
        async with aiohttp.ClientSession() as session:
            for i in range(10):
                try:
                    async with session.get(url, headers=self.headers, proxy=self.proxy) as response:
                        data = await response.read()
                        tmp_path = tempfile.mktemp(".png")
                        open(tmp_path, 'wb').write(data)
                        return Path(tmp_path)
                except Exception as e:
                    print(e)


async def __send(prompt, callback: Callable[[Path], None]):
    sender = Sender()
    prompt = await sender.send(prompt)

    # print(f"prompt=[{prompt}]")

    receiver = Receiver(prompt)
    result = await receiver.check_result()

    try:
        if result is not None:
            print(f"result=[{result}]")
            result = await receiver.download_img(result)
            callback(result)
    except Exception as e:
        print(e)
        return str(e)


def draw(prompt: str, callback: Callable[[Path], None]):
    return asyncio.run(__send(prompt, callback))