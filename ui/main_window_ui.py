import datetime

from PyQt5.QtCore import QDateTime, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QComboBox, QDateTimeEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QStackedWidget

from compents.log import logger
from compents.file_process import FileProcess
from compents.time_process import TimeProcess
from compents.calculate_process import CalculateProcess

from ui.main_window_compents.event_def import EventDef
from ui.uilt.assistant_def import AssistantDef
from ui.main_window_compents.toggle_page.chat_page import ChatPage
from ui.main_window_compents.toggle_page.task_page import TaskPage
from ui.main_window_compents.toggle_page.diary_page import DiaryPage
from compents.load_path import load_path


class MainWindowUI(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.unfinished_list_task_data = []
        self.timer_ms = load_path["time"]["data_refresh"]
        self.all_list = {}
        logger.info("主窗口UI控件类")
        self._init_ui()
        self._init_time()

    def _init_ui(self):
        logger.info("正在创建MainWindowUI")

        # 主布局
        main_layout = QHBoxLayout()

        # 顶部切换栏
        switch_bar = QWidget()
        switch_bar.setContentsMargins(0,0,0,0)

        switch_bar.setFixedWidth(150)

        switch_bar.setObjectName("toggle_border")
        switch_layout = QVBoxLayout(switch_bar)
        switch_layout.setSpacing(0)

        # 页面：
        page_title = QLabel("页面-切换")
        page_title.setObjectName("toggle_title")
        page_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        switch_layout.addWidget(page_title)

        # 查看任务项
        self.task_btn = QPushButton("任务")
        self.task_btn.setCheckable(True)
        self.task_btn.setChecked(True)
        self.task_btn.setObjectName("toggle_btn")
        self.task_btn.clicked.connect(lambda: self._switch_page(0))

        # AI 聊天按钮
        self.chat_btn = QPushButton("AI聊天")
        self.chat_btn.setCheckable(True)
        self.chat_btn.setObjectName("toggle_btn")
        self.chat_btn.clicked.connect(lambda:self._switch_page(1))

        # 日记按钮
        self.diary_btn = QPushButton("日记")
        self.diary_btn.setCheckable(True)
        self.diary_btn.setObjectName("toggle_btn")
        self.diary_btn.clicked.connect(lambda:self._switch_page(2))


        switch_layout.addWidget(self.task_btn)
        switch_layout.addWidget(self.chat_btn)
        switch_layout.addWidget(self.diary_btn)
        switch_layout.addStretch()

        # 创建内容窗口
        self.stacked_weight = QStackedWidget(self.parent)
        self.stacked_weight.setContentsMargins(0,0,0,0)

        # 第一个页面
        # 任务管理页面
        task_page = TaskPage(self)
        self.task_page = task_page.task_container
        self.stacked_weight.addWidget(self.task_page)

        # AI 聊天页面
        chat_page = ChatPage(self.parent)
        self.chat_page = chat_page.chat_container
        self.stacked_weight.addWidget(self.chat_page)

        # 日记页面
        self.new_diary_page = DiaryPage(self.parent)
        self.diary_page = self.new_diary_page.diary_container
        self.stacked_weight.addWidget(self.diary_page)


        # 组合布局
        main_layout.addWidget(switch_bar)
        main_layout.addWidget(self.stacked_weight)

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

        important_list = FileProcess.read_json_attribute(load_path["data_map"], ["important_map"])
        # print(important_list,"important")
        self.task_important_combo_box.addItems(important_list)
        parent_layout.addRow(task_important_label, self.task_important_combo_box)

        # 类别
        task_category_label = QLabel("选择类别：",self.parent)
        task_category_label.setObjectName("form_key_style")

        self.task_category_combo_box = QComboBox(self.parent)
        self.task_category_combo_box.setObjectName("form_value_style")
        category_list = FileProcess.read_json_attribute(load_path["data_map"], ["category_map"])
        self.task_category_combo_box.addItems(category_list)
        parent_layout.addRow(task_category_label, self.task_category_combo_box)


        # 标签
        task_label_label = QLabel("选择标签：",self.parent)
        task_label_label.setObjectName("form_key_style")

        self.task_label_combo_box = QComboBox(self.parent)
        self.task_label_combo_box.setObjectName("form_value_style")
        label_list = FileProcess.read_json_attribute(load_path["data_map"], ["label_map"])
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
        if not FileProcess.is_root_file(load_path["store"]["task"]):
            logger.debug(f"没有这个目录进行创建-> {load_path["store"]["task"]}")
            # 获取结构json
            init_structure = FileProcess.read_json_attribute(load_path["template"],["start_data"])
            # 创建文件及文件夹，传入结构json
            FileProcess.create_dir_file(load_path["store"]["task"],init_structure)

        # 获取最大唯一 id
        max_id = FileProcess.read_json_attribute(load_path["store"]["task"],["max_id"])

        max_id += 1
        # 写入回去max_id + 1
        FileProcess.write_json_attribute(load_path["store"]["task"],["max_id"],max_id)

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

        obj = {
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
        self.task_name_line_edit.setText("")
        return obj

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
        # print(self.unfinished_list_task_data,"self.unfinished_list_task_data")
        for task in self.unfinished_list_task_data:
            # print(self.unfinished_list_task_data,"unfinished_list_task_data")
            # 判断超时
            end_time = task.get("end_time",None)

            has_overtime = AssistantDef.is_task_timeout(end_time)
            # print(has_overtime,"我超时了吗",task,"这个任务")
            if has_overtime:
                AssistantDef.task_status_change("overtime",task,load_path["store"]["task"])
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

                FileProcess.write_json_attribute(load_path["store"]["task"],["unfinished_list"],self.unfinished_list_task_data)
                self.all_list["unfinished"].refresh_list()




    def auto_refresh_list(self):
        self.all_list["unfinished"].refresh_list()
        self.all_list["overtime"].refresh_list()
        self.is_all_list_overtime()

        # 日记页实时日期
        now_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H时%M分%S秒')
        now_week = TimeProcess.now_week()
        self.new_diary_page.now_time_label.setText(f"{now_time} · {now_week}")





    def _switch_page(self,index):
        # 切换页面
        self.stacked_weight.setCurrentIndex(index)

        # 更新状态
        self.task_btn.setChecked(index == 0)
        self.chat_btn.setChecked(index == 1)
        self.diary_btn.setChecked(index == 2)