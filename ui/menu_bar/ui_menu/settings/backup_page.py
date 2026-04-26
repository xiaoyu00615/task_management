from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy, QFormLayout

from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout

class BackUpPage(BasePage):
    def __init__(self,title):
        super().__init__(title)
        self.title = title
        self._init_back_up()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def _init_back_up(self):
        # 自动备份
        auto_back_widget,auto_back_layout = Pyqt5WidgetLayout.create_border_block("自动备份",layout_type="qv_layout")
        open_auto_backup = Pyqt5WidgetLayout.add_switch("启用自动备份",checked=self.setting_config["backup"]["auto_backup"])
        auto_back_layout.addWidget(open_auto_backup)

        # 备份间隔
        backup,backup_layout = Pyqt5WidgetLayout.create_div("row")
        backup_timer = Pyqt5WidgetLayout.add_label("备份间隔（分钟）：",warp=False)
        backup_spin = Pyqt5WidgetLayout.add_spinbox(self.setting_config["backup"]["backup_time_minute"])

        backup_layout.addWidget(backup_timer)
        backup_layout.addWidget(backup_spin)
        backup_layout.addStretch()

        auto_back_layout.addWidget(backup)

        # 备份目录
        backup_dir, backup_layout = Pyqt5WidgetLayout.create_div("row")

        backup_dir_label = Pyqt5WidgetLayout.add_label("备份目录：")

        # 路径框
        path_edit = Pyqt5WidgetLayout.add_edit(self.setting_config["backup"]["backup_dir"])
        button_path = Pyqt5WidgetLayout.add_button("浏览",
            obj_class="""
                QPushButton{
                    color: white;  /* 文字色 */
                    background-color: #0078D7;  
                    border: none; 
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-weight: bold;
                    font-size: 14px;
                    }
                QPushButton:hover{
                    background-color: #0068ba;
                }
            """,size_width=80)

        backup_layout.addWidget(backup_dir_label)
        backup_layout.addWidget(path_edit)
        backup_layout.addWidget(button_path)

        auto_back_layout.addWidget(backup_dir)


        self.main_content_layout.addWidget(auto_back_widget)


        # 手动备份
        manual_widget,manual_layout = Pyqt5WidgetLayout.create_border_block("手动备份")

        click_backup_button = Pyqt5WidgetLayout.add_button("立即手动备份",
            obj_class="""
                QPushButton{
                    color: white;  /* 文字色 */
                    background-color: #28a745;  
                    border: none; 
                    border-radius: 4px;
                    padding: 10px 5px;
                    font-weight: bold;
                    font-size: 14px;
                    }
                QPushButton:hover{
                    background-color: #208537;
                }
            """,size_width=None)
        manual_layout.addWidget(click_backup_button)

        # 注意
        attention_label = Pyqt5WidgetLayout.add_label(self.setting_config["backup"]["click_backup_attention"],obj_class="attention_label")
        manual_layout.addWidget(attention_label)

        self.main_content_layout.addWidget(manual_widget)


        # 数据恢复
        data_recover_widget,data_recover_layout = Pyqt5WidgetLayout.create_border_block("数据恢复")
        # 按钮
        data_recover = Pyqt5WidgetLayout.add_button("从备份文件恢复",
            obj_class="""
                QPushButton{
                    color: white;  /* 文字色 */
                    background-color: #ffc107;  
                    border: none; 
                    border-radius: 4px;
                    padding: 10px 5px;
                    font-weight: bold;
                    font-size: 14px;
                    }
                QPushButton:hover{
                    background-color: #c99806;
                }
            """,size_width=None)
        data_recover_layout.addWidget(data_recover)

        recover_error = Pyqt5WidgetLayout.add_label(self.setting_config["backup"]["click_recover_warning"],obj_class="error_label")
        data_recover_layout.addWidget(recover_error)

        self.main_content_layout.addWidget(data_recover_widget)

        self.main_content_layout.addStretch()