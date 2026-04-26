from PyQt5.QtWidgets import QAction
from ui.menu_bar.ui_menu.setting_event import SettingsEvent

class MenuUi:
    def __init__(self, parent):
        self.parent = parent
        self._init_ui()

    def _init_ui(self):
        menubar = self.parent.menuBar()
        menubar.setNativeMenuBar(False)

        # 文件项
        file_menu = menubar.addMenu("文件")

        # 数据保存
        data_save = QAction("数据保存", self.parent)
        data_save.setShortcut("Ctrl+;") # 绑定文件菜单事件
        file_menu.addAction(data_save)

        # 分隔线
        file_menu.addSeparator()

        # 退出程序
        exit_action = QAction("退出", self.parent)
        exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(exit_action)



        # 设置项
        settings_menu = menubar.addMenu("设置")

        # 基本设置
        foundation = QAction("基本设置", self.parent)
        foundation.setShortcut("Ctrl+H")
        foundation.triggered.connect(lambda:SettingsEvent.on_basic_setting(0))
        settings_menu.addAction(foundation)

        # 备份与恢复
        backup_and_recovery = QAction("备份与恢复", self.parent)
        backup_and_recovery.setShortcut("Ctrl+B")
        backup_and_recovery.triggered.connect(lambda:SettingsEvent.on_basic_setting(1))
        settings_menu.addAction(backup_and_recovery)

        # 外观设置
        appearance = QAction("外观设置", self.parent)
        appearance.triggered.connect(lambda:SettingsEvent.on_basic_setting(2))
        appearance.setShortcut("Ctrl+A")
        settings_menu.addAction(appearance)

        # 通知设置
        notice = QAction("通知设置", self.parent)
        notice.setShortcut("Ctrl+N")
        notice.triggered.connect(lambda:SettingsEvent.on_basic_setting(3))
        settings_menu.addAction(notice)

        # 数据更新设置
        update = QAction("数据更新设置", self.parent)
        update.setShortcut("Ctrl+U")
        update.triggered.connect(lambda:SettingsEvent.on_basic_setting(4))
        settings_menu.addAction(update)

        # 快捷键
        shortcut_key = QAction("快捷键设置", self.parent)
        shortcut_key.setShortcut("Ctrl+K")
        shortcut_key.triggered.connect(lambda: SettingsEvent.on_basic_setting(5))
        settings_menu.addAction(shortcut_key)
