import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QFrame, QCheckBox)  # 新增导入QCheckBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from compents.load_path import load_path
from compents.log import logger
from compents.file_process import FileProcess


class OperationConfirmDialog(QDialog):
    """
    美化版操作确认对话框（支持长文本+不再提示复选框）
    样式通过外部QSS文件加载，代码与样式完全分离
    """

    def __init__(self, parent=None, title="操作确认", text="确定要执行此操作吗？"):
        super().__init__(parent)
        # 基础设置
        self.setWindowTitle(title)
        self.setModal(True)  # 模态对话框
        self.setMinimumSize(400, 180)  # 最小尺寸
        self.setMaximumSize(500, 400)  # 最大尺寸（限制长文本时弹窗大小）
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # 移除帮助按钮

        # 初始化UI
        self.text_content = text
        self._init_ui()

    def _init_ui(self):
        # 1. 创建文本显示区域（支持长文本+滚动）
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("ConfirmDialogTextEdit")  # 设置唯一标识，用于QSS定位
        self.text_edit.setPlainText(self.text_content)
        self.text_edit.setReadOnly(True)  # 只读，禁止编辑
        self.text_edit.setFrameStyle(QFrame.NoFrame)  # 移除边框
        self.text_edit.setFont(QFont("微软雅黑", 14))
        self.text_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 文本左对齐，垂直居中

        # 2. 创建按钮（设置唯一标识，用于QSS定位）
        self.confirm_btn = QPushButton("确定")
        self.confirm_btn.setObjectName("ConfirmDialogConfirmBtn")
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setObjectName("ConfirmDialogCancelBtn")

        # 设置按钮固定大小
        btn_size = QSize(100, 40)
        self.confirm_btn.setFixedSize(btn_size)
        self.cancel_btn.setFixedSize(btn_size)

        # 3. 创建“不再提示”复选框（右下角）
        self.no_prompt_check = QCheckBox("不再提示此提示框")
        self.no_prompt_check.setObjectName("ConfirmDialogNoPromptCheck")  # 唯一标识
        self.no_prompt_check.setFont(QFont("微软雅黑", 12))  # 字体适配

        # 4. 布局管理
        # 按钮水平布局（居中显示）
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addSpacing(20)  # 按钮间距
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 15, 0, 10)  # 调整边距，给复选框留空间

        # 复选框布局（靠右对齐，实现右下角效果）
        check_layout = QHBoxLayout()
        check_layout.addStretch()  # 左侧拉伸，让复选框靠右
        check_layout.addWidget(self.no_prompt_check)
        check_layout.setContentsMargins(0, 0, 20, 20)  # 右、下留边距，贴合右下角

        # 整体垂直布局：文本 → 按钮 → 复选框
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(check_layout)
        main_layout.setContentsMargins(20, 20, 20, 0)  # 整体边距
        main_layout.setSpacing(5)

        self.setLayout(main_layout)

        # 5. 绑定按钮事件
        self.confirm_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    @property
    def is_no_prompt(self):
        """获取“不再提示”复选框的状态"""
        return self.no_prompt_check.isChecked()

    @classmethod
    def get_confirmation(cls, parent=None, title="操作确认", text="确定要执行此操作吗？"):
        """
        静态调用方法：快速获取用户确认结果 + 不再提示状态
        :param parent: 父窗口
        :param title: 对话框标题
        :param text: 提示文本（支持长文本）
        :return: tuple - (是否确认操作: bool, 是否不再提示: bool)
        """
        dialog = cls(parent, title, text)
        confirm_result = dialog.exec_() == cls.Accepted
        no_prompt_result = dialog.is_no_prompt  # 获取复选框状态
        return confirm_result, no_prompt_result



def use_operation_confirm_dialog_template(operation_dict,logger_dict):
    """
    二次封装使用弹窗
    :param operation_dict:{parent:'',title:'',text:''}
    :param logger_dict: {cancel_msg:'',update_msg:''}
    :return: bool -> 是否继续执行函数
    """
    if not load_path["prompt_box"]["misoperation"]:
        is_confirm_bool,is_on_prompt = OperationConfirmDialog.get_confirmation(
                parent=operation_dict["parent"],
                title=operation_dict["title"],
                text=operation_dict["text"]
        )
        if not is_confirm_bool:
            logger.warning(logger_dict["cancel_msg"])
            return False

        if is_on_prompt and is_confirm_bool:
            FileProcess.write_json_attribute("config/file_path.json", ["prompt_box", "misoperation"], is_on_prompt)
            logger.warning(logger_dict["update_msg"])
            load_path["prompt_box"]["misoperation"] = is_on_prompt
            return True

    return True



# 测试示例（包含长文本+复选框场景）
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置应用程序基础字体（统一样式）
    font = QFont("微软雅黑", 12)
    app.setFont(font)

    # 长文本测试内容
    long_text = """
    您即将执行批量删除操作，请注意以下事项：
    1. 本次删除将包含以下类型的数据：
       - 用户上传的本地文件（共25条）
       - 自动生成的临时缓存（共187条）
       - 过期的日志记录（共96条）
    2. 删除后的数据将无法通过常规方式恢复，如需恢复需联系管理员申请数据回溯；
    3. 操作执行时间预计需要30-60秒，期间请不要关闭程序或刷新页面；
    4. 确认删除前请确保已备份重要数据，避免不必要的损失。

    请问您确定要执行本次批量删除操作吗？
    """

    # 调用弹窗，获取两个返回值：是否确认、是否不再提示
    is_confirm, is_no_prompt = OperationConfirmDialog.get_confirmation(
        title="批量删除确认",
        text=long_text.strip()
    )
    # 打印结果
    if is_confirm:
        print("用户确认执行，开始批量删除操作...")
    else:
        print("用户取消操作，终止批量删除...")
    if is_no_prompt:
        print("用户勾选了“不再提示此提示框”，后续可不再弹出该弹窗")
    else:
        print("用户未勾选“不再提示”，后续仍会弹出该弹窗")

    sys.exit(app.exec_())