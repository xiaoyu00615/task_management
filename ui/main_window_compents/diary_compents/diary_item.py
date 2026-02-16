from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from compents.str_process import StrProcess
from ui.main_window_compents.toggle_event.diary_event import DiaryEvent

class DiaryItem:

    @staticmethod
    def create_diary_item(this,this_list,data_dict,parent):
        diary_item_weight = QWidget()

        diary_item_layout = QVBoxLayout(diary_item_weight)

        title_label = QLabel(f"标题：{StrProcess.specify_str_num_pad(data_dict["title"],15,"...")}")
        diary_item_layout.addWidget(title_label)

        small_label = QLabel(f"简述：{StrProcess.specify_str_num_pad(data_dict["small"],8,"...")}")
        diary_item_layout.addWidget(small_label)

        line_weight = QWidget()
        line_layout = QHBoxLayout(line_weight)
        line_layout.setContentsMargins(0,0,0,0)
        diary_item_layout.addWidget(line_weight)

        emotion_label = QLabel(f"心情：{StrProcess.specify_str_num_pad(data_dict["emotion"],5,"...")}")
        line_layout.addWidget(emotion_label)

        weather_label = QLabel(f"天气：{StrProcess.specify_str_num_pad(data_dict["weather"],5,"...")}")
        line_layout.addWidget(weather_label)

        content_label = QLabel(f"内容：{StrProcess.specify_str_num_pad(data_dict["content"],30,"...")}")
        content_label.setWordWrap(True)
        diary_item_layout.addWidget(content_label)

        create_label = QLabel(data_dict["create_time"])
        diary_item_layout.addWidget(create_label)

        btn_weight = QWidget()
        btn_layout = QHBoxLayout(btn_weight)

        # 详情
        details_diary = QPushButton("详情")
        print("详情数据",data_dict)
        details_diary.clicked.connect(lambda:DiaryEvent.no_details_diary(this,this_list,data_dict,parent))
        btn_layout.addWidget(details_diary)

        # 收藏
        collection_diary = QPushButton("收藏")
        collection_diary.clicked.connect(lambda: DiaryEvent.no_collection_diary(this,this_list,data_dict))
        btn_layout.addWidget(collection_diary)


        # 删除
        del_diary = QPushButton("删除")
        del_diary.clicked.connect(lambda: DiaryEvent.no_del_diary(this,this_list,data_dict))
        btn_layout.addWidget(del_diary)


        diary_item_layout.addWidget(btn_weight)


        return diary_item_weight