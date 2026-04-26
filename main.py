
import sys

from PyQt5.QtWidgets import QApplication,QMainWindow

from compents.load_path import config_manager
from compents.log import logger
from uilt.qss_tool.qss_load_tool import QssLoadTool
from ui.main_window_ui import MainWindowUI
from compents.init_json_file import InitJsonFile
from ui.menu_bar.ui_menu.menu_bar.menu_ui import MenuUi


class MyMainWindow(QMainWindow):
    setting_path = config_manager.get_entity_config(path_key="menu_bar/settings")
    def __init__(self):
        super().__init__()
        logger.info("启动主窗口！")

        # 设置窗口基础类型

        self.setWindowTitle(MainWindowUI.setting_path["basic"]["exe_name"])
        self.resize(1280,650)
        self.move(300,200)

        logger.info("初始化文件夹")
        InitJsonFile()
        

    def __del__(self):
        logger.info("窗口关闭！")



if __name__ == '__main__':
    my_app = QApplication(sys.argv)

    # 加载qss 文件
    qss_file = [
        "qss/original.qss",
        "qss/public.qss",
        "qss/main_window_ui.qss",
        "qss/segmentation.qss",
        "qss/toggle.qss",
        "qss/chat.qss",
        "qss/diary.qss",
        "qss/operation_config_dialog.qss",
        "qss/password_dialog.qss",
        "qss/pyqt5_widget_layout.qss",
        "ui/menu_bar/ui_menu/qss/base.qss",
        "ui/menu_bar/ui_menu/qss/basic_page.qss",
        "ui/menu_bar/ui_menu/qss/backup_page.qss",
        "ui/menu_bar/ui_menu/qss/shortcut_page.qss"
    ]
    qss = QssLoadTool.load_multi_qss(qss_file)
    my_app.setStyleSheet(qss)
    logger.info("qss文件加载完成")

    my_window = MyMainWindow()


    # main_window_ui控件
    main_window_ui = MainWindowUI(my_window)
    MenuUi(my_window)

    my_window.show()
    sys.exit(my_app.exec_())



