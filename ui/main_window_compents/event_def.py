from compents.file_process import FileProcess
from compents.log import logger
from ui.uilt.assistant_def import AssistantDef
from ui.sub_window.modal_segmentation import ModalSegmentation
from compents.load_path import load_path
from compents_pyqt5.operation_confirm_dialog import OperationConfirmDialog
from compents_pyqt5.operation_confirm_dialog import use_operation_confirm_dialog_template


class EventDef:

    @staticmethod
    def on_create_task(task_data,update_all,main_window):
        logger.info(f"点击了按钮进行事件处理创建任务 -> {task_data}")
        int_task_data = task_data


        # 处理原数据和最新数据进行合并
        origin_json = FileProcess.read_json(load_path["store"]["task"])
        origin_json["unfinished_list"].append(int_task_data)

        # 合并后重写入json数据
        FileProcess.write_json(load_path["store"]["task"],origin_json)


        main_window.unfinished_list_task_data = origin_json["unfinished_list"]

        # 重新排序
        AssistantDef.tasks_sort(main_window.unfinished_list_task_data,"weight")

        EventDef.refresh_all_list(update_all)


    @staticmethod
    def on_complete_task(parent,task_data,update_list):
        logger.info(f"任务已完成触发事件 -> {task_data}数据")
        if not use_operation_confirm_dialog_template({
            "parent":parent,
            "title":f"完成任务操作 -> {task_data['name']}",
            "text":"已经完成了这个任务了吗，点击完成即可获得完成时间的专属印章，继续加油呀！！！"
        },{
            "cancel_msg":f"还没有完成任务哦 -> {task_data} 加油！",
            "update_msg":f"此类提示窗状态更新！不再显示！"
        }): return

        AssistantDef.task_status_change("completed",task_data,"data/tasks.json")

        EventDef.refresh_all_list(update_list)

    @staticmethod
    def on_del_task(parent,task_data,update_list):
        logger.info(f"触发删除事件 -> {task_data}数据")

        if not use_operation_confirm_dialog_template({
            "parent":parent,
            "title":f"删除任务操作 -> {task_data['name']}",
            "text":"真的想删除这个任务吗，此操作不可撤回请考虑清楚，这也是你之前写过想要完成的任务不是吗？"
        },{
            "cancel_msg":f"不删除任务 -> {task_data} 嘿嘿加油！",
            "update_msg":f"此类提示窗状态更新！不再显示！"
        }): return

        AssistantDef.task_del(task_data,load_path["store"]["task"])

        EventDef.refresh_all_list(update_list)




    @staticmethod
    def refresh_all_list(all_list:list):
        logger.debug(f"刷新列表 -> {all_list}")
        if not all_list:
            return

        for task_data in all_list:
            task_data.refresh_list()


    @staticmethod
    def on_segmentation_task(parent,task):
        logger.debug(f"细分任务列表 -> {task}")
        module_segmentation = ModalSegmentation(parent=parent,task=task)
        module_segmentation.exec_()


