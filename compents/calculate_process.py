from compents.str_process import StrProcess
from compents.file_process import FileProcess



class CalculateProcess:

    @staticmethod
    def calculate_task_weight(important:str,urgency:str):
        """
        计算权重
        :param important: 重要度
        :param urgency: 紧急度
        :return: 权重
        """
        important_num = StrProcess.get_str_inside_num(important)
        urgency_num = StrProcess.get_str_inside_num(urgency)

        # 计算基础分
        important_weight = (5 - important_num) * 20
        urgency_weight = (11 - urgency_num) * 10

        # 计算权重比例
        important_proportion = 0.6
        urgency_proportion = 0.4

        # 计算和
        total_widget = important_weight * important_proportion + urgency_weight * urgency_proportion

        return total_widget

    @staticmethod
    def add_weight(tasks,important,urgency,is_write=True,path="data/tasks.json"):
        for task in tasks:
            total_weight = CalculateProcess.calculate_task_weight(important,urgency)
            task['weight'] = total_weight

        if is_write:
            get_total_data = FileProcess.read_json(path)
            get_total_data['unfinished'] = tasks

            FileProcess.write_json_attribute(path,["unfinished"],get_total_data)
