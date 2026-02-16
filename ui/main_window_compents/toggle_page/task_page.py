import datetime

from PyQt5.QtCore import QDateTime, qQNaN, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QFormLayout, QWidget, QLineEdit, QDateEdit, QComboBox, QDateTimeEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QStackedWidget

from compents.log import logger
from compents.file_process import FileProcess
from compents.time_process import TimeProcess
from compents.calculate_process import CalculateProcess
from compents.str_process import StrProcess
from ui.main_window_compents.list_layout import ListLayout
from ui.main_window_compents.event_def import EventDef
from ui.uilt.assistant_def import AssistantDef

class TaskPage:
    def __init__(self,this):
        self.this = this
        self._ui_init()

    def _ui_init(self):
        # 创建任务
        self.task_container = QWidget(self.this.parent)
        task_layout = QHBoxLayout(self.task_container)

        # 左侧表单容器控件
        left_form_widget = QWidget(self.this.parent)
        left_form_widget.setFixedWidth(280)
        # 左侧表单
        form_layout = QFormLayout(left_form_widget)
        form_layout.setSpacing(10)
        self.this._init_form_widgets(form_layout)

        # 右侧区域
        main_right_widget = QWidget(self.this.parent)

        main_right_layout = QHBoxLayout(main_right_widget)

        self.this.unfinished_list = ListLayout("unfinished", self.this.parent, self.this)
        self.this.overtime_list = ListLayout("overtime", self.this.parent, self.this)
        self.this.completed_list = ListLayout("completed", self.this.parent, self.this)

        self.this.all_list = {
            "unfinished": self.this.unfinished_list,
            "overtime": self.this.overtime_list,
            "completed": self.this.completed_list
        }

        main_right_layout.addWidget(self.this.unfinished_list.container)
        main_right_layout.addWidget(self.this.overtime_list.container)
        main_right_layout.addWidget(self.this.completed_list.container)

        # 组合
        task_layout.addWidget(left_form_widget)
        task_layout.addWidget(main_right_widget)