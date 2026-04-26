import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QFrame, QCheckBox, QLineEdit, QLabel, QMessageBox)  # 新增密码框、标签、消息框
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


from compents.load_path import load_path
from compents.log import logger
from compents.file_process import FileProcess
from compents.simple_cryptor import SimpleCryptor


class PasswordConfirmDialog(QDialog):
    def __init__(self, parent=None, title="密码验证", prompt_text="请输入操作密码：", correct_password="123456"):
        super().__init__(parent)
        # 基础设置
        self.setWindowTitle(title)
        self.setModal(True)  # 模态对话框
        self.setMinimumSize(400, 200)  # 调整最小尺寸适配密码框
        self.setMaximumSize(500, 220)  # 调整最大尺寸
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # 移除帮助按钮

        # 核心参数
        self.prompt_text = prompt_text  # 密码提示文本
        self.correct_password = correct_password  # 正确密码
        self.password_input = None  # 密码输入框
        self._init_ui()

    def _init_ui(self):
        # 1. 创建提示文本标签
        prompt_label = QLabel(self.prompt_text)
        prompt_label.setObjectName("PasswordDialogPromptLabel")
        prompt_label.setFont(QFont("微软雅黑", 12))
        prompt_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 2. 创建密码输入框（核心修改）
        self.password_input = QLineEdit()
        self.password_input.setObjectName("PasswordDialogInput")
        self.password_input.setEchoMode(QLineEdit.Password)  # 设置为密码模式，输入内容隐藏
        self.password_input.setFont(QFont("微软雅黑", 14))
        self.password_input.setMinimumHeight(40)  # 调整高度适配样式
        # 按Enter键触发确认
        self.password_input.returnPressed.connect(self._verify_password)

        # 3. 创建按钮（保持原有样式和尺寸）
        self.confirm_btn = QPushButton("确定")
        self.confirm_btn.setObjectName("PasswordDialogConfirmBtn")
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setObjectName("PasswordDialogCancelBtn")

        # 设置按钮固定大小
        btn_size = QSize(100, 40)
        self.confirm_btn.setFixedSize(btn_size)
        self.cancel_btn.setFixedSize(btn_size)

        # 4. 创建“不再提示”复选框（保留原有逻辑）
        self.no_prompt_check = QCheckBox("后续操作无需验证密码（不建议开启！）")
        self.no_prompt_check.setObjectName("PasswordDialogNoPromptCheck")
        self.no_prompt_check.setFont(QFont("微软雅黑", 12))

        # 5. 布局管理（适配密码框结构）
        # 密码输入区域布局
        password_layout = QVBoxLayout()
        password_layout.addWidget(prompt_label)
        password_layout.addWidget(self.password_input)
        password_layout.setSpacing(10)

        # 按钮水平布局（居中显示）
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addSpacing(20)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 15, 0, 10)

        # 复选框布局（靠右对齐）
        check_layout = QHBoxLayout()
        check_layout.addStretch()
        check_layout.addWidget(self.no_prompt_check)
        check_layout.setContentsMargins(0, 0, 20, 20)

        # 整体垂直布局：密码区域 → 按钮 → 复选框
        main_layout = QVBoxLayout()
        main_layout.addLayout(password_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(check_layout)
        main_layout.setContentsMargins(20, 20, 20, 0)
        main_layout.setSpacing(5)

        self.setLayout(main_layout)

        # 6. 绑定按钮事件
        self.confirm_btn.clicked.connect(self._verify_password)
        self.cancel_btn.clicked.connect(self.reject)

    def _verify_password(self):
        """密码验证逻辑"""
        input_pwd = self.password_input.text().strip()
        # 使用解密方式验证密码
        sim = SimpleCryptor(self.correct_password["key"])
        try:
            # 尝试解密存储的密码
            decrypted_password = sim.decrypt(self.correct_password["correct_password"])
            if input_pwd == decrypted_password:
                self.accept()  # 密码正确，确认对话框
            else:
                # 密码错误，弹出提示
                QMessageBox.warning(
                    self,
                    "密码错误",
                    "您输入的密码不正确，请重新输入！",
                    QMessageBox.Ok
                )
                self.password_input.clear()  # 清空输入框
                self.password_input.setFocus()  # 聚焦输入框
        except Exception as e:
            # 如果解密失败，使用简单加密进行验证
            encryption = sim.encrypt(input_pwd)
            if encryption == self.correct_password["correct_password"]:
                self.accept()  # 密码正确，确认对话框
            else:
                # 密码错误，弹出提示
                QMessageBox.warning(
                    self,
                    "密码错误",
                    "您输入的密码不正确，请重新输入！",
                    QMessageBox.Ok
                )
                self.password_input.clear()  # 清空输入框
                self.password_input.setFocus()  # 聚焦输入框

    @property
    def is_no_prompt(self):
        """获取“不再提示”复选框的状态"""
        return self.no_prompt_check.isChecked()

    @classmethod
    def get_password_confirmation(cls, parent=None, title="密码验证", prompt_text="请输入操作密码：", correct_password="123456"):
        """
        静态调用方法：快速获取密码验证结果 + 不再提示状态
        :param parent: 父窗口
        :param title: 对话框标题
        :param prompt_text: 密码提示文本
        :param correct_password: 正确的验证密码
        :return: tuple - (是否验证通过: bool, 是否不再提示: bool)
        """
        dialog = cls(parent, title, prompt_text, correct_password)
        verify_result = dialog.exec_() == cls.Accepted
        no_prompt_result = dialog.is_no_prompt
        return verify_result, no_prompt_result


def use_password_confirm_dialog_template(operation_dict, logger_dict, correct_password="123456"):
    """
    二次封装使用密码弹窗
    :param operation_dict: {parent:'', title:'', prompt_text:''}
    :param logger_dict: {cancel_msg:'', update_msg:'', wrong_pwd_msg:''}
    :param correct_password: {password:"",key:""}
    :return: bool -> 是否继续执行函数
    """
    # 如果已勾选不再提示，直接返回True
    if not load_path["prompt_box"]["diary_password_verification"]:
        is_verify_pass, is_no_prompt = PasswordConfirmDialog.get_password_confirmation(
            parent=operation_dict["parent"],
            title=operation_dict["title"],
            prompt_text=operation_dict["prompt_text"],
            correct_password=correct_password
        )
        if not is_verify_pass:
            logger.warning(logger_dict["cancel_msg"])
            return False

        if is_no_prompt and is_verify_pass:
            # 写入配置，后续无需验证
            FileProcess.write_json_attribute("config/file_path.json", ["prompt_box", "diary_password_verification"], is_no_prompt)
            logger.warning(logger_dict["update_msg"])
            load_path["prompt_box"]["diary_password_verification"] = is_no_prompt
            return True
    return True


# 测试示例
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置应用程序基础字体（统一样式）
    font = QFont("微软雅黑", 12)
    app.setFont(font)

    # 调用密码验证弹窗
    is_verify_pass, is_no_prompt = PasswordConfirmDialog.get_password_confirmation(
        title="批量删除操作验证",
        prompt_text="执行批量删除操作需要验证密码，请输入管理员密码："
    )

    # 打印结果
    if is_verify_pass:
        print("密码验证通过，开始执行批量删除操作...")
    else:
        print("用户取消操作或密码验证失败，终止批量删除...")
    if is_no_prompt:
        print("用户勾选了“后续无需验证密码”，后续操作将跳过密码验证")
    else:
        print("用户未勾选免验证，后续操作仍需密码验证")

    sys.exit(app.exec_())