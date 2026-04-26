"""通知工具模块

该模块用于发送系统通知，包括任务提醒等功能。
"""

from plyer import notification
from compents.log import logger


class NotificationTool:
    @staticmethod
    def send_task_reminder(task_name, deadline):
        """
        发送任务提醒通知
        :param task_name: 任务名称
        :param deadline: 任务截止时间
        :return: bool
        """
        try:
            notification.notify(
                title="任务提醒",
                message=f"任务 '{task_name}' 即将到期，截止时间：{deadline}",
                app_name="Task Management",
                timeout=10  # 通知显示10秒
            )
            logger.info(f"发送任务提醒通知成功：{task_name}")
            return True
        except Exception as e:
            logger.error(f"发送任务提醒通知失败：{e}")
            return False
    
    @staticmethod
    def send_generic_notification(title, message):
        """
        发送通用通知
        :param title: 通知标题
        :param message: 通知内容
        :return: bool
        """
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Task Management",
                timeout=10
            )
            logger.info(f"发送通用通知成功：{title}")
            return True
        except Exception as e:
            logger.error(f"发送通用通知失败：{e}")
            return False
