import json
import os
import time
from datetime import datetime
from compents.file_process import FileProcess


class BackupJsonData:
    root_path = FileProcess.ROOT_FILE


    @staticmethod
    def backup_json(config_data, backup_dir=None, keep_history=True):
        """
        备份JSON格式的配置数据
        :param config_data: 要备份的配置字典
        :param backup_dir: 备份目录
        :param keep_history: 是否保留历史备份（True=生成带时间戳的文件名，False=覆盖同名文件）
        :return: 备份文件路径（成功）/None（失败）
        """
        # 1. 处理备份目录
        if backup_dir is None:
            return False

        if not backup_dir:
            return False

        if not os.path.exists(backup_dir):
            try:
                os.makedirs(backup_dir)  # 创建目录（包括多级）
            except Exception as e:
                print(f"创建备份目录失败：{e}")
                return None

        # 2. 生成备份文件名
        if keep_history:
            # 带时间戳的文件名（格式：20260223_153020_config_backup.json）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{timestamp}_config_backup.json"
        else:
            # 固定文件名（会覆盖旧文件）
            backup_filename = "config_backup.json"

        backup_file_path = os.path.join(BackupJsonData.root_path,backup_dir, backup_filename)

        # 3. 写入JSON文件（格式化输出，保证可读性）
        try:
            with open(backup_file_path, "w", encoding="utf-8") as f:
                # indent=4：格式化缩进，ensure_ascii=False：支持中文（如果有）
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            print(f"配置备份成功！文件路径：{backup_file_path}")
            return backup_file_path
        except PermissionError:
            print(f"权限不足，无法写入备份文件：{backup_file_path}")
        except Exception as e:
            print(f"备份配置失败：{e}")
        return None

    @staticmethod
    def restore_json(backup_file_path):
        """
        从备份文件恢复配置
        :param backup_file_path: 备份文件的路径
        :return: 恢复的配置字典（成功）/None（失败）
        """
        if not os.path.exists(backup_file_path):
            print(f"备份文件不存在：{backup_file_path}")
            return None

        try:
            with open(backup_file_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            print(f"配置恢复成功！从文件：{backup_file_path}")
            return config_data
        except json.JSONDecodeError:
            print(f"备份文件格式错误，无法解析：{backup_file_path}")
        except Exception as e:
            print(f"恢复配置失败：{e}")
        return None


# ==================== 调用示例（适配你的项目）====================
if __name__ == "__main__":
    # 你的配置数据（和你之前的appearance结构一致）
    your_config = {
        "appearance": {
            "main_window": {"width": 1280, "height": 650},
            "task_segmentation_window": {"width": 650, "height": 550},
            "diary_details_window": {"width": 650, "height": 550},
            "setting_window": {"width": 750, "height": 650}
        }
    }

    # 1. 备份配置（保留历史版本，生成带时间戳的文件）
    backup_path = BackupJsonData.backup_json(your_config,"backup/data")

    # # 2. （可选）从备份恢复配置
    # if backup_path:
    #     restored_config = BackupJsonData.restore_json(backup_path)
    #     # 恢复后可直接使用配置（比如给window_template传参）
    #     # 示例：获取主窗口尺寸
    #     if restored_config:
    #         main_width = restored_config["appearance"]["main_window"]["width"]
    #         main_height = restored_config["appearance"]["main_window"]["height"]
    #         print(f"恢复的主窗口尺寸：{main_width} x {main_height}")
