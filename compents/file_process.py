import json
import os.path
import copy


class FileProcess:
    # 绝对路径根目录
    ROOT_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))# 初始化创建data.json 文件



    @staticmethod
    def read_json(path) -> dict:
        """
        读取整个json文件 并返回
        :param path: 文件路径 根目录开始
        :return: dict -> json数据
        """
        # logger.info(f"开始读取json文件 -> {path}",)
        path = os.path.join(FileProcess.ROOT_FILE, path)
        try:
            with open(path,"r",encoding="utf-8") as f:
                # logger.info(f"json文件读取完成 -> {path}")
                return json.load(f)
        except Exception as e:
            logger.error("文件路径不存在！")
            print(e)
            return {}


    @staticmethod
    def read_json_attribute(path,attrs:list):
        """
        读取json 指定层级获取元素
        :param path: 路径 -> 填写从根目录开始的路径
        :param attrs: 需要遍历的层级 -> list
        :return: 返回指定对象层级的(值)数据
        """
        # logger.info(f"开始读取json文件 -> {path}", )
        path = os.path.join(FileProcess.ROOT_FILE, path)

        try:
            with open(path,"r",encoding="utf-8") as f:
                json_data = json.load(f)
                obj_value = json_data

                if not attrs:
                    logger.error("这是一个空列表")
                    return None

                # 如果是一个就直接拿取返回
                if len(attrs) <= 1:
                    logger.info(f"json文件读取完成 -> {path}，参数 -> {attrs}")
                    return obj_value.get(attrs[0],None)

                for attr in attrs:
                    # 用之前保存的数据进行遍历
                    obj_value = obj_value.get(attr,None)

                    # 判断是否取出属性
                    if obj_value is None:
                        logger.error(f"没有此对象属性{obj_value} -> {attr}")
                        break

            # logger.info(f"json文件读取完成 -> {path}，参数 -> {attrs}")
            return obj_value

        except FileNotFoundError:
            logger.error(f"JSON文件路径不存在：{path}")
        except json.JSONDecodeError:
            logger.error(f"JSON文件解析失败，文件格式错误：{path}")
        except PermissionError:
            logger.error(f"无权限读取JSON文件：{path}")
        except Exception as e:
            logger.error(f"读取/解析JSON文件异常：{str(e)}，文件路径：{path}")

        return None

    @staticmethod
    def write_json(path,content,write_fun="w"):
        """
        写入json文件
        :param path: 文件路径从根目录开始写
        :param content: 写入内容
        :param write_fun: 写入方法 "w" "w+" ....
        :return: bool -> 写入状态
        """
        # logger.info(f"开始写入文件 -> {path}")

        write_fun_list = ["w","w+","a","a+"]
        if write_fun not in write_fun_list:
            logger.error(f"写入方法 -> {write_fun} 不合法")
            return False

        path = os.path.join(FileProcess.ROOT_FILE, path)

        if not os.path.exists(path):
            logger.error(f"没有文件 -> {os.path.dirname(path)} 进行创建")
            os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            with open(path,write_fun,encoding="utf-8") as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=4))
                # logger.info(f"文件写入成功！-> {path}")
                return True

        except Exception as e:
            logger.error(f"文件错误 -> {e}")

        return False


    @staticmethod
    def write_json_attribute(path,attrs:list,content):
        """
        写入json 属性
        :param path: 项目根目录开始
        :param attrs: list -> 层级嵌套关系
        :param content: 写入属性的内容
        :return: bool -> 布尔
        """
        # logger.info(f"开始写入属性->{path} -> {attrs} -> {content}")
        # 拼接全部路径
        paths = os.path.join(FileProcess.ROOT_FILE, path)
        # 获取json 数据
        json_data = FileProcess.read_json(paths)
        new_json = json_data

        # 空列表直接不出来退出
        if not attrs:
            return False

        # 如果是一层就直接修改保存
        if len(attrs) <= 1:
            new_json[attrs[0]] = content

        else:
            # 循环到倒数第二个元素
            # print(attrs[:-1])
            for attr in attrs[:-1]:
                new_json = new_json[attr]

            # 获取最后一个元素进行修改
            last_attr = attrs[-1]
            new_json[last_attr] = content

        # 重新写入json文件s
        FileProcess.write_json(paths,json_data)
        # logger.info(f"写入属性成功 -> {paths}")
        return True


    @staticmethod
    def create_dir_file(path, json_content=None):
        """
        创建文件夹或文件，如果是文件则写入json，不是文件则直接创建
        :param path: 文件路径从项目根目录开始
        :param json_content: 写入的json内容
        :return: bool -> 是否创建成功
        """
        if json_content is None:
            json_content = dict()
        # logger.info(f"开始创创建文件夹 -> {path}")
        # 拆分出文件名
        file_split = os.path.split(path)[1]

        # 拆出扩展名
        extension = os.path.splitext(file_split)

        # 合并路径
        paths = os.path.join(FileProcess.ROOT_FILE, path)

        if os.path.exists(paths):
            return True

        try:
            # 判断是否有扩展名
            if extension[1]:
                os.makedirs(os.path.dirname(paths), exist_ok=True)
                with open(paths,"w",encoding="utf-8") as f:
                    f.write(json.dumps(json_content, ensure_ascii=False, indent=4))

                logger.info(f"文件夹创建完成并写入文件成功 -> {paths} -> {json_content}")
            else:
                os.makedirs(paths, exist_ok=True)
                logger.info(f"文件夹创建完成 -> {paths}")
        except Exception as e:
            logger.error(f"创建或写入文件夹或文件时出现错误 -> {e}")
            return False

        return True


    @staticmethod
    def is_root_file(path):
        """
        判断从根目录开始这个文件有没有存在
        :param path: 路径根目录开始
        :return: bool
        """
        if os.path.exists(os.path.join(FileProcess.ROOT_FILE,path)):
            return True
        return False


if __name__ == "__main__":
    from log import logger
    # print(FileProcess.read_json("config/public.json"))
    # print(FileProcess.read_json_attribute("config/public.json",["important_map"]))
    # print(FileProcess.write_json("data/data.json",{"a":1,"b":2}))
    # print(FileProcess.create_dir_file("data/data/names",{"a":1,"b":2}))
    # print(FileProcess.write_json_attribute("config/init.json", ["start_data", "max_id"], 2))
else:
    from compents.log import logger