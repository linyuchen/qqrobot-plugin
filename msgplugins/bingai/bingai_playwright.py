import queue
import tempfile
import threading
import time
from dataclasses import dataclass
from typing import Callable

from playwright.sync_api import sync_playwright

CHROME_DATA_DIR = tempfile.gettempdir() + "/playwright_chrome_data_bingai"


class BingAIPlayWright:

    def __init__(self, proxy: str = "", headless=False):
        self.timeout = 90
        p = sync_playwright().start()
        self.browser = p.chromium.launch_persistent_context(
            CHROME_DATA_DIR,
            headless=headless,
            proxy={
                "server": proxy,
            } if proxy else None)
        self.page = self.browser.new_page()
        url = "https://www.bing.com/chat?cc=us"
        try:
            self.page.goto(url, timeout=30000)
        except Exception as e:
            error_msg = f"{e}"
        # self.page.pause()
        self.question_num = 0

    def send_msg(self, msg: str):
        if not self.page.query_selector("textarea").is_enabled():
            self.page.click("button[aria-label='新主题']")
            time.sleep(1)
        self.page.fill("textarea", msg)
        self.page.click("div[class='control submit']")
        self.question_num += 1

    @property
    def is_responding(self) -> bool:
        responding = self.page.query_selector("#stop-responding-button").is_enabled()
        return responding

    def get_msg(self):
        used_time = 0
        while self.is_responding:
            time.sleep(0.5)
            used_time += 0.5
            if used_time > self.timeout:
                return "网络超时了~"
        # css选择器 选择ai的文本回复 "cib-message[source='bot'][type='text'] .ac-textBlock"
        replies = self.page.query_selector_all("cib-message[source='bot'][type='text'] .ac-textBlock")
        last_reply = replies[-1]
        # 移除里面的sup标签
        last_reply.evaluate("el => el.querySelectorAll('sup').forEach(e => e.remove())")
        return last_reply.inner_text()


@dataclass
class BinAITask:
    question: str
    reply_callback: Callable[[str], None]


class BinAITaskPool(threading.Thread):
    def __init__(self, proxy: str = "", headless=True):
        self.proxy = proxy
        self.headless = headless
        super().__init__(daemon=True)
        self.task_queue = queue.Queue()

    def put_question(self, task: BinAITask):
        self.task_queue.put(task)

    def run(self):
        bing = BingAIPlayWright(proxy=self.proxy, headless=self.headless)
        while True:
            task = self.task_queue.get()
            try:
                bing.send_msg(task.question)
            except Exception as e:
                reply_text = f"发生了错误：{e}"
            else:
                try:
                    reply_text = bing.get_msg()
                except Exception as e:
                    reply_text = f"网络错误：{e}"
            threading.Thread(target=task.reply_callback, args=(reply_text,), daemon=True).start()


if __name__ == '__main__':
    test = BinAITaskPool(proxy="http://localhost:7890", headless=False)
    test.start()
    while True:
        question = input("请输入问题：")
        print("思考中...")
        test.put_question(BinAITask(question, print))