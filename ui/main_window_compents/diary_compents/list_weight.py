from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from ui.main_window_compents.diary_compents.diary_item import DiaryItem
from ui.main_window_compents.diary_compents.tool_def import ToolDef

from compents.file_process import FileProcess

class ListWeight:
    def __init__(self,this,list_dict,diary_type,parent):
        self.this = this
        self.parent = parent
        self.diary_type = diary_type
        self.list_dict = list_dict[diary_type]
        # print(self.list_dict,"__init__list_dict")
        self.list_dict_num = len(self.list_dict)
        self._ui_list()

    def _ui_list(self):
        self.list_container = QWidget()
        self.list_container.setMinimumWidth(300)
        self.list_container.setObjectName("list_layout")
        self.list_container_layout = QVBoxLayout(self.list_container)

        # 滚动区域
        self.chat_scroll = QScrollArea()  # 滚动区域
        self.chat_scroll.setWidgetResizable(True)  # 自适应内容高度
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭横向滚动（关键：避免宽度拉伸）
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 纵向滚动按需显示
        self.list_container_layout.addWidget(self.chat_scroll)

        if self.diary_type == 'ordinary_list':
            self.diary_num = QLabel(f"日记总数：({self.list_dict_num})")
            self.list_container_layout.addWidget(self.diary_num)
        else:
            self.diary_num = QLabel(f"收藏总数：({self.list_dict_num})")
            self.list_container_layout.addWidget(self.diary_num)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.chat_scroll.setWidget(self.content)
        self.list_container_layout.addWidget(self.chat_scroll)



        self._load_list()


    def _load_list(self):
        self.list_dict.sort(key=lambda x: x["create_stamp"], reverse=reversed)
        for item in self.list_dict:
           self.add_item(item)

    def add_item(self,data_dict):
        self.content_layout.addWidget(DiaryItem.create_diary_item(self.this,self,data_dict,self.parent))




    def ref_list(self,update):
        ToolDef.del_all_tasks_ui(update)
        self.list_dict = FileProcess.read_json_attribute("data/diary.json",[self.diary_type])
        print(self.list_dict,"__init__list_dict",self.diary_type)

        self._load_list()

        self.diary_num.setText(f"日记总数：({len(self.list_dict)})")