import datetime

from PyQt5.QtCore import QDateTime, qQNaN, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QFormLayout, QWidget, QLineEdit, QDateEdit, QComboBox, QDateTimeEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QStackedWidget, QTextEdit, QScrollArea, QListWidget, QFrame, QListWidgetItem

from compents.log import logger
from compents.file_process import FileProcess
from compents.time_process import TimeProcess
from compents.calculate_process import CalculateProcess
from compents.str_process import StrProcess
from ui.main_window_compents.list_layout import ListLayout
from ui.main_window_compents.event_def import EventDef
from ui.uilt.assistant_def import AssistantDef
from ui.main_window_compents.diary_compents.list_weight import ListWeight
from ui.main_window_compents.toggle_event.diary_event import DiaryEvent
from compents.load_path import load_path

class DiaryPage:
    def __init__(self,parent):
        self.diary_dict = FileProcess.read_json(load_path["store"]["diary"])
        self.parent = parent
        self._init_ui()


    def _init_ui(self):
        """初始化日记页面UI"""
        logger.info("初始化日记页面UI")
        # 主布局
        self.diary_container = QWidget()
        self.diary_container_layout = QHBoxLayout(self.diary_container)

        # 写区域：
        self.write_diary_block = QWidget()
        self.write_diary_block.setFixedWidth(500)
        self.write_diary_block.setObjectName("diary_block_weight")
        self.write_diary_block_layout = QVBoxLayout(self.write_diary_block)

        # 将写区域放入主布局
        self.diary_container_layout.addWidget(self.write_diary_block)

        now_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H时%M分%S秒')
        now_week = TimeProcess.now_week()
        self.now_time_label = QLabel(f"{now_time} · {now_week}")
        self.now_time_label.setObjectName("now_time_label")

        self.write_diary_block_layout.addWidget(self.now_time_label)

        # 块
        self.title_block = QWidget()
        self.title_block.setContentsMargins(0,0,0,0)
        self.title_block_layout = QVBoxLayout(self.title_block)
        self.title_block_layout.setContentsMargins(0,3,0,3)
        self.write_diary_block_layout.addWidget(self.title_block)

        # 标题
        diary_title_label = QLabel("这一天，想给它起个什么样的名字呢？")
        diary_title_label.setObjectName("label_style")
        self.title_block_layout.addWidget(diary_title_label)

        # 输入框
        self.diary_title_entry = QLineEdit()
        self.diary_title_entry.setPlaceholderText("用一个词，为今天的时光命名吧。")
        self.diary_title_entry.setObjectName("entry_style")
        self.title_block_layout.addWidget(self.diary_title_entry)

        # 块
        small_block = QWidget()
        small_block.setContentsMargins(0,0,0,0)
        small_block_layout = QVBoxLayout(small_block)
        small_block_layout.setContentsMargins(0,3,0,3)
        self.write_diary_block_layout.addWidget(small_block)
        # 小记
        diary_small_label = QLabel("有没有遇到什么小小的、让你心头一暖的小事呀？")
        diary_small_label.setObjectName("label_style")
        small_block_layout.addWidget(diary_small_label)

        # 输入框
        self.diary_small_entry = QLineEdit()
        self.diary_small_entry.setPlaceholderText("有什么让你忍不住嘴角上扬的瞬间吗？")
        self.diary_small_entry.setObjectName("entry_style")
        small_block_layout.addWidget(self.diary_small_entry)

        # 块
        emotion_block = QWidget()
        emotion_block.setContentsMargins(0,0,0,0)
        emotion_block_layout = QVBoxLayout(emotion_block)
        emotion_block_layout.setContentsMargins(0,3,0,3)
        self.write_diary_block_layout.addWidget(emotion_block)
        # 心情
        diary_emotion_label = QLabel("此刻的心情，像一首什么样的小诗呢？")
        diary_emotion_label.setObjectName("label_style")
        emotion_block_layout.addWidget(diary_emotion_label)

        # 输入框
        self.diary_emotion_entry = QLineEdit()
        self.diary_emotion_entry.setPlaceholderText("试着描述一下，此刻心里的感受是什么样的？")
        self.diary_emotion_entry.setObjectName("entry_style")
        emotion_block_layout.addWidget(self.diary_emotion_entry)

        # 块
        weather_block = QWidget()
        weather_block.setContentsMargins(0,0,0,0)
        weather_block_layout = QVBoxLayout(weather_block)
        weather_block_layout.setContentsMargins(0,3,0,3)
        self.write_diary_block_layout.addWidget(weather_block)

        # 天气
        diary_weather_label = QLabel("天气，像一首什么样的歌呢？")
        diary_weather_label.setObjectName("label_style")
        weather_block_layout.addWidget(diary_weather_label)

        # 输入框
        self.diary_weather_entry = QLineEdit()
        self.diary_weather_entry.setPlaceholderText("你眼里的天气，是什么模样的呢？")
        self.diary_weather_entry.setObjectName("entry_style")
        weather_block_layout.addWidget(self.diary_weather_entry)

        # 块
        content_block = QWidget()
        content_block.setContentsMargins(0,0,0,0)
        content_block_layout = QVBoxLayout(content_block)
        content_block_layout.setContentsMargins(0,3,0,3)
        self.write_diary_block_layout.addWidget(content_block)

        # 内容
        diary_content_label = QLabel("你想写一个什么故事呢？")
        diary_content_label.setObjectName("label_style")
        content_block_layout.addWidget(diary_content_label)

        # 多行输入框
        self.diary_content_text = QTextEdit()
        self.diary_content_text.setPlaceholderText("把今天的故事、感受都写下来吧...")
        self.diary_content_text.setObjectName("entry_style")
        content_block_layout.addWidget(self.diary_content_text)

        # 我写完啦
        write_ok = QPushButton()
        write_ok.setFixedWidth(200)
        write_ok.setText("我写完啦... -> 存起来！")
        write_ok.setObjectName("write_ok")
        write_ok.clicked.connect(lambda: DiaryEvent.on_create_diary_item(self,self.get_int_data()))
        self.write_diary_block_layout.addWidget(write_ok)

        self.write_diary_block_layout.addStretch()

        # =========================================================================

        # 看区域
        self.look_diary_block = QWidget()
        self.look_diary_block_layout = QHBoxLayout(self.look_diary_block)

        # 普通区域
        self.ordinary_list_weight = ListWeight(self,self.diary_dict,"ordinary_list",self.parent)
        self.look_diary_block_layout.addWidget(self.ordinary_list_weight.list_container)


        # 收藏区域
        self.collection_list_weight = ListWeight(self,self.diary_dict,"collection_list",self.parent)
        self.look_diary_block_layout.addWidget(self.collection_list_weight.list_container)


        # 将看区域放入主布局
        self.diary_container_layout.addWidget(self.look_diary_block)



    def get_int_data(self):


        # 获取最大唯一 id
        max_id = FileProcess.read_json_attribute(load_path["store"]["diary"], ["max_id"])

        max_id += 1

        obj = {
            "id": max_id,
            "title":self.diary_title_entry.text().strip(),
            "small":self.diary_small_entry.text().strip(),
            "emotion":self.diary_emotion_entry.text().strip(),
            "weather":self.diary_weather_entry.text().strip(),
            "content":self.diary_content_text.toPlainText().strip(),
            "create_time":self.now_time_label.text().strip(),
            "create_stamp":datetime.datetime.now().timestamp(),
            "type":"ordinary",
            "reading_num":0
        }

        self.diary_title_entry.setText("")
        self.diary_small_entry.setText("")
        self.diary_emotion_entry.setText("")
        self.diary_weather_entry.setText("")
        self.diary_content_text.setText("")

        return obj


