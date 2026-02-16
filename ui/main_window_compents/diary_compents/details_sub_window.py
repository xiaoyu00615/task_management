from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class DetailsSubWindow(QDialog):
    def __init__(self,parent,data):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        self._init_ui()

    def _init_ui(self):
        # print("实例了窗口")
        self.setWindowTitle(f"日记详情 -- {self.data.get('title',None)}")
        self.setFixedSize(650, 550)

        # 主窗口
        # main_widget = QWidget()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15,10,15,10)


        title_label = QLabel(f"{self.data.get('title',None)}")
        title_label.setAlignment(Qt.AlignHCenter)
        title_label.setObjectName("title")
        self.main_layout.addWidget(title_label)

        small_label = QLabel(f"{self.data.get('small',None)}")
        small_label.setWordWrap(True)
        small_label.setObjectName("small")
        self.main_layout.addWidget(small_label)

        emotion_label = QLabel(f"{self.data.get('emotion',None)}")
        emotion_label.setObjectName("emotion")

        self.main_layout.addWidget(emotion_label)

        weather_label = QLabel(f"{self.data.get('weather',None)}")
        weather_label.setObjectName("weather")
        self.main_layout.addWidget(weather_label)

        content_label = QLabel(f"{self.data.get('content',None)}")
        content_label.setWordWrap(True)
        content_label.setMidLineWidth(15)
        content_label.setIndent(2)
        content_label.setObjectName("content")
        self.main_layout.addWidget(content_label)

        reading_num_label = QLabel(f"阅读( {self.data.get('reading_num', None)} )次")
        reading_num_label.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(reading_num_label)

        create_time = QLabel(f"{self.data.get('create_time',None)}")
        create_time.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(create_time)



        self.main_layout.addStretch()

