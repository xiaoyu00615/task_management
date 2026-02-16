from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QScrollArea
from ui.main_window_compents.item_widget import ItemWidget
from compents.file_process import FileProcess
from compents.log import logger
from ui.uilt.assistant_def import AssistantDef
from compents.load_path import load_path

class ListLayout(QWidget):
    def __init__(self,status,parent=None,main_window=None):
        super().__init__(parent)
        self.widget_list = []
        self.status = status
        self.main_window = main_window
        self.parent = parent

        self.choose_list = None
        self._init_ui()



    def _init_ui(self):
        self.scroll_area = QScrollArea()
        self.container = QWidget(parent=self.parent)
        self.container.setObjectName("list_layout")

        self.main_right_layout = QVBoxLayout(self.container)

        # 配置滚动区域
        # 内容部件随滚动区域自适应宽度
        self.scroll_area.setWidgetResizable(True)
        # 垂直滚动条按需显示
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 隐藏水平滚动条
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self._init_list(self.main_right_layout)


    def _init_list(self,main_layout):
        # 上半部分基础信息
        self.text_map = {
            "unfinished":"待完成",
            "overtime":"已超时",
            "completed":"已完成"
        }
        if self.status:
            get_data = self.get_all_tasks()
            self.choose_list = get_data.get(f"{self.status}_list",[])

        if self.status == "unfinished":
            self.main_window.unfinished_list_task_data = self.choose_list

            logger.debug(f"初始化 -> {self.text_map[self.status]}列表 -> {self.choose_list}数据")




        self.label_value = QLabel(f"{self.text_map.get(self.status,None)}:({len(self.choose_list)})")
        self.label_value.setObjectName("form_key_style")
        main_layout.addWidget(self.label_value)

        # 下部分内容竖向列表
        content_widget = QWidget()
        self.content_widget_layout = QVBoxLayout(content_widget)
        # 当列表大于0 时进行熏染
        self._load_items()


        self.scroll_area.setWidget(content_widget)
        main_layout.addWidget(self.scroll_area,stretch=1)
        main_layout.addStretch()

    def get_all_tasks(self):

        return FileProcess.read_json(load_path["store"]["task"])


    def _load_items(self):
        """加载列表项（抽离成独立方法，方便刷新调用）"""
        if not len(self.choose_list) > 0:
            return

        if self.status == "unfinished":
            AssistantDef.tasks_sort(self.choose_list,'weight')

        for index,task in enumerate(self.choose_list):
            task_item = ItemWidget(task,self.main_window.all_list,self,index)
            self.widget_list.append(task_item)
            self.content_widget_layout.addWidget(task_item.main_item_layout)
        self.content_widget_layout.addStretch()



    def del_all_tasks_ui(self):
        while self.content_widget_layout.count():
            item = self.content_widget_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

            self.widget_list.clear()


        return True

    def refresh_list(self):

        self.del_all_tasks_ui()

        if self.status:
            get_data = self.get_all_tasks()
            self.choose_list = get_data.get(f"{self.status}_list",[])
            # logger.debug(f"刷新列表 -> {self.choose_list}")

        self.label_value.setText(f"{self.text_map.get(self.status,None)}:({len(self.choose_list)})")

        self._load_items()