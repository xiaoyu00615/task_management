from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout



class BasicPage(BasePage):
    def __init__(self,title):
        super().__init__(title)
        self._init_basic_ui()

    def _init_basic_ui(self):
        widget, layout = Pyqt5WidgetLayout.create_border_block(self.setting_config['basic']['exe_message'], "form_layout")

        # 窗口名称
        window_name_label = Pyqt5WidgetLayout.add_label("窗口名称：")
        window_name_value = Pyqt5WidgetLayout.add_label(self.setting_config['basic']['exe_name'],obj_class="value_style",bg_color="white")
        layout.addRow(window_name_label,window_name_value)

        # 当前版本
        now_version_label = Pyqt5WidgetLayout.add_label("当前版本：")
        now_version_value = Pyqt5WidgetLayout.add_label(self.setting_config['basic']['version'],obj_class="value_style",bg_color="white")
        layout.addRow(now_version_label,now_version_value)

        # 最近更新
        now_update_label = Pyqt5WidgetLayout.add_label("最近更新：")
        now_update_value = Pyqt5WidgetLayout.add_label(self.setting_config['basic']['update_time'],obj_class="value_style",bg_color="white")
        layout.addRow(now_update_label,now_update_value)

        self.main_content_layout.addWidget(widget)


        re_button = Pyqt5WidgetLayout.add_button("重置所有设置",
            obj_class="""
                QPushButton{
                    color: white;  /* 文字色 */
                    background-color: #e74c3c;  /* 背景色（必生效） */
                    border: none;  /* 关键！ */
                    border-radius: 4px;
                    padding: 10px 16px;
                    font-weight: bold;
                    font-size: 14px;
                    }
                QPushButton:hover{
                    background-color: #cf3a46;
                }
            """,size_width=120)
        self.main_content_layout.addWidget(re_button)



        # 程序详情
        exe_message_widget, exe_message_layout = Pyqt5WidgetLayout.create_border_block("程序详情","qv_layout")
        # 介绍
        message = Pyqt5WidgetLayout.add_label(self.setting_config['basic']['message'])
        exe_message_layout.addWidget(message)

        self.main_content_layout.addWidget(exe_message_widget)

        self.main_content_layout.addStretch()