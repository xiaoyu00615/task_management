from compents import load_path
from compents.file_process import FileProcess
from ui.menu_bar.ui_menu.menu_bar.setting_window import SettingWindow
from compents.load_path import config_manager
from compents_pyqt5.pyqt5_set_timer import Pyqt5SetTimer

class SettingsEvent:
    setting_path = config_manager.get_entity_config(path_key="menu_bar/settings")

    @staticmethod
    def on_basic_setting(index):
        # 点击基本设置
        print("点击基本设置")
        setting_window = SettingWindow(index)
        setting_window.exec()

    @classmethod
    def on_auto_backup_switch(cls, checked):
        """
        开关状态变化的槽函数（补全True/False分支逻辑）
        :param checked: 开关新状态（int：0=关/2=开；bool：True=开/False=关）
        """
        # 统一转换为布尔值
        if isinstance(checked, int):
            checked = checked == 2

        # ========== 1. 修改配置（全局同步+持久化） ==========
        config_manager.update_entity_config(
            new_value=checked,
            path_key="menu_bar/settings",
            config_key_path="backup/auto_backup"
        )

        # ========== 2. 分状态处理计时器（核心补全逻辑） ==========
        if checked:
            # 分支1：开关开启 → 初始化/更新自动备份计时器
            # 读取配置中的备份间隔（分钟 → 毫秒）
            backup_minute = cls.setting_path["backup"]["backup_time_minute"]
            backup_ms = backup_minute * 60 * 1000

            # 初始化/重启计时器（复用已有实例，自动更新间隔）
            Pyqt5SetTimer.init_task_timer(
                task_id=cls.setting_path["backup"]["auto_backup_id_name"],
                timer_ms=backup_ms,
                call_back=cls.auto_backup_callback,
                parent=None  # 实际使用时传入你的窗口实例（如self/setting_window）
            )
        else:
            # 分支2：开关关闭 → 停止并删除计时器（彻底释放内存）
            Pyqt5SetTimer.stop_task_timer(cls.setting_path["backup"]["auto_backup_id_name"])
            Pyqt5SetTimer.remove_task_timer(cls.setting_path["backup"]["auto_backup_id_name"])

        # ========== 3. 用户提示 ==========
        tip = "开启" if checked else "关闭"
        print(f"自动备份已{tip}，配置已保存并同步，计时器已{tip}")

    @classmethod
    def auto_backup_callback(cls):
        """自动备份的回调函数（每次触发时读取最新数据）"""
        try:
            # 每次备份都读取最新的任务数据（修正静态数据问题）
            task_json = FileProcess.read_json(load_path["store"]["task"])
            # 备份时间：分钟转毫秒
            auto_backup_timer = cls.setting_path["backup"]["backup_time_minute"]
            auto_backup_second = auto_backup_timer * 60 * 1000
            # 备份路径
            save_path = cls.setting_path["backup"]["backup_dir"]
            # 执行备份
            cls.backup_json(task_json, save_path)
            print(f"自动备份成功，备份路径：{save_path}")
        except Exception as e:
            print(f"自动备份失败：{e}")  # 异常捕获，避免计时器崩溃