
from compents.log import logger
from compents.file_process import FileProcess
from compents.time_process import TimeProcess
from compents.str_process import StrProcess
import datetime

class AssistantDef:

    @staticmethod
    def has_urgency(total_seconds):
        """
        根据总秒数判断紧急度（1-10级），1最紧急，10最不紧急
        时间分割规则（科学非线性梯度，短时间精细、长时间宽泛）：
        1级：<6小时（最紧急）、2级：6-12小时、3级：12-24小时
        4级：1-3天、5级：3-7天、6级：7-14天
        7级：14-30天、8级：30-45天、9级：45-60天
        10级：≥60天（2个月及以上，最不紧急）
        :param total_seconds: 总秒数（支持int/float，可直接传timedelta.total_seconds()）
        :return: 紧急度等级（int，1-10）
        """
        # 鲁棒性处理：负秒数（时间差计算异常）按最紧急处理
        if total_seconds < 0:
            return "0-超时"

        # 定义基础时间单位（秒），方便维护和调整，无需手动计算
        SEC_PER_HOUR = 3600  # 1小时=3600秒
        SEC_PER_DAY = 86400  # 1天=86400秒
        HOUR_6 = 6 * SEC_PER_HOUR  # 6小时（1级临界）
        HOUR_12 = 12 * SEC_PER_HOUR  # 12小时（2级临界）
        DAY_1 = 1 * SEC_PER_DAY  # 1天（3级临界）
        DAY_3 = 3 * SEC_PER_DAY  # 3天（4级临界）
        DAY_7 = 7 * SEC_PER_DAY  # 7天（5级临界）
        DAY_14 = 14 * SEC_PER_DAY  # 14天（6级临界）
        DAY_30 = 30 * SEC_PER_DAY  # 30天（7级临界）
        DAY_45 = 45 * SEC_PER_DAY  # 45天（8级临界）
        DAY_60 = 60 * SEC_PER_DAY  # 60天（2个月，9级临界，10级起始）

        # 从高紧急度到低紧急度判断（满足即返回，格式统一：数字-形容词）
        if total_seconds < HOUR_6:
            return "1-立即"  # 6小时内：最紧急，需立即处理
        if total_seconds < HOUR_12:
            return "2-紧急"  # 6-12小时：高紧急，需紧急处理
        if total_seconds < DAY_1:
            return "3-重要"  # 12-24小时：重要任务，1天内完成
        if total_seconds < DAY_3:
            return "4-快速"  # 1-3天：需快速推进，3天内收尾
        if total_seconds < DAY_7:
            return "5-规划"  # 3-7天：需简单规划，1周内完成
        if total_seconds < DAY_14:
            return "6-充分"  # 7-14天：有充分时间，2周内落地
        if total_seconds < DAY_30:
            return "7-缓冲"  # 14-30天：有缓冲周期，1个月内完成即可
        if total_seconds < DAY_45:
            return "8-宽裕"  # 30-45天：时间宽裕，无需赶进度
        if total_seconds < DAY_60:
            return "9-从容"  # 45-60天：从容安排，近2个月内完成
        return "10-暂缓"  # ≥60天（2个月及以上）：最不紧急，可暂缓处理


    @staticmethod
    def is_upgrade_urgency(old_urgency:str,end_time:str):
        """
        是否升级紧急度
        :param old_urgency: 旧的紧急度
        :param end_time: 新紧急度
        :return: 返回紧急度
        """
        old_urgency_num = StrProcess.get_str_inside_num(old_urgency)

        now_time = f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
        total_second = TimeProcess.calculate_time_poor(now_time,end_time)

        leve = AssistantDef.has_urgency(total_second)
        new_urgency_num = StrProcess.get_str_inside_num(leve)

        if old_urgency_num == new_urgency_num:
            # print("不用升级紧急度")
            return False

        return leve


    @staticmethod
    def task_status_change(new_status,task,path):
        print("===================================================")
        print(task,"任务状态改变")
        """
        任务状态改变
        :param new_status: 新状态
        :param task: 任务项数据
        :param path: 文件地址
        :return: bool -> 回是否成功
        """
        # print(new_status,task,path)
        new_task = task
        old_status = new_task.get("status",None)

        # 判断是否是有效修改状态
        if old_status == new_status or old_status is None:
            logger.error(f"新状态异常 {old_status} -> {new_status}")
            return False



        all_tasks = AssistantDef.task_del(new_task,path,has_write=False)
        # print(f"删除后的========all_tasks -> {all_tasks}")


        # 修改好的task -> status
        new_task["status"] = new_status
        new_task["completed_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(new_task, "new_status:")

        all_tasks[f"{new_status}_list"].append(new_task)

        # print(f"处理好的数据,{all_tasks}")
        print("new_task:",new_task)
        print("改变写入数据的",all_tasks)
        print("=====================================================")
        FileProcess.write_json(path,all_tasks)
        return True


    @staticmethod
    def task_del(task,path,has_write=True):
        """
        删除任务数据
        :param task: 删除的任务项 dict -> {id,name}
        :param path: 根目录路径
        :param has_write: 是否进行写入
        :return: 删除是否成功
        """
        task_id = task.get("id",None)
        status = task.get("status",None)

        # 获取全部数据
        all_tasks = FileProcess.read_json(path)

        try:
            if len(all_tasks[f"{status}_list"]) <= 1:
                all_tasks[f"{status}_list"].pop(0)

        except Exception as e:
            logger.error(f"下标越界 -> {e}")

        # 删除
        for i, all_task in enumerate(all_tasks[f"{status}_list"]):
            # print('删除逻辑：all_task["id"] == task_id',all_task["id"] , task_id)
            if all_task["id"] == task_id:
                logger.debug(f"删除数据项 -> {all_tasks[f"{status}_list"][i]} -> 状态{status}")
                all_tasks[f"{status}_list"].pop(i)
                break
        if has_write:
            FileProcess.write_json(path,all_tasks)

        return all_tasks

    @staticmethod
    def del_task_ui(parent_widget,target_widget):
        if not parent_widget or not target_widget:
            return False

        try:
            parent_widget.removeWidget(target_widget)
            target_widget.hide()
            target_widget.deleteLater()
        except Exception as e:
            logger.error(f"已删除 -> {e}")
            return False

        return True

    @staticmethod
    def is_task_timeout(end_time:str) -> bool:
        """
        判断任务是否会超时
        :param end_time: 截止时间
        :return: bool -> True
        """
        now_time = f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"

        time_rest = TimeProcess.calculate_time_poor(now_time,end_time)
        # print(time_rest,"time_rest")
        if time_rest <= 0:
            return True
        return False


    @staticmethod
    def del_list_item_dict(tasks:list,item:dict,) -> list:
        return [ task for task in tasks if item["id"] != task["id"]]


    @staticmethod
    def tasks_sort(tasks: list, weight: str):
        """
        任务排序：
        1. 优先按指定weight字段降序排序
        2. 权重相同时，按end_time升序（截止时间更早的排前面）
        3. 兼容weight/end_time为空的情况
        """
        # 边界处理：任务列表为空 或 第一个任务无weight字段 → 直接返回原列表
        if not tasks or (len(tasks) > 0 and not tasks[0].get(weight)):
            return tasks

        def get_sort_key(task):
            """定义排序键：(权重值(负数降序), 截止时间datetime对象)"""
            # 1. 处理权重值（空值默认0，确保排序不报错）
            weight_value = task.get(weight, 0)
            # 转成数值类型（避免字符串权重比较出错，比如"10"和"2"）
            try:
                weight_value = float(weight_value)
            except (ValueError, TypeError):
                weight_value = 0

            # 2. 处理截止时间（转成datetime对象，用于比较；异常/空值默认一个极晚的时间）
            end_time_str = task.get('end_time', '')
            try:
                end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                # 无截止时间/格式错误 → 排到权重相同组的最后
                end_time = datetime.datetime.max

            # 排序键：(-权重值 → 降序, 截止时间 → 升序)
            return (-weight_value, end_time)

        # 按自定义key排序
        tasks.sort(key=get_sort_key)
        return tasks