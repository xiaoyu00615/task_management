import datetime

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFormLayout, QLineEdit, QDateTimeEdit, \
    QComboBox, QPushButton, QTableWidget, QTextEdit, QScrollArea

from compents.file_process import FileProcess
from ui.main_window_compents.event_modal_segmentation import EventModalSegmentation


class ModalSegmentation(QDialog):
    def __init__(self,parent=None,task=None):
        super().__init__(parent)
        self.task_item_widget = None
        self.task = task
        self.task_status = task.get("status", None)
        self.all_segmentation_task = task.get("segmentation", None)

        # print(self.task,"self.task")

        self._init_ui()

        # print(self.all_segmentation_task,"self.all_segmentation_task")
        self.create_all_task(self.all_segmentation_task)

    def _init_ui(self):
        # print("实例了窗口")
        self.setWindowTitle(f"细碎任务 -- {self.task.get("name")}")
        self.setFixedSize(650,550)

        # 主窗口
        main_widget = QWidget()

        # 水平布局
        self.main_layout = QHBoxLayout(main_widget)

        # form 布局
        self.form_widget = QWidget()
        form_layout = QFormLayout(self.form_widget)
        self.form_widget.setFixedWidth(300)
        self._form_ui(form_layout)

        self._list_ui()

    def _form_ui(self,form_layout):
        # 任务名称
        task_name_table = QLabel("任务名称：")
        task_name_table.setObjectName("form_key_style")

        self.task_name_line_edit = QLineEdit()
        self.task_name_line_edit.setObjectName("form_value_style")
        self.task_name_line_edit.setPlaceholderText("请输入任务名称！")
        form_layout.addRow(task_name_table, self.task_name_line_edit)


        # 任务描述
        task_lines_label = QLabel("任务描述：")
        task_lines_label.setObjectName("form_key_style")

        self.task_lines_value = QTextEdit()
        self.task_lines_value.setObjectName("form_value_style")
        self.task_lines_value.setPlaceholderText("请输入任务描述！")
        form_layout.addRow(task_lines_label,self.task_lines_value)


        mar = QLabel()


        task_submit_data = QPushButton("创建任务")
        task_submit_data.setObjectName("button_style")
        task_submit_data.setFixedWidth(150)



        task_submit_data.clicked.connect(lambda: EventModalSegmentation.on_segmentation_create_task(self,self.task,self.get_data()))
        form_layout.addRow(mar,task_submit_data)

        self.main_layout.addWidget(self.form_widget)


        self.setLayout(self.main_layout)


    def _list_ui(self):

        # 配置滚动区域
        self.scroll_area = QScrollArea()
        # 内容部件随滚动区域自适应宽度
        self.scroll_area.setWidgetResizable(True)
        # 垂直滚动条按需显示
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 隐藏水平滚动条
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.list_widget = QWidget()
        self.list_widget.setObjectName("list_layout")


        list_layout = QVBoxLayout(self.list_widget)

        task_show_num = QWidget()
        task_show_num_layout = QVBoxLayout(task_show_num)
        list_layout.addWidget(task_show_num)

        self.label_value = QLabel(f"细碎任务（{len(self.all_segmentation_task)}）")
        self.label_value.setObjectName("form_key_style")
        task_show_num_layout.addWidget(self.label_value)


        # 上部分
        self.main_layout.addWidget(self.list_widget)
        # 下部分
        self.content_widget = QWidget()
        self.main_down = QVBoxLayout(self.content_widget)


        self.scroll_area.setWidget(self.content_widget)
        list_layout.addWidget(self.scroll_area)

        self.main_layout.addWidget(self.list_widget)


    def get_data(self):
        max_segmentation_id = FileProcess.read_json_attribute("data/tasks.json",["max_segmentation_id"])

        return {
            "segmentation_id": max_segmentation_id + 1,
            "name": self.task_name_line_edit.text().strip(),
            "description": self.task_lines_value.toPlainText().strip(),
            "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status":"unfinished",
            "end_time":None
        }


    def create_task_item_ui(self,task,index):

        self.task_item_widget = QWidget()
        self.task_item_widget.setContentsMargins(5,5,5,0)

        task_item_down_layout = QVBoxLayout(self.task_item_widget)
        task_item_down_layout.setSpacing(8)
        self.task_item_widget.setObjectName("item_style")
        # print(task,"create_task")




        name_ql = QLabel(f"{index}、{task.get("name", None)}")
        name_ql.setObjectName("segmentation_title_un")
        task_item_down_layout.addWidget(name_ql)


        description_ql = QLabel(f"任务描述：{task.get("description", None)}")
        description_ql.setObjectName("segmentation_content")

        task_item_down_layout.addWidget(description_ql)

        create_ql = QLabel(f"创建时间：{task.get("create_time", None)}")
        create_ql.setObjectName("segmentation_create_time")
        create_ql.setStyleSheet(f"""color:#388E3C;""")
        task_item_down_layout.addWidget(create_ql)

        if task.get("status") == "completed":
            end_ql = QLabel(f"完成时间：{task.get("end_time", None)}")
            end_ql.setObjectName("segmentation_end_time")
            end_ql.setStyleSheet(f"""color:#0288D1""")
            task_item_down_layout.addWidget(end_ql)


            name_ql.setStyleSheet("""text-decoration: line-through;""")
            description_ql.setStyleSheet("""text-decoration: line-through;""")



        btn_widget = QWidget()
        btn_widget.setContentsMargins(0,0,0,0)
        btn_layout = QHBoxLayout(btn_widget)

        del_btn = QPushButton()
        del_btn.setText("删除")
        del_btn.clicked.connect(lambda :EventModalSegmentation.on_del_segmentation_task(self,self.task,task))

        com_btn = QPushButton()
        com_btn.setText("完成")
        com_btn.clicked.connect(lambda : EventModalSegmentation.on_complete_segmentation_task(self,self.task,task))

        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(com_btn)



        task_item_down_layout.addWidget(btn_widget)


        self.main_down.addWidget(self.task_item_widget)
        task_item_down_layout.addStretch()

    def create_all_task(self,task_list):
        # print("task_list",task_list)

        for index,item in enumerate(task_list):
            # print(item,"create_all_task")
            self.create_task_item_ui(item,index+1)


    def del_all_tasks_ui(self):
        while self.main_down.count():
            item = self.main_down.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


    def refresh_all_segmentation_tasks_ui(self,task_list_item):
        get_data = FileProcess.read_json("data/tasks.json")


        self.del_all_tasks_ui()

        sort_list = task_list_item["segmentation"][::-1]

        self.create_all_task(sort_list)

        # 最新缓存数据
        self.task = task_list_item

        self.label_value.setText(f"细碎任务（{len(task_list_item["segmentation"])}）")

        for items_list in get_data[f"{self.task_status}_list"]:
            if items_list["id"] == task_list_item["id"]:
                items_list["segmentation"] = task_list_item["segmentation"]
                break

        FileProcess.write_json("data/tasks.json",get_data)


    def del_segmentation_tasks(self,task_list,task):
        for index,item in enumerate(task_list["segmentation"]):
            if item["segmentation_id"] == task["segmentation_id"]:
                task_list["segmentation"].pop(index)
                break
        return task_list
