import datetime

from PyQt5.QtCore import QDateTime, qQNaN, QTimer
from PyQt5.QtWidgets import QLabel, QFormLayout, QWidget, QLineEdit, QDateEdit, QComboBox, QDateTimeEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout

from compents.log import logger
from compents.file_process import FileProcess
from compents.time_process import TimeProcess
from compents.calculate_process import CalculateProcess
from compents.str_process import StrProcess
from ui.main_window_compents.list_layout import ListLayout
from ui.main_window_compents.event_def import EventDef
from ui.uilt.assistant_def import AssistantDef


class MainWindowUI(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.unfinished_list_task_data = []
        self.timer_ms = FileProcess.read_json_attribute("config/setting.json",["time","data_refresh"])
        self.all_list = {}
        logger.info("主窗口UI控件类")
        self._init_ui()
        self._init_time()

    def _init_ui(self):
        logger.info("正在创建MainWindowUI")

        main_layout = QHBoxLayout()

        # 左侧表单容器控件
        left_form_widget = QWidget(self.parent)
        left_form_widget.setFixedWidth(280)
        # 左侧表单
        form_layout = QFormLayout(left_form_widget)
        form_layout.setSpacing(10)
        self._init_form_widgets(form_layout)

        # 右侧区域
        main_right_widget = QWidget(self.parent)

        main_right_layout = QHBoxLayout(main_right_widget)


        self.unfinished_list = ListLayout("unfinished",self.parent,self)
        self.overtime_list = ListLayout("overtime",self.parent,self)
        self.completed_list = ListLayout("completed",self.parent,self)

        self.all_list = {
            "unfinished":self.unfinished_list,
            "overtime":self.overtime_list,
            "completed":self.completed_list
        }


        main_right_layout.addWidget(self.unfinished_list.container)
        main_right_layout.addWidget(self.overtime_list.container)
        main_right_layout.addWidget(self.completed_list.container)




        # 组合
        main_layout.addWidget(left_form_widget)
        main_layout.addWidget(main_right_widget)

        # 主布局
        main_widget = QWidget(self.parent)
        main_widget.setLayout(main_layout)
        self.parent.setCentralWidget(main_widget)


    def _init_form_widgets(self,parent_layout):
        # 任务名称
        task_name_table = QLabel("任务名称：",self.parent)
        task_name_table.setObjectName("form_key_style")

        self.task_name_line_edit = QLineEdit(self.parent)
        self.task_name_line_edit.setObjectName("form_value_style")
        self.task_name_line_edit.setPlaceholderText("请输入任务名称！")
        parent_layout.addRow(task_name_table, self.task_name_line_edit)

        # 任务截止时间
        task_stop_time = QLabel("截止时间：",self.parent)
        task_stop_time.setObjectName("form_key_style")

        # 时间控件
        self.task_stop_date_edit = QDateTimeEdit(self.parent)
        self.task_stop_date_edit.setObjectName("form_value_style")
        # 开启日历弹窗
        self.task_stop_date_edit.setCalendarPopup(True)
        # 设置时间
        self.task_stop_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        # 设置添加30分钟
        # 获取当前时间
        current_time = QDateTime.currentDateTime()
        # 添加1800秒
        setting_time = current_time.addSecs(1800)
        # 输入的时间
        self.task_stop_date_edit.setDateTime(setting_time)

        parent_layout.addRow(task_stop_time, self.task_stop_date_edit)

        # 重要度
        task_important_label = QLabel("重要程度：",self.parent)
        task_important_label.setObjectName("form_key_style")

        self.task_important_combo_box = QComboBox(self.parent)
        self.task_important_combo_box.setObjectName("form_value_style")

        important_list = FileProcess.read_json_attribute("config/public.json", ["important_map"])
        # print(important_list,"important")
        self.task_important_combo_box.addItems(important_list)
        parent_layout.addRow(task_important_label, self.task_important_combo_box)

        # 类别
        task_category_label = QLabel("选择类别：",self.parent)
        task_category_label.setObjectName("form_key_style")

        self.task_category_combo_box = QComboBox(self.parent)
        self.task_category_combo_box.setObjectName("form_value_style")
        category_list = FileProcess.read_json_attribute("config/public.json", ["category_map"])
        self.task_category_combo_box.addItems(category_list)
        parent_layout.addRow(task_category_label, self.task_category_combo_box)


        # 标签
        task_label_label = QLabel("选择标签：",self.parent)
        task_label_label.setObjectName("form_key_style")

        self.task_label_combo_box = QComboBox(self.parent)
        self.task_label_combo_box.setObjectName("form_value_style")
        label_list = FileProcess.read_json_attribute("config/public.json", ["label_map"])
        self.task_label_combo_box.addItems(label_list)
        parent_layout.addRow(task_label_label, self.task_label_combo_box)


        task_submit_data = QPushButton("创建任务",self.parent)
        task_submit_data.setObjectName("button_style")
        task_submit_data.setFixedWidth(150)



        task_submit_data.clicked.connect(lambda: EventDef.on_create_task(self._get_value(),[self.unfinished_list],self))

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(task_submit_data)
        btn_layout.addStretch()
        parent_layout.addRow(btn_layout)

    def _get_value(self):
        # 判断是不是初次加载
        if not FileProcess.is_root_file("data/tasks.json"):
            logger.debug(f"没有这个目录进行创建-> {'data/tasks.json'}")
            # 获取结构json
            init_structure = FileProcess.read_json_attribute("config/init.json",["start_data"])
            # 创建文件及文件夹，传入结构json
            FileProcess.create_dir_file("data/tasks.json",init_structure)

        # 获取最大唯一 id
        max_id = FileProcess.read_json_attribute("data/tasks.json",["max_id"])

        max_id += 1
        # 写入回去max_id + 1
        FileProcess.write_json_attribute("data/tasks.json",["max_id"],max_id)

        # 创建时间
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 截止时间
        end_time = self.task_stop_date_edit.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        # 计算紧急度
        total_second = TimeProcess.calculate_time_poor(create_time,end_time)
        # print("全部时间",total_second)


        important = self.task_important_combo_box.currentText()
        urgency = AssistantDef.has_urgency(total_second)

        # print(urgency,"紧急度")

        weight_value = CalculateProcess.calculate_task_weight(important,urgency)
        return {
            "id":max_id,
            "name": self.task_name_line_edit.text().strip(),
            "create_time": create_time,
            "end_time": end_time,
            "completed_time":None,
            "important": important,
            "urgency": urgency,
            "category": self.task_category_combo_box.currentText(),
            "label": self.task_label_combo_box.currentText(),
            "weight":weight_value,
            "status": "unfinished",
            "segmentation": []

        }

    def _init_time(self):
        """
        初始化时间定时器
        :return:
        """
        # 实例化
        self.timer = QTimer(self.parent)
        # 设定时间
        self.timer.setInterval(self.timer_ms)
        # 绑定触发方法
        self.timer.timeout.connect(self.auto_refresh_list)
        # 启动
        self.timer.start()

        # logger.info(f"已开始计时器自动刷新数据 -> {self.timer_ms}")


    def is_all_list_overtime(self):
        for task in self.unfinished_list_task_data:
            # print(self.unfinished_list_task_data,"unfinished_list_task_data")
            # 判断超时
            end_time = task.get("end_time",None)

            has_overtime = AssistantDef.is_task_timeout(end_time)
            # print(has_overtime,"我超时了吗",task,"这个任务")
            if has_overtime:
                AssistantDef.task_status_change("overtime",task,"data/tasks.json")
                self.all_list["overtime"].refresh_list()
                self.all_list["unfinished"].refresh_list()

                self.unfinished_list_task_data = AssistantDef.del_list_item_dict(self.unfinished_list_task_data,task)

            # 紧急度提升
            old_urgency = task.get("urgency", None)
            is_update = AssistantDef.is_upgrade_urgency(old_urgency,end_time)
            if is_update:
                # 修改紧急度
                task["urgency"] = is_update

                # 修改权重
                # 重要度
                important_value = task.get("important",None)
                # 权重值
                weight_value = CalculateProcess.calculate_task_weight(important_value,is_update)
                task["weight"] = weight_value

                FileProcess.write_json_attribute("data/tasks.json",["unfinished_list"],self.unfinished_list_task_data)
                self.all_list["unfinished"].refresh_list()




    def auto_refresh_list(self):
        self.all_list["unfinished"].refresh_list()
        self.all_list["overtime"].refresh_list()
        self.is_all_list_overtime()
