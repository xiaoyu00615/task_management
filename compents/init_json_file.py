
from compents.load_path import config_manager,load_path
from compents.file_process import FileProcess

class InitJsonFile:
    init_template = config_manager.get_entity_config(path_key="template")
    def __init__(self):


        self._init_json()

    def _init_json(self):
        InitJsonFile.init_task()
        InitJsonFile.init_chat()
        InitJsonFile.init_diary()


    @classmethod
    def init_task(cls):
        # 获取结构json
        init_structure = cls.init_template["start_task"]
        # 创建文件及文件夹，传入结构json
        FileProcess.create_dir_file(load_path["store"]["task"], init_structure)


    @classmethod
    def init_chat(cls):
        # 获取结构json
        init_structure = cls.init_template["ai_chat"]
        # 创建文件及文件夹，传入结构json
        FileProcess.create_dir_file(load_path["store"]["chat"], init_structure)

    @classmethod
    def init_diary(cls):
        init_structure = cls.init_template["diary"]
        FileProcess.create_dir_file(load_path["store"]["diary"], init_structure)

