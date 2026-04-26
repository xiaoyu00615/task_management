from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy, QFormLayout

from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout

class ShortcutPage(BasePage):
    def __init__(self,title,parent=None):
        super().__init__(title)
        self._init_shortcut()

    def _init_shortcut(self):
        shortcut,shortcut_layout = Pyqt5WidgetLayout.create_border_block("常用快捷键",layout_type="qv_layout")

        # 强制关闭程序
        close_exe_row,close_exe_row_layout = Pyqt5WidgetLayout.create_div("row")
        close_exe_label = Pyqt5WidgetLayout.add_label(self.setting_config['shortcut']['close']['text'],obj_class="show_shortcut_label")
        close_exe_shortcut_label = Pyqt5WidgetLayout.add_label(self.setting_config['shortcut']['close']['key'],obj_class="show_shortcut_style")

        close_exe_row_layout.addWidget(close_exe_label)
        close_exe_row_layout.addWidget(close_exe_shortcut_label)
        close_exe_row_layout.addStretch()

        shortcut_layout.addWidget(close_exe_row)


        # 提示内容
        tips_text = Pyqt5WidgetLayout.add_label(self.setting_config['shortcut']['close']['tips'],obj_class="attention_label")
        shortcut_layout.addWidget(tips_text)



        self.main_content_layout.addWidget(shortcut)

        self.main_content_layout.addStretch()