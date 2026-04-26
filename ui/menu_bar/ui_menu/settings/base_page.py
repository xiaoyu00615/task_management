from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from compents.load_path import config_manager,load_path

class BasePage(QWidget):

    def __init__(self,title):
        super().__init__()
        self.setting_config = config_manager.get_entity_config(path_key="menu_bar/settings")
        self.title = title
        self._init_ui()

    def _init_ui(self):

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # 初始标题
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("title_label")
        self.main_layout.addWidget(self.title_label)

        self.main_content_widget = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        self.main_content_layout.setSpacing(20)
        self.main_layout.addWidget(self.main_content_widget)

        # 滚动区域
        self.content_scroll = QScrollArea()  # 滚动区域

        self.content_scroll.setWidgetResizable(True)  # 自适应内容高度
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭横向滚动（关键：避免宽度拉伸）
        self.content_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 纵向滚动按需显示
        self.content_scroll.setWidget(self.main_content_widget)
        self.main_layout.addWidget(self.content_scroll)