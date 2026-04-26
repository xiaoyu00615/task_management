import datetime

from compents.log import logger
from compents.file_process import FileProcess
from compents.load_path import load_path
from compents_pyqt5.operation_confirm_dialog import use_operation_confirm_dialog_template

class EventModalSegmentation:
    @staticmethod
    def on_segmentation_create_task(this,task,segmentation_task_item):
        # print(task,"创建细分")

        # 创建任务
        logger.debug(f"创建细分任务 -> {segmentation_task_item} -> {task}")

        # 任务状态
        status_list = f"{task["status"]}_list"


        get_json = FileProcess.read_json(load_path["store"]["task"])
        # 修改最大索引
        get_json["max_segmentation_id"] = segmentation_task_item["segmentation_id"]
        items = None
        for index,items in enumerate(get_json[status_list]):
            if items["id"] == task["id"]:
                # 确保 items["segmentation"] 是一个列表
                if "segmentation" not in items or not isinstance(items["segmentation"], list):
                    items["segmentation"] = []
                items["segmentation"].append(segmentation_task_item)
                if task["status"] == "uncompleted":
                    # 确保 unfinished_list_task_data 中的 segmentation 是一个列表
                    if "segmentation" not in this.parent.main_window.unfinished_list_task_data[index] or not isinstance(this.parent.main_window.unfinished_list_task_data[index]["segmentation"], list):
                        this.parent.main_window.unfinished_list_task_data[index]["segmentation"] = []
                    this.parent.main_window.unfinished_list_task_data[index]["segmentation"].append(segmentation_task_item)
                break
        
        # 写回 JSON 文件
        FileProcess.write_json(load_path["store"]["task"],get_json)

        # 确保 task["segmentation"] 是一个列表并添加任务
        if "segmentation" not in task or not isinstance(task["segmentation"], list):
            task["segmentation"] = []
        # 避免重复添加，只在 task 中不存在该任务时添加
        task_ids = [item.get("segmentation_id") for item in task["segmentation"] if isinstance(item, dict)]
        if segmentation_task_item["segmentation_id"] not in task_ids:
            task["segmentation"].append(segmentation_task_item)

        this.refresh_all_segmentation_tasks_ui(items)




    @staticmethod
    def on_del_segmentation_task(this,list_task_dict,task_item_dict):
        logger.debug(f"删除segmentation任务 -> {task_item_dict}")
        # 使用 get 方法安全获取 password 键，避免 KeyError
        if not task_item_dict.get("password") is None:
            if not use_operation_confirm_dialog_template({
                "parent":this.parent,
                "title":f"删除细碎任务操作 -> {task_item_dict.get('name', '未命名任务')}",
                "text":"想要删除这个细碎任务吗？一旦删除将无法撤回任务"
            },{
                "cancel_msg":f"删除细碎任务 -> {task_item_dict} 加油！",
                "update_msg":f"此类提示窗状态更新！不再显示！"
            }): return

        new_json = this.del_segmentation_tasks(list_task_dict,task_item_dict)

        # 刷新界面
        this.refresh_all_segmentation_tasks_ui(new_json)

    @staticmethod
    def on_complete_segmentation_task(this,list_task_dict,task_item_dict):
        logger.debug(f"完成segmentation任务 -> {task_item_dict}")

        if not use_operation_confirm_dialog_template({
            "parent":this.parent,
            "title":f"完成细碎任务操作 -> {task_item_dict.get('name', '未命名任务')}",
            "text":"已经完成了这个任务吗，距离目标又近了一步哦！加油呀！"
        },{
            "cancel_msg":f"完成细碎任务 -> {task_item_dict} 加油！",
            "update_msg":f"此类提示窗状态更新！不再显示！"
        }): return

        task_item_dict["status"] = "completed"
        task_item_dict["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        this.refresh_all_segmentation_tasks_ui(list_task_dict)


