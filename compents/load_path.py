# config_manager.py
from compents.file_process import FileProcess
import os


class LoadConfigPath:
    # 单例实例
    _instance = None
    # 缓存：路径配置（总配置file_path.json）
    _path_config = {}
    # 缓存：实体配置（key=实体配置路径，value=实体配置字典）
    _entity_config_cache = {}

    def __new__(cls):
        """单例模式：全局唯一实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化加载总配置（路径配置）
            cls._init_path_config()
        return cls._instance

    @classmethod
    def _init_path_config(cls):
        """加载总配置（file_path.json），仅执行一次"""
        total_config_path = "config/file_path.json"  # 你的总配置文件路径
        if os.path.exists(total_config_path):
            cls._path_config = FileProcess.read_json(total_config_path)
        else:
            raise FileNotFoundError(f"总配置文件不存在：{total_config_path}")

    @classmethod
    def get_path_config(cls):
        """获取总配置（路径配置），兼容你原有代码的load_path"""
        return cls._path_config

    @classmethod
    def get_entity_config(cls, path_key=None, direct_path=None):
        """
        加载/获取实体配置（核心方法）
        :param path_key: 总配置中的路径索引（如"menu_bar/settings"），二选一
        :param direct_path: 实体配置的直接路径（如"config/setting.json"），二选一
        :return: 实体配置字典（缓存的引用，全局唯一）
        """
        # 优先通过path_key从总配置找路径
        if path_key:
            keys = path_key.split("/")
            config = cls._path_config
            try:
                for key in keys:
                    config = config[key]
                entity_path = config
            except KeyError:
                raise KeyError(f"总配置中未找到路径索引：{path_key}")
        elif direct_path:
            entity_path = direct_path
        else:
            raise ValueError("必须传入path_key或direct_path")

        # 缓存命中：直接返回已加载的字典（引用不变）
        if entity_path in cls._entity_config_cache:
            return cls._entity_config_cache[entity_path]
        # 缓存未命中：加载并缓存
        if os.path.exists(entity_path):
            entity_config = FileProcess.read_json(entity_path)
            cls._entity_config_cache[entity_path] = entity_config
            return entity_config
        else:
            raise FileNotFoundError(f"实体配置文件不存在：{entity_path}")

    @classmethod
    def update_entity_config(cls, new_value, path_key=None, direct_path=None, config_key_path=None):
        """
        更新实体配置（保证全局同步+持久化）
        :param new_value: 要修改的新值
        :param path_key: 总配置中的路径索引（如"menu_bar/settings"）
        :param direct_path: 实体配置直接路径（如"config/setting.json"）
        :param config_key_path: 实体配置内的多级键（如"backup/auto_backup"）
        """
        # 1. 获取实体配置路径和缓存的字典
        if path_key:
            keys = path_key.split("/")
            config = cls._path_config
            for key in keys:
                config = config[key]
            entity_path = config
        elif direct_path:
            entity_path = direct_path
        else:
            raise ValueError("必须传入path_key或direct_path")

        entity_config = cls.get_entity_config(direct_path=entity_path)  # 获取缓存的字典

        # 2. 修改实体配置字典的内部值（关键：引用不变，全局同步）
        if config_key_path:
            keys = config_key_path.split("/")
            config = entity_config
            # 遍历到最后一级父节点
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            # 修改最后一级值
            config[keys[-1]] = new_value
        else:
            # 替换整个实体配置（慎用，建议用config_key_path修改局部）
            cls._entity_config_cache[entity_path] = new_value

        # 3. 持久化保存到实体配置文件
        FileProcess.write_json(entity_config, entity_path)
        print(f"实体配置已更新并保存：{entity_path} → {config_key_path} = {new_value}")


# ==================== 兼容你原有代码的全局变量 ====================
# 初始化单例
config_manager = LoadConfigPath()

# 原有代码中的load_path（总配置，路径索引）
load_path = config_manager.get_path_config()

# # 原有代码中的setting_path（实体配置：config/setting.json）
# setting_config = load_path["menu_bar"]["settings"]  # 从总配置取路径
# setting_path = config_manager.get_entity_config(direct_path=setting_config)  # 加载实体配置