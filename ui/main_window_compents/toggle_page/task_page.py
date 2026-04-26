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
from compents.load_path import load_path

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

        main_right_layout = QVBoxLayout(main_right_widget)
        
        # 添加搜索和筛选区域
        search_filter_widget = QWidget()
        search_filter_layout = QHBoxLayout(search_filter_widget)
        search_filter_layout.setSpacing(10)
        
        # 搜索框
        search_label = QLabel("搜索:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入任务名称...")
        self.search_input.textChanged.connect(self._on_search_changed)
        
        # 筛选下拉框
        filter_label = QLabel("筛选:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("全部")
        
        # 从配置中加载分类选项
        category_list = FileProcess.read_json_attribute(load_path["data_map"], ["category_map"])
        for category in category_list:
            self.filter_combo.addItem(category)
        
        self.filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        
        search_filter_layout.addWidget(search_label)
        search_filter_layout.addWidget(self.search_input)
        search_filter_layout.addWidget(filter_label)
        search_filter_layout.addWidget(self.filter_combo)
        search_filter_layout.addStretch()
        
        main_right_layout.addWidget(search_filter_widget)

        # 任务列表区域
        list_widget = QWidget()
        list_layout = QHBoxLayout(list_widget)

        self.this.unfinished_list = ListLayout("unfinished", self.this.parent, self.this)
        self.this.overtime_list = ListLayout("overtime", self.this.parent, self.this)
        self.this.completed_list = ListLayout("completed", self.this.parent, self.this)

        self.this.all_list = {
            "unfinished": self.this.unfinished_list,
            "overtime": self.this.overtime_list,
            "completed": self.this.completed_list
        }

        list_layout.addWidget(self.this.unfinished_list.container)
        list_layout.addWidget(self.this.overtime_list.container)
        list_layout.addWidget(self.this.completed_list.container)
        
        main_right_layout.addWidget(list_widget, stretch=1)

        # 组合
        task_layout.addWidget(left_form_widget)
        task_layout.addWidget(main_right_widget)
    
    def _on_search_changed(self, text):
        """搜索文本变化时触发"""
        for list_name, list_obj in self.this.all_list.items():
            list_obj.filter_tasks(search_text=text)
    
    def _on_filter_changed(self, index):
        """筛选选项变化时触发"""
        filter_text = self.filter_combo.currentText()
        for list_name, list_obj in self.this.all_list.items():
            list_obj.filter_tasks(filter_category=filter_text if filter_text != "全部" else None)