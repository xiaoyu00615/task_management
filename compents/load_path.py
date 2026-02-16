from compents.file_process import FileProcess

class LoadConfigPath:
    def __init__(self):
        pass

    @staticmethod
    def init_path(path):
        return FileProcess.read_json(path)



load_path = LoadConfigPath.init_path("config/file_path.json")