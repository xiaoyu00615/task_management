import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout,
    QFormLayout, QLineEdit, QPushButton, QTextEdit, QScrollArea,
    QListWidget, QListWidgetItem, QStackedWidget, QCheckBox, QSpinBox,
    QGroupBox, QMessageBox
)
from ..settings.basic_page import BasicPage
from ..settings.backup_page import BackUpPage
from ..settings.appearance_page import AppearancePage
from ..settings.notification_page import NotificationPage
from ..settings.data_update_page import DataUpdatePage

# 保留你原有的导入
from compents.file_process import FileProcess
from ui.main_window_compents.event_modal_segmentation import EventModalSegmentation
from compents.load_path import load_path
from ..settings.shortcut_page import ShortcutPage


class SettingWindow(QDialog):
    def __init__(self, index):
        super().__init__()
        self.index = index  # 保留传入的索引参数，不删除
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(f"设置")
        self.setFixedSize(750, 650)
        self.setModal(True)

        # ========== 主布局容器 ==========
        main_widget = QWidget()
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # ========== 1. 左侧导航（先创建，但临时屏蔽信号触发） ==========
        self._init_left_nav()

        # ========== 2. 右侧页面容器（创建page_container） ==========
        self._init_right_pages()

        # ========== 3. 关键：page_container创建后，触发默认选中（保留self.index） ==========
        self.nav_list.setCurrentRow(self.index)  # 此时page_container已存在，触发切换不报错

        # ========== 设置主窗口的中心部件 ==========
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(main_widget)

    def _init_left_nav(self):
        """初始化左侧导航（临时不触发信号）"""
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("background-color: #f5f5f5;")

        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                border: none;
                font-size: 14px;
                outline: none;
            }
            QListWidget::item {
                height: 45px;
                text-align: center;
                padding: 5px;
                border: none;
            }
            QListWidget::item:hover {
                background-color: #e8f4ff;
                color: #409eff;
            }
            QListWidget::item:selected {
                background-color: #409eff;
                color: white;
                border: none;
            }
        """)

        # 导航项
        nav_items = ["基本设置", "备份与恢复", "外观设置", "通知设置","数据更新设置","快捷键设置"]
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignCenter)
            self.nav_list.addItem(item)

        # ========== 关键修改：先绑定信号，但初始化时不主动触发（把setCurrentRow移到_init_ui最后） ==========
        self.nav_list.currentRowChanged.connect(self._switch_page)

        # 注意：这里不再设置self.nav_list.setCurrentRow(self.index)，移到page_container创建后

        nav_layout.addWidget(self.nav_list)
        self.main_layout.addWidget(nav_widget)  # 布局顺序不变，左侧先加

    def _init_right_pages(self):
        """初始化右侧页面（创建page_container）"""
        self.page_container = QStackedWidget()
        self.page_container.setContentsMargins(15,15,15,15)
        self.page_container.setStyleSheet("background-color: white;")

        # 添加各页面
        basic_page = BasicPage("基本介绍")
        self.page_container.addWidget(basic_page.main_widget)

        backup_page = BackUpPage("备份与恢复")
        self.page_container.addWidget(backup_page.main_widget)

        appearance_page = AppearancePage("外观与个性化")
        self.page_container.addWidget(appearance_page.main_widget)

        notification_page = NotificationPage("通知与消息")
        self.page_container.addWidget(notification_page.main_widget)

        data_update_page = DataUpdatePage("数据更新")
        self.page_container.addWidget(data_update_page.main_widget)

        shortcut_page = ShortcutPage("快捷键设置")
        self.page_container.addWidget(shortcut_page.main_widget)

        self.main_layout.addWidget(self.page_container)  # 布局顺序不变，右侧后加

    def _switch_page(self, index):
        """切换页面（此时page_container已存在）"""
        self.page_container.setCurrentIndex(index)