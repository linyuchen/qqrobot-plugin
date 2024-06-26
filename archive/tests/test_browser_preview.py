from unittest import TestCase

from PIL import Image

from msgplugins.browser_preview.browser_screenshot import github_readme, search_baidu, ZhihuPreviewer, moe_wiki, \
    wx_article
from config import get_config

GFW_PROXY = get_config("GFW_PROXY")


class TestBrowserPreview(TestCase):
    zhihu_previewer = ZhihuPreviewer()

    def test_baidu(self):
        Image.open(search_baidu("python")).show()

    def test_github_readme(self):
        Image.open(github_readme("https://github.com/linyuchen/qqrobot-plugin", http_proxy=GFW_PROXY)).show()

        self.assertIsNone(github_readme("https://github.com/microsoft/playwright-python/issues/2087"))

    def test_zhihu_question(self):
        url = "https://www.zhihu.com/question/68611994/answer/3188443851"
        Image.open(self.zhihu_previewer.screenshot_zhihu_question(url)).show()

    def test_zhihu_article(self):
        url = "https://zhuanlan.zhihu.com/p/191600009"
        Image.open(self.zhihu_previewer.screenshot_zhihu_zhuanlan(url)).show()

    def test_moe_wiki(self):
        keyword = "39music"
        Image.open(moe_wiki(keyword)).show()

    def test_wx_article(self):
        url = "https://mp.weixin.qq.com/s/2j1VZDFsgxiuLVjNq09SXw"
        Image.open(wx_article(url)).show()
