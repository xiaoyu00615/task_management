
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QSizePolicy, QFormLayout

from .base_page import BasePage
from compents_pyqt5.pyqt5_widget_layout import Pyqt5WidgetLayout

class NotificationPage(BasePage):
    def __init__(self,title):
        super().__init__(title)
        self._init_notification()

    def _init_notification(self):
        notification,notification_layout = Pyqt5WidgetLayout.create_border_block("通知选项",layout_type="qv_layout")

        # 误触提示
        misoperation_notification = Pyqt5WidgetLayout.add_switch("误操作提示",self.setting_config['notification']['misoperation_notification'])
        notification_layout.addWidget(misoperation_notification)

        # 托盘弹窗提示
        tray_tips = Pyqt5WidgetLayout.add_switch("托盘弹窗提示",self.setting_config['notification']['tray_tips'])
        notification_layout.addWidget(tray_tips)

        # 任务升级提示
        task_up_leve_tips = Pyqt5WidgetLayout.add_switch("任务升级提示",self.setting_config['notification']['task_up_leve_tips'])
        notification_layout.addWidget(task_up_leve_tips)

        # 任务超时提示
        task_out_time_tips = Pyqt5WidgetLayout.add_switch("任务超时提示",self.setting_config['notification']['task_timeout_tips'])
        notification_layout.addWidget(task_out_time_tips)

        # 窗口开启/关闭提示
        window_open_close = Pyqt5WidgetLayout.add_switch("窗口开启/关闭提示",self.setting_config['notification']['task_open_or_close'])
        notification_layout.addWidget(window_open_close)

        # 相同任务提示冷却时间
        same_tips_timer,same_tips_timer_layout = Pyqt5WidgetLayout.create_div("row")

        same_label = Pyqt5WidgetLayout.add_label("相同通知冷却时间（分钟）：",warp=self.setting_config['notification']['same_task_timer_minute'])
        same_spin = Pyqt5WidgetLayout.add_spinbox(1,1440,1)
        same_tips_timer_layout.addWidget(same_label)
        same_tips_timer_layout.addWidget(same_spin)
        same_tips_timer_layout.addStretch()

        notification_layout.addWidget(same_tips_timer)

        tips = Pyqt5WidgetLayout.add_label(self.setting_config['notification']['setting_notification_attention'],obj_class="attention_label")
        notification_layout.addWidget(tips)

        self.main_content_layout.addWidget(notification)


        # 通知演示
        demo,demo_layout = Pyqt5WidgetLayout.create_border_block("通知测试",layout_type="qv_layout")
        self.main_content_layout.addWidget(demo)

        # 按钮
        send_test_btn = Pyqt5WidgetLayout.add_button("发送测试通知",
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
            """,size_width=None)
        demo_layout.addWidget(send_test_btn)

        # 发送提示
        send_tips = Pyqt5WidgetLayout.add_label(self.setting_config['notification']['send_test_attention'],obj_class="error_label")
        demo_layout.addWidget(send_tips)

        self.main_content_layout.addStretch()