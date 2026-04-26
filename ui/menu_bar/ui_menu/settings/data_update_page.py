from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy, QFormLayout

from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout

class DataUpdatePage(BasePage):
    def __init__(self,title):
        super().__init__(title)
        self._init_update()

    def _init_update(self):
        # 更新频率
        update_time,update_time_layout = Pyqt5WidgetLayout.create_border_block("更新频率",layout_type="qv_layout")

        # 更新速率
        update_timer_block,update_time_block_layout = Pyqt5WidgetLayout.create_div("row")
        update_time_label = Pyqt5WidgetLayout.add_label("更新时间间隔（秒）：",warp=False)
        update_time_spin = Pyqt5WidgetLayout.add_spinbox(self.setting_config['data_update']['update_time_second'],86400,1,align=Qt.AlignLeft | Qt.AlignVCenter)

        update_time_block_layout.addWidget(update_time_label)
        update_time_block_layout.addWidget(update_time_spin)
        update_time_block_layout.addStretch()

        update_time_layout.addWidget(update_timer_block)

        # 任务变更时自动保存
        task_range_save = Pyqt5WidgetLayout.add_switch("任务变更时自动保存",checked=self.setting_config['data_update']['task_change_auto_save'])
        update_time_layout.addWidget(task_range_save)

        # 注意
        task_label = Pyqt5WidgetLayout.add_label(self.setting_config['data_update']['data_update_attention'],obj_class="attention_label")
        update_time_layout.addWidget(task_label)

        self.main_content_layout.addWidget(update_time)

        # 数据优化
        date_optimize,date_optimize_layout = Pyqt5WidgetLayout.create_border_block("数据优化",layout_type="qv_layout")

        data_button,data_button_layout = Pyqt5WidgetLayout.create_div("row")

        # 清理历史数据
        clear_data_button = Pyqt5WidgetLayout.add_button("清理历史数据",
            obj_class="""
                QPushButton{
                    color: white;  /* 文字色 */
                    background-color: #dc3545;  
                    border: none; 
                    border-radius: 4px;
                    padding: 10px 5px;
                    font-weight: bold;
                    font-size: 14px;
                    }
                QPushButton:hover{
                    background-color: #c22f3d;
                }
            """,size_width=None)

        # 优化数据性能
        optimize_data_button = Pyqt5WidgetLayout.add_button("清理历史数据",
            obj_class="""
                    QPushButton{
                        color: white;  /* 文字色 */
                        background-color: #007bff;  
                        border: none; 
                        border-radius: 4px;
                        padding: 10px 5px;
                        font-weight: bold;
                        font-size: 14px;
                        }
                    QPushButton:hover{
                        background-color: #006adb;
                    }
                """, size_width=None)

        data_button_layout.addWidget(clear_data_button)
        data_button_layout.addWidget(optimize_data_button)

        date_optimize_layout.addWidget(data_button)

        # 数据注意提示
        data_tips = Pyqt5WidgetLayout.add_label(self.setting_config['data_update']['data_tips_attention'],obj_class="attention_label")
        date_optimize_layout.addWidget(data_tips)

        self.main_content_layout.addWidget(date_optimize)

        self.main_content_layout.addStretch()
