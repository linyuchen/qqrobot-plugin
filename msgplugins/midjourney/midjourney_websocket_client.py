import random
from copy import deepcopy
from datetime import datetime

from common.discord_client.discord_client import DiscordWebsocketClientBase, Message
from common.logger import logger
from .midjourney_client import MidjourneyClientBase, Task, TaskCallbackResponse, TaskType


class MidjourneyClient(MidjourneyClientBase, DiscordWebsocketClientBase):

    def __init__(self, token: str, channel_id: str, guild_id: str, proxy: str = None):
        DiscordWebsocketClientBase.__init__(self, token, channel_id, guild_id, proxy)
        MidjourneyClientBase.__init__(self, proxy)

    def __post_interaction(self, task: Task, payload: dict):
        try:
            super()._post_interaction(payload)
        except Exception as e:
            with self._lock:
                self.tasks.remove(task)
                task.callback(TaskCallbackResponse(task=task, error=f'提交任务失败 {e}'))

    def _action_continue(self, msg: Message):
        custom_id = msg.origin_data["components"][0]["components"][0]["custom_id"]
        payload = {
            "type": 3,
            "nonce": f"{random.randint(1134276220909715456, 1144276220909715456)}",
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 64,
            "message_id": msg.msg_id,
            "application_id": "936929561302675456",
            "session_id": "cc1789f5fba05b9af65c7f0c6033986c",
            "data": {
                "component_type": 2,
                "custom_id": custom_id
            }
        }
        super()._post_interaction(payload)

    def __post_draw(self, task: Task):
        payload = {
            "channel_id": self.channel_id,  # 当前频道浏览器上方有
            "guild_id": self.guild_id,  # 当前频道浏览器上方有
            "session_id": "34a0d78eb9e624d31ac63cff92c2687b",  # 固定即可
            "application_id": "936929561302675456",  # 固定的
            "type": 2,
            'data': {
                "version": "1166847114203123795",  # 固定的
                "id": "938956540159881230",  # command id，固定的
                'name': 'imagine',
                'type': 1,
                'options': [{'type': 3, 'name': 'prompt', 'value': task.prompt}],
                'attachments': []}
        }
        self.__post_interaction(task, payload)

    def __post_upscale(self, task: Task):
        filename = task.reply_msg.attachment_urls[0].split("_")[-1]
        filename = filename.replace(".png", "").split("?")[0]
        payload = {
            "type": 3,
            "nonce": random.randint(1142187534726463488, 1143187534726463488),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 0,
            "message_id": task.reply_msg.msg_id,
            "application_id": "936929561302675456",
            "session_id": "b74a9d0a15349bbc72fd969edecab7e7",
            "data": {
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample::{task.upscale_index}::{filename}",
            }
        }
        self.__post_interaction(task, payload)

    def _handle_new_task(self, task: Task):
        """
            提交新的任务，用http接口
            """
        if task.task_type == TaskType.DRAW:
            self.__post_draw(task)
        elif task.task_type == TaskType.UPSCALE:
            self.__post_upscale(task)

    def upscale(self, reply_task: TaskCallbackResponse, index: int):
        task = deepcopy(reply_task.task)
        task.task_type = TaskType.UPSCALE
        task.datetime = datetime.now(tz=self.local_timezone)
        task.upscale_index = index
        task.reply_msg = deepcopy(reply_task.reply_msg)
        self._putted_tasks.put(task)

    def _listen_msg(self):
        pass

    def _handle_new_msg(self, reply_msg: Message):
        if reply_msg.channel_id != self.channel_id:
            return
        return super()._handle_new_msg(reply_msg)
