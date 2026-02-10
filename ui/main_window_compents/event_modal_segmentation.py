import datetime

from compents.log import logger
from compents.file_process import FileProcess
from ui.uilt.assistant_def import AssistantDef


class EventModalSegmentation:
    @staticmethod
    def on_segmentation_create_task(this,task,segmentation_task_item):

        # 创建任务
        logger.debug(f"创建细分任务 -> {segmentation_task_item} -> {task}")
        task["segmentation"] = segmentation_task_item

        # 任务状态
        status_list = f"{task["status"]}_list"


        get_json = FileProcess.read_json("data/tasks.json")
        # 修改最大索引
        get_json["max_segmentation_id"] = segmentation_task_item["segmentation_id"]

        items = None
        for items in get_json[status_list]:
            if items["id"] == task["id"]:
                items["segmentation"].append(segmentation_task_item)
                break


        this.refresh_all_segmentation_tasks_ui(items)




    @staticmethod
    def on_del_segmentation_task(this,list_task_dict,task_item_dict):
        logger.debug(f"删除segmentation任务 -> {task_item_dict}")
        new_json = this.del_segmentation_tasks(list_task_dict,task_item_dict)

        # 刷新界面
        this.refresh_all_segmentation_tasks_ui(new_json)

    @staticmethod
    def on_complete_segmentation_task(this,list_task_dict,task_item_dict):
        logger.debug(f"完成segmentation任务 -> {task_item_dict}")

        task_item_dict["status"] = "completed"
        task_item_dict["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        this.refresh_all_segmentation_tasks_ui(list_task_dict)


