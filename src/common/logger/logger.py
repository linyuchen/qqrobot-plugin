import datetime
import logging
from pathlib import Path
base_dir = Path(__file__).parent.parent.parent.parent / "logs"
# 创建logger对象
logger = logging.getLogger('robot_plugin')
logger.setLevel(logging.DEBUG)

# 创建一个用于写入error级别日志的handler
error_handler = logging.FileHandler(base_dir / f'error-{datetime.datetime.now().date()}.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)

# 创建一个用于写入所有级别日志的handler
debug_handler = logging.FileHandler(base_dir / f'debug-{datetime.datetime.now().date()}.log', encoding='utf-8')
debug_handler.setLevel(logging.DEBUG)

info_handler = logging.FileHandler(base_dir / f'{datetime.datetime.now().date()}.log', encoding='utf-8')
info_handler.setLevel(logging.INFO)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s[line:%(lineno)d]: %(message)s ')

# 将格式应用到handler
error_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)

# 将handler添加到logger对象中
logger.addHandler(error_handler)
logger.addHandler(debug_handler)
logger.addHandler(info_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
