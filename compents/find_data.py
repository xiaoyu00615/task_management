
class FindData:


    @staticmethod
    def find_data(data_list:list,item:dict,field) -> int:
        """
        索引查找
        :param data_list: 列表
        :param item: 字典
        :param field: 字段
        :return: int
        """
        for index,data in enumerate(data_list):
            if data[field] == item[field]:
                return index
        return -1