from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy, QFormLayout

from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout


class AppearancePage(BasePage):
    def __init__(self, title,parent=None):
        super().__init__(title)
        self.title = title
        self.init_appearance()

    def init_appearance(self):
        self.window_template("主窗口",self.setting_config["appearance"]["main_window"]["width"],self.setting_config["appearance"]["main_window"]["height"])

        window_theme,window_theme_layout = Pyqt5WidgetLayout.create_border_block("界面主题","qv_layout")

        self.main_content_layout.addWidget(window_theme)


        self.window_template("任务细分窗口",self.setting_config["appearance"]["task_segmentation_window"]["width"],self.setting_config["appearance"]["task_segmentation_window"]["height"])
        self.window_template("日记详情窗口",self.setting_config["appearance"]["diary_details_window"]["width"],self.setting_config["appearance"]["diary_details_window"]["height"])
        self.window_template("设置窗口",self.setting_config["appearance"]["setting_window"]["width"],self.setting_config["appearance"]["setting_window"]["height"])



        self.main_content_layout.addStretch()

    def window_template(self,title,default_width,default_height):
        print(default_width,default_height,"width-height")
        window_size, window_size_layout = Pyqt5WidgetLayout.create_border_block(title, "form_layout", )
        self.main_content_layout.addWidget(window_size)

        window_width_label = Pyqt5WidgetLayout.add_label("窗口宽度：")
        # 1280 ，650
        window_width_spin = Pyqt5WidgetLayout.add_spinbox(num=default_width, max_num=2560, min_num=500, width=None,
                                                          align=Qt.AlignLeft | Qt.AlignVCenter)
        window_size_layout.addRow(window_width_label, window_width_spin)

        window_height_label = Pyqt5WidgetLayout.add_label("窗口高度：")
        window_height_spin = Pyqt5WidgetLayout.add_spinbox(num=default_height, max_num=1440, min_num=500, width=None,
                                                           align=Qt.AlignLeft | Qt.AlignVCenter)
        window_size_layout.addRow(window_height_label, window_height_spin)