from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QProgressBar
from ui.main_window_compents.event_def import EventDef
from compents.calculate_process import CalculateProcess
from compents.time_process import TimeProcess
import datetime
from compents.file_process import FileProcess
from compents.str_process import StrProcess

class ItemWidget(QWidget):
    def __init__(self,task,list_layout,parent,index):
        super().__init__(parent)
        self.parent = parent
        self.list_layout = list_layout
        self.task = task
        self.status = self.task.get("status", None)
        # print(self.status,"ItemWidget_status")
        self.index = index

        # 获取数据
        self.color_map = FileProcess.read_json('config/public.json')
        self.important_color_map = self.color_map.get("importance_color_map",{"1": "#AAAAAA","2": "#777777","3": "#4488FF","4": "#4444FF"})
        self.urgency_color_map = self.color_map.get("urgency_color_map",{"0": "#666666","1": "#FF4444","2": "#FF7744", "3": "#FFAA44","4": "#FFDD44","5": "#FFFF44","6": "#DDFF44","7": "#AAFF44","8": "#77FF44", "9": "#44FF44","10": "#AAAAAA"})

        self.urgency_value = self.task.get('urgency', None)
        self.important_value = self.task.get('important', None)

        self.urgency_num = f"{StrProcess.get_str_inside_num(self.urgency_value)}"
        self.important_num = f"{StrProcess.get_str_inside_num(self.important_value)}"

        self._init_ui()




    def _init_ui(self):

        self.main_item_layout = QWidget()

        self.main_item_layout.setObjectName("item_style")
        item_main_layout = QHBoxLayout(self.main_item_layout)
        item_main_layout.setContentsMargins(5,5,5,8)
        item_main_layout.setSpacing(0)
        # 任务项ui
        self._init_item(item_main_layout)

    def _init_item(self,item_content_layout):
        item_content_widget = QWidget()
        color_content_widget = QWidget()
        color_content_widget.setFixedWidth(25)

        color_layout = QHBoxLayout(color_content_widget)
        color_layout.setContentsMargins(5,5,5,5)
        color_layout.setSpacing(0)

        content_layout = QVBoxLayout(item_content_widget)
        content_layout.setContentsMargins(5,5,5,5)
        content_layout.setSpacing(6)

        self._init_color_block(color_layout)


        # 任务名称
        name_label = QLabel(f"{self.index + 1}、{self.task.get('name', None)}")
        name_label.setObjectName("title_name")
        content_layout.addWidget(name_label)

        # 重要度
        important_label = QLabel(f"重要度：{self.important_value}")
        important_label.setStyleSheet(f"""
            color:{self.important_color_map.get(self.important_num)}
        """)

        content_layout.addWidget(important_label)

        # 紧急度
        urgency_label = QLabel(f"紧急度：{self.urgency_value}")
        urgency_label.setStyleSheet(f"""
            color:{self.urgency_color_map.get(self.urgency_num)["solid"]
        }""")
        content_layout.addWidget(urgency_label)

        # 比例权重
        weight_label = QLabel(f"比例权重：{self.task.get('weight', None)}")
        content_layout.addWidget(weight_label)


        # 类别
        category_label = QLabel(f"类别：{self.task.get('category', None)}")
        content_layout.addWidget(category_label)

        # 标签
        label_label = QLabel(f"标签：{self.task.get('label', None)}")
        content_layout.addWidget(label_label)

        # 创建时间
        create_time_value = self.task.get('create_time', None)
        create_time_label = QLabel(f"创建时间：{create_time_value}")
        create_time_label.setStyleSheet(f"""color:#388E3C;""")
        content_layout.addWidget(create_time_label)

        # 截止时间
        end_time_value = self.task.get('end_time', None)
        end_time_label = QLabel(f"截止时间：{end_time_value}")
        end_time_label.setStyleSheet(f"""color:#a10028 ;""")
        content_layout.addWidget(end_time_label)



        if self.status == "unfinished":
            # 剩余时间
            now_time = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            total_seconde = TimeProcess.calculate_time_poor(now_time, end_time_value)
            format_time = TimeProcess.seconde_format(total_seconde)
            remaining_time = QLabel(f"剩余时间：{format_time}")
            remaining_time.setStyleSheet(f"""
                        color:{self.urgency_color_map.get(self.urgency_num)["solid"]
            }""")
            content_layout.addWidget(remaining_time)

            # 进度条
            self.progress_bar = QProgressBar()
            # 范围
            self.progress_bar.setRange(0,100)
            # 初始进度
            progress_value = TimeProcess.get_time_percent(create_time_value,end_time_value)
            self.progress_bar.setValue(progress_value)
            # 显示进度文字
            self.progress_bar.setTextVisible(True)
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                /* 进度条整体（下层：50%透明度背景） */
                background-color: {self.urgency_color_map.get(self.urgency_num)["transparent_50"]};
                border: none;          /* 去掉默认边框 */
                border-radius: 12px;   /* 圆角（可选，按需调整） */
                text-align: center;    /* 进度文字居中 */
                color: white;          /* 进度文字颜色（白色更清晰） */
                font-size: 12px;       /* 文字大小 */
                }}
                QProgressBar::chunk {{
                    /* 进度条已完成部分（上层：鲜艳实色） */
                    background-color: {self.urgency_color_map.get(self.urgency_num)["solid"]};
                    border-radius: 12px;   /* 和整体圆角一致 */
                }}
            """)

            content_layout.addWidget(self.progress_bar)

        # 专属超时内容
        if self.status == "overtime":
            # 超时时间
            timeout_now_time = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            timeout_total_seconde = TimeProcess.calculate_time_poor(end_time_value,timeout_now_time)
            timeout_format_time = TimeProcess.seconde_format(timeout_total_seconde)
            timeout_remaining_time = QLabel(f"超时时间：{timeout_format_time}")
            timeout_remaining_time.setStyleSheet(f"""color:#ED6C02""")
            content_layout.addWidget(timeout_remaining_time)

        # 已完成专属内容
        if self.status == "completed":
            completed_time = self.task.get('completed_time', None)
            # 跳过老版本生成时间
            if not completed_time is None:

                timeout_total_seconde = TimeProcess.calculate_time_poor(completed_time,end_time_value)
                if timeout_total_seconde > 0:
                    # 预期完成
                    expectation_format_time = TimeProcess.seconde_format(timeout_total_seconde)
                    expectation_com = QLabel(f"预期完成提前：{expectation_format_time}")
                    expectation_com.setStyleSheet(f"""color:#0288D1""")
                    content_layout.addWidget(expectation_com)
                if timeout_total_seconde <= 0:
                    # 超时完成
                    timeout_total_seconde = TimeProcess.calculate_time_poor(end_time_value,completed_time)
                    timeout_format_time = TimeProcess.seconde_format(timeout_total_seconde)
                    timeout_com = QLabel(f"逾期完成超时：{timeout_format_time}")
                    timeout_com.setStyleSheet(f"""color:#C2185B""")
                    content_layout.addWidget(timeout_com)




        # 按钮QWidget
        btn_widget = QWidget()
        btn_widget.setContentsMargins(0,0,0,0)

        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setSpacing(5)

        # 细分
        segmentation = QPushButton("细分")
        segmentation.clicked.connect(lambda : EventDef.on_segmentation_task(self.parent,self.task))

        btn_layout.addWidget(segmentation)

        # 删除
        del_btn = QPushButton("删除")
        del_btn.clicked.connect(lambda: EventDef.on_del_task(self.task,[self.parent]))
        # 完成
        complete_btn = QPushButton("完成")
        complete_btn.clicked.connect(lambda: EventDef.on_complete_task(self.task,self.list_layout.values()))

        btn_layout.addWidget(del_btn)

        btn_layout.addWidget(complete_btn)
        content_layout.addWidget(btn_widget)

        item_content_layout.addWidget(color_content_widget)
        item_content_layout.addWidget(item_content_widget)

        content_layout.addStretch()

    def _init_color_block(self,item_color_layout):

        color_block = QWidget()
        color_block.setFixedWidth(8)
        color_block.setObjectName("color_block")


        color_block.setStyleSheet(f"""
            background-color:{self.urgency_color_map.get(self.urgency_num)["solid"]};
        """)

        item_color_layout.addWidget(color_block)
        item_color_layout.addStretch()

