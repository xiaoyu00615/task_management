import json
import os.path
import sys


class FileProcess:
    # 类属性：真实根目录（指向exe/源码所在目录）
    ROOT_FILE = None
    # 缓存：存储已读取的JSON文件内容
    _json_cache = {}
    # 缓存过期时间（秒）
    _cache_expiry = 300  # 5分钟
    # 缓存最后更新时间
    _cache_last_update = {}

    @classmethod
    def get_real_root_path(cls):
        """
        获取程序运行的真实根目录（优先exe所在目录，其次源码目录）
        """
        if getattr(sys, 'frozen', False):
            # 打包成exe运行：获取exe文件所在目录
            root_path = os.path.dirname(os.path.abspath(sys.executable))
        else:
            # 源码运行：获取当前源码文件所在目录的上上级（根据你的项目层级调整）
            current_file = os.path.abspath(__file__)
            root_path = os.path.dirname(os.path.dirname(current_file))  # 按需调整层数

        # 确保路径是绝对路径，避免相对路径混乱
        return os.path.abspath(root_path)

    @classmethod
    def _init_root_path(cls):
        """
        初始化根路径
        """
        if cls.ROOT_FILE is None:
            cls.ROOT_FILE = cls.get_real_root_path()

    @classmethod
    def _is_cache_valid(cls, path):
        """
        检查缓存是否有效
        :param path: 文件路径
        :return: bool
        """
        import time
        if path not in cls._json_cache:
            return False
        if path not in cls._cache_last_update:
            return False
        return time.time() - cls._cache_last_update[path] < cls._cache_expiry

    @classmethod
    def read_json(cls, path) -> dict:
        """
        读取整个json文件 并返回
        :param path: 文件路径 根目录开始
        :return: dict -> json数据
        """
        cls._init_root_path()
        full_path = os.path.join(cls.ROOT_FILE, path)
        
        # 检查缓存是否有效
        if cls._is_cache_valid(full_path):
            return cls._json_cache[full_path]
        
        try:
            with open(full_path,"r",encoding="utf-8") as f:
                data = json.load(f)
                # 更新缓存
                cls._json_cache[full_path] = data
                import time
                cls._cache_last_update[full_path] = time.time()
                return data
        except Exception as e:
            logger.error(f"读取JSON文件失败：{e}")
            return {}

    @classmethod
    def read_json_attribute(cls, path, attrs:list):
        """
        读取json 指定层级获取元素
        :param path: 路径 -> 填写从根目录开始的路径
        :param attrs: 需要遍历的层级 -> list
        :return: 返回指定对象层级的(值)数据
        """
        cls._init_root_path()
        full_path = os.path.join(cls.ROOT_FILE, path)
        
        # 检查缓存是否有效
        if not cls._is_cache_valid(full_path):
            # 缓存无效，重新读取
            try:
                with open(full_path,"r",encoding="utf-8") as f:
                    data = json.load(f)
                    cls._json_cache[full_path] = data
                    import time
                    cls._cache_last_update[full_path] = time.time()
            except Exception as e:
                logger.error(f"读取JSON文件失败：{e}")
                return None
        
        json_data = cls._json_cache[full_path]
        obj_value = json_data

        if not attrs:
            logger.error("这是一个空列表")
            return None

        # 如果是一个就直接拿取返回
        if len(attrs) <= 1:
            return obj_value.get(attrs[0],None)

        for attr in attrs:
            # 用之前保存的数据进行遍历
            obj_value = obj_value.get(attr,None)

            # 判断是否取出属性
            if obj_value is None:
                logger.error(f"没有此对象属性{obj_value} -> {attr}")
                break

        return obj_value

    @classmethod
    def write_json(cls, path, content, write_fun="w"):
        """
        写入json文件
        :param path: 文件路径从根目录开始写
        :param content: 写入内容
        :param write_fun: 写入方法 "w" "w+" ....
        :return: bool -> 写入状态
        """
        cls._init_root_path()
        write_fun_list = ["w","w+","a","a+"]
        if write_fun not in write_fun_list:
            logger.error(f"写入方法 -> {write_fun} 不合法")
            return False

        full_path = os.path.join(cls.ROOT_FILE, path)

        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path,write_fun,encoding="utf-8") as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=4))
                # 更新缓存
                cls._json_cache[full_path] = content
                import time
                cls._cache_last_update[full_path] = time.time()
                return True

        except Exception as e:
            logger.error(f"文件错误 -> {e}")

        return False

    @classmethod
    def write_json_attribute(cls, path, attrs:list, content):
        """
        写入json 属性
        :param path: 项目根目录开始
        :param attrs: list -> 层级嵌套关系
        :param content: 写入属性的内容
        :return: bool -> 布尔
        """
        cls._init_root_path()
        full_path = os.path.join(cls.ROOT_FILE, path)
        # 获取json 数据
        json_data = cls.read_json(full_path)
        new_json = json_data

        # 空列表直接不出来退出
        if not attrs:
            return False

        # 如果是一层就直接修改保存
        if len(attrs) <= 1:
            new_json[attrs[0]] = content
        else:
            # 循环到倒数第二个元素
            for attr in attrs[:-1]:
                if attr not in new_json:
                    new_json[attr] = {}
                new_json = new_json[attr]

            # 获取最后一个元素进行修改
            last_attr = attrs[-1]
            new_json[last_attr] = content

        # 重新写入json文件
        result = cls.write_json(full_path, json_data)
        return result

    @classmethod
    def create_dir_file(cls, path, json_content=None):
        """
        创建文件夹或文件，如果是文件则写入json，不是文件则直接创建
        :param path: 文件路径从项目根目录开始
        :param json_content: 写入的json内容
        :return: bool -> 是否创建成功
        """
        cls._init_root_path()
        if json_content is None:
            json_content = dict()
        # 拆分出文件名
        file_split = os.path.split(path)[1]

        # 拆出扩展名
        extension = os.path.splitext(file_split)

        # 合并路径
        full_path = os.path.join(cls.ROOT_FILE, path)

        if os.path.exists(full_path):
            return True

        try:
            # 判断是否有扩展名
            if extension[1]:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path,"w",encoding="utf-8") as f:
                    f.write(json.dumps(json_content, ensure_ascii=False, indent=4))
                # 更新缓存
                cls._json_cache[full_path] = json_content
                import time
                cls._cache_last_update[full_path] = time.time()
                logger.info(f"文件夹创建完成并写入文件成功 -> {full_path} -> {json_content}")
            else:
                os.makedirs(full_path, exist_ok=True)
                logger.info(f"文件夹创建完成 -> {full_path}")
        except Exception as e:
            logger.error(f"创建或写入文件夹或文件时出现错误 -> {e}")
            return False

        return True

    @classmethod
    def is_root_file(cls, path):
        """
        判断从根目录开始这个文件有没有存在
        :param path: 路径根目录开始
        :return: bool
        """
        cls._init_root_path()
        return os.path.exists(os.path.join(cls.ROOT_FILE, path))

    @classmethod
    def clear_cache(cls, path=None):
        """
        清除缓存
        :param path: 可选，指定路径，不指定则清除所有缓存
        """
        if path:
            full_path = os.path.join(cls.ROOT_FILE, path)
            if full_path in cls._json_cache:
                del cls._json_cache[full_path]
            if full_path in cls._cache_last_update:
                del cls._cache_last_update[full_path]
        else:
            cls._json_cache.clear()
            cls._cache_last_update.clear()


if __name__ == "__main__":
    from log import logger
    # print(FileProcess.read_json("config/public.json"))
    # print(FileProcess.read_json_attribute("config/public.json",["important_map"]))
    # print(FileProcess.write_json("data/data.json",{"a":1,"b":2}))
    # print(FileProcess.create_dir_file("data/data/names",{"a":1,"b":2}))
    # print(FileProcess.write_json_attribute("config/init.json", ["start_data", "max_id"], 2))
else:
    from compents.log import logger