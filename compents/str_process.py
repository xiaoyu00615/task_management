from compents.log import logger

class StrProcess:


    @staticmethod
    def get_str_inside_num(str_content,rest_type="int"):
        """
        获取字符串中的数字
        :param str_content: 进行处理的字符串
        :param rest_type:  返回的结果类型 int list sum ride
        :return: int list
        """
        # logger.info(f"进行处理字符串操作 -> 字符串：{str_content} -> 返回类型{rest_type}")

        if type(str_content) == int:
            return str_content


        if str_content.isdigit():
            return int(str_content)

        if not str_content:
            logger.error(f"内容字符串为空 -> {str_content}")
            return None

        num_list = [i for i in list(str_content) if i.isdigit()]

        if not num_list:
            logger.error("处理后 -> 字符串中没有数字")
            return None

        if rest_type == "int":
            return int(''.join(num_list))

        if rest_type == "list":
            return num_list

        if rest_type == "sum":
            sum_num = 0
            for i in num_list:
                sum_num += int(i)
            return sum_num

        if rest_type == "ride":
            ride_num = 1
            for i in num_list:
                ride_num *= int(i)
            return ride_num

        logger.info(f"传入的返回类型不正确 -> {rest_type}")
        return None

    @staticmethod
    def specify_str_num_pad(str_content,num,pad=None):
        if len(str_content) <= num:
            return str_content

        new = str_content[:num]
        if pad is None:
            return new

        return f"{new}{pad}"


if __name__ == '__main__':
    # print(StrProcess.get_str_inside_num("sadasd "))
    # print(StrProcess.specify_str_num_pad("asdjaksdjskafjlsdkfsdlfjskl",5,"..."))

    pass
