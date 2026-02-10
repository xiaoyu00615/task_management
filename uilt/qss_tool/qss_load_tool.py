import os.path

from compents.log import logger

class QssLoadTool:
    def __init__(self):
        pass

    @staticmethod
    def load_multi_qss(file_paths):
        """
        加载并合并多个QSS文件，按列表顺序读取，后加载的覆盖先加载的同属性
        :param file_paths: QSS文件路径列表，如["global.qss", "login.qss"]
        :return: 合并后的QSS内容字符串
        """
        logger.info("开始加载qss文件")
        qss_content = ""
        for path in file_paths:
            path = os.path.join('qss', path)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    qss_content += f.read() + "\n"  # 加换行符，避免样式连写报错
            except FileNotFoundError:
                print(f"警告：未找到QSS文件 {path}，跳过加载")
            except Exception as e:
                print(f"错误：读取QSS文件 {path} 失败：{e}，跳过加载")
        return qss_content
