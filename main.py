
import sys

from PyQt5.QtWidgets import QApplication,QMainWindow

from compents.log import logger
from uilt.qss_tool.qss_load_tool import QssLoadTool
from ui.main_window_ui import MainWindowUI
from compents.init_json_file import InitJsonFile


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        logger.info("启动主窗口！")

        # 设置窗口基础类型
        self.setWindowTitle("task_management")
        self.resize(1280,600)
        self.move(300,200)

        logger.info("初始化文件夹")
        InitJsonFile()
        

    def __del__(self):
        logger.info("窗口关闭！")



if __name__ == '__main__':
    my_app = QApplication(sys.argv)

    # 加载qss 文件
    qss_file = [
        "original.qss",
        "public.qss",
        "main_window_ui.qss",
        "segmentation.qss",
        "toggle.qss",
        "chat.qss",
        "diary.qss",
    ]
    qss = QssLoadTool.load_multi_qss(qss_file)
    my_app.setStyleSheet(qss)
    logger.info("qss文件加载完成")

    my_window = MyMainWindow()

    # main_window_ui控件
    main_window_ui = MainWindowUI(my_window)

    my_window.show()
    sys.exit(my_app.exec_())



