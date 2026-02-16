from compents.log import logger
from compents.file_process import FileProcess
from compents.find_data import FindData
from ui.main_window_compents.diary_compents.details_sub_window import DetailsSubWindow
from compents.load_path import load_path
class DiaryEvent:

    @staticmethod
    def on_create_diary_item(this,data):
        logger.info(f"创建日记任务项 -> {data}")
        this.diary_dict["ordinary_list"].insert(0,data)

        # 修改日记主页面内容
        this.ordinary_list_weight.list_dict_num += 1
        this.diary_dict["max_id"] = data.get("id")
        this.ordinary_list_weight.diary_num.setText(f"日记总数：({this.ordinary_list_weight.list_dict_num})")

        # print(this.diary_dict)
        FileProcess.write_json(load_path["store"]["diary"],this.diary_dict)

        this.ordinary_list_weight.ref_list(this.ordinary_list_weight.content_layout)

    @staticmethod
    def no_del_diary(this,this_list,data):
        logger.debug(f"删除日记数据 -> this {this} -> {data}")

        # 1. 前置校验：确保必要字段存在
        if not data.get("id"):
            logger.error("删除失败：日记数据缺少id字段")
            return
        if not data.get("type"):  # 需确保data有type字段（ordinary/collection）
            logger.error("删除失败：日记数据缺少type字段")
            return

        try:
            # 2. 查找目标数据索引（处理未找到的情况）
            data_index = FindData.find_data(this_list.list_dict, data, "id")
            # print(data_index, "data_index")

            # 关键：如果没找到目标索引，直接返回，避免删错数据
            if data_index == -1:
                logger.warning(f"删除失败：未找到id为{data['id']}的日记")
                return

            this_list.list_dict.pop(data_index)

            # 根据日记类型找到对应的源列表（ordinary_list/collection_list）
            diary_type_list = this.diary_dict.get(f"{data['type']}_list", [])
            source_index = FindData.find_data(diary_type_list, data, "id")
            if source_index != -1:
                diary_type_list.pop(source_index)
            else:
                logger.warning(f"源数据中未找到id为{data['id']}的日记（类型：{data['type']}）")

            FileProcess.write_json(load_path["store"]["diary"], this.diary_dict)

            this_list.ref_list(this_list.content_layout)

            this_list.list_dict_num = len(this_list.list_dict)
            this_list.diary_num.setText(f"日记总数：({this_list.list_dict_num})")

            logger.info(f"成功删除id为{data['id']}的日记，当前列表剩余{len(this_list.list_dict)}条")

        except IndexError as e:
            # 捕获索引越界异常（如列表为空、索引无效）
            logger.error(f"删除失败：索引异常 - {e}，当前列表长度：{len(this_list.list_dict)}")
        except Exception as e:
            # 捕获其他未知异常，避免程序崩溃
            logger.error(f"删除失败：未知错误 - {e}")





    @staticmethod
    def no_collection_diary(this,this_list,data):
        logger.debug(f"更改类型，原类型：{data['type']}")

        # 1. 保存原类型，用于从原列表删除数据
        old_type = data['type']
        # 2. 切换类型
        if old_type == "collection":
            new_type = 'ordinary'
        elif old_type == "ordinary":
            new_type = 'collection'
        data["type"] = new_type

        try:
            # 3. 从原类型列表中删除该数据（核心修复：解决数据冗余）
            old_list = this.diary_dict[f"{old_type}_list"]
            old_index = FindData.find_data(old_list, data, "id")
            if old_index != -1:  # 确保找到数据再删除
                old_list.pop(old_index)

            # 4. 将数据添加到新类型列表
            this.diary_dict[f"{new_type}_list"].append(data)

            # 5. 从当前显示列表中移除数据
            current_index = FindData.find_data(this_list.list_dict, data, "id")
            if current_index != -1:
                this_list.list_dict.pop(current_index)

            # 6. 写入JSON文件
            FileProcess.write_json(load_path["store"]["diary"], this.diary_dict)

            # 7. 刷新两个列表的界面（核心修复：刷新逻辑）
            this.ordinary_list_weight.ref_list(this.ordinary_list_weight.content_layout)
            this.collection_list_weight.ref_list(this.collection_list_weight.content_layout)

            # 8. 更新两个列表的数量统计
            this.ordinary_list_weight.list_dict_num = len(this.diary_dict["ordinary_list"])
            this.collection_list_weight.list_dict_num = len(this.diary_dict["collection_list"])
            this.ordinary_list_weight.diary_num.setText(f"日记总数：({this.ordinary_list_weight.list_dict_num})")
            this.collection_list_weight.diary_num.setText(f"收藏总数：({this.collection_list_weight.list_dict_num})")

            logger.info(f"日记类型切换成功：{old_type} -> {new_type}")
        except Exception as e:
            logger.error(f"切换日记类型失败：{str(e)}")
            # 异常时恢复原类型，避免数据错乱
            data["type"] = old_type


    @staticmethod
    def no_details_diary(this,this_list,data,parent):
        logger.info("详细日记")

        data_index = FindData.find_data(this_list.list_dict, data, "id")
        this_list.list_dict[data_index]["reading_num"] += 1
        FileProcess.write_json_attribute(load_path["store"]["diary"], [this_list.diary_type],this_list.list_dict)

        print(data,"进入data")
        details_sub_window = DetailsSubWindow(parent,data)
        details_sub_window.exec_()


