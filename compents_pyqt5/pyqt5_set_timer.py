from PyQt5.QtCore import QTimer, Qt
from typing import Optional, Callable


class Pyqt5SetTimer:
    # 字典存储多任务计时器：key=任务唯一标识，value=QTimer实例
    _timer_instances = {}

    @classmethod
    def init_task_timer(cls, task_id: str, timer_ms: int, call_back: Callable, parent=None):
        """
        初始化指定任务的计时器（若已存在则更新并重启）
        :param task_id: 任务唯一标识（如"refresh_list"、"auto_save"）
        :param timer_ms: 计时间隔（毫秒）
        :param call_back: 该任务计时器触发的回调函数
        :param parent: 父控件（避免内存泄漏）
        :return: 该任务的QTimer实例
        """
        # 若该任务已有计时器，先停止并复用
        if task_id in cls._timer_instances:
            timer = cls._timer_instances[task_id]
            timer.stop()
            timer.setInterval(timer_ms)
            # 断开旧回调（避免重复绑定）
            try:
                timer.timeout.disconnect()
            except TypeError:
                # 无绑定的回调时忽略错误
                pass
            timer.timeout.connect(call_back)
            timer.start()
            print(f"任务[{task_id}]计时器已更新并重启，间隔：{timer_ms}ms")
        else:
            # 新建计时器实例
            timer = QTimer(parent)
            timer.setInterval(timer_ms)
            timer.timeout.connect(call_back)
            timer.start()
            cls._timer_instances[task_id] = timer
            print(f"任务[{task_id}]计时器已初始化，间隔：{timer_ms}ms")

        return cls._timer_instances[task_id]

    @classmethod
    def update_task_timer_interval(cls, task_id: str, new_timer_ms: int):
        """
        动态更新指定任务的计时器间隔
        :param task_id: 任务唯一标识
        :param new_timer_ms: 新的计时间隔（毫秒）
        """
        if task_id not in cls._timer_instances:
            print(f"警告：任务[{task_id}]的计时器未初始化！")
            return

        timer = cls._timer_instances[task_id]
        timer.setInterval(new_timer_ms)
        # 可选：停止后重启（确保间隔立即生效，部分场景需要）
        # timer.stop()
        # timer.start()
        print(f"任务[{task_id}]计时器间隔已更新为：{new_timer_ms}ms")

    @classmethod
    def stop_task_timer(cls, task_id: str):
        """停止指定任务的计时器"""
        if task_id in cls._timer_instances:
            cls._timer_instances[task_id].stop()
            print(f"任务[{task_id}]计时器已停止")
        else:
            print(f"警告：任务[{task_id}]的计时器未初始化！")

    @classmethod
    def remove_task_timer(cls, task_id: str):
        """停止并删除指定任务的计时器（释放内存）"""
        if task_id in cls._timer_instances:
            cls._timer_instances[task_id].stop()
            del cls._timer_instances[task_id]
            print(f"任务[{task_id}]计时器已删除")

    @classmethod
    def stop_all_timers(cls):
        """停止所有任务的计时器（如程序退出时）"""
        for task_id in cls._timer_instances:
            cls._timer_instances[task_id].stop()
        print(f"所有计时器已停止，共{len(cls._timer_instances)}个任务")


# ==================== 调用示例（模拟多任务场景）====================
if __name__ == "__main__":
    # 定义不同任务的回调函数
    def task1_callback():
        """任务1：列表自动刷新"""
        print("【任务1】执行列表刷新...")


    def task2_callback():
        """任务2：自动保存数据"""
        print("【任务2】执行数据自动保存...")


    def task3_callback():
        """任务3：同步远程数据"""
        print("【任务3】执行远程数据同步...")


    # 1. 初始化3个任务的计时器（不同间隔）
    parent = None  # 实际使用时传入你的窗口实例（如self）
    Pyqt5SetTimer.init_task_timer("task_refresh_list", 1000, task1_callback, parent)  # 1秒
    Pyqt5SetTimer.init_task_timer("task_auto_save", 5000, task2_callback, parent)  # 5秒
    Pyqt5SetTimer.init_task_timer("task_data_sync", 10000, task3_callback, parent)  # 10秒

    # 2. 配置修改后，单独更新任务2的计时器间隔（比如从5秒改为3秒）
    Pyqt5SetTimer.update_task_timer_interval("task_auto_save", 3000)

    # 3. 单独停止任务3的计时器
    # Pyqt5SetTimer.stop_task_timer("task_data_sync")

    # 4. 删除任务3的计时器（彻底释放）
    # Pyqt5SetTimer.remove_task_timer("task_data_sync")

    # 5. 程序退出时停止所有计时器
    # Pyqt5SetTimer.stop_all_timers()