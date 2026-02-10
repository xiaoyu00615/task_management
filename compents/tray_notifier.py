import plyer
import pystray
from PIL import Image, ImageDraw, ImageFont
from threading import Thread
import sys
import time

# 通用单例装饰器（保留原实现，解耦不侵入业务）
def singleton(cls):
    _instances = {}
    def wrapper(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return wrapper

# 美化版托盘通知+常驻菜单核心类（单例/高扩展/美观化）
@singleton
class TrayNotifier():
    def __init__(self, default_duration: int = 2, tray_icon=None, tray_title="我的托盘工具"):
        """
        初始化美化版托盘（含通知+常驻菜单）
        :param default_duration: 通知默认显示时间（秒），可单次覆盖
        :param tray_icon: 托盘图标（本地路径，如"icon.ico"，None则使用默认纯文本图标）
        :param tray_title: 托盘悬浮提示文字
        """
        # 基础配置
        self.default_duration = default_duration
        self.tray_title = tray_title
        self.tray = None  # 托盘实例，延迟初始化
        self.icon = self._create_tray_icon(tray_icon)  # 初始化托盘图标

        # 启动托盘常驻线程（非阻塞，不影响主程序）
        self._start_tray_thread()

    def _create_tray_icon(self, icon_path):
        """创建托盘图标：自定义路径/默认纯文本图标（避免无图标文件问题）"""
        if icon_path:
            # 加载本地图标文件（支持ico/png/jpg，自动适配尺寸）
            try:
                return Image.open(icon_path)
            except Exception as e:
                print(f"加载自定义图标失败，使用默认图标：{e}")

        # 默认纯文本图标（生成256x256黑色背景+白色"通"字，系统会自动缩放）
        icon_size = (256, 256)
        image = Image.new("RGBA", icon_size, (0, 0, 0, 255))  # 不透明黑色背景
        draw = ImageDraw.Draw(image)
        # 尝试加载系统字体，兼容跨平台
        try:
            font = ImageFont.truetype("simhei.ttf", 120)  # Windows黑体
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", 120)  # macOS/Linux
            except:
                font = ImageFont.load_default(size=120)  # 兜底默认字体
        # 文字居中绘制
        text = "通"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (icon_size[0] - text_width) // 2
        y = (icon_size[1] - text_height) // 2
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))  # 白色文字
        return image

    def _create_tray_menu(self):
        """创建托盘右键菜单：关闭通知、创建任务、关于、退出（可动态扩展）"""
        return pystray.Menu(
            # 菜单项1：关闭所有通知（跨平台通用实现）
            pystray.MenuItem("关闭通知", self._action_close_notify, enabled=True),
            # 菜单项2：创建任务（预留扩展接口，可自定义业务逻辑）
            pystray.MenuItem("创建任务", self._action_create_task, enabled=True),
            # 分隔符（优化菜单布局，更美观）
            pystray.Menu.SEPARATOR,
            # 菜单项3：关于（显示工具信息）
            pystray.MenuItem("关于", self._action_about, enabled=True),
            # 菜单项4：退出程序（关闭托盘+退出主进程）
            pystray.MenuItem("退出", self._action_quit, enabled=True)
        )

    def _start_tray_thread(self):
        """启动守护线程运行托盘，避免阻塞主程序"""
        def tray_run():
            # 初始化托盘：图标+标题+右键菜单
            self.tray = pystray.Icon(
                name=self.tray_title,
                icon=self.icon,
                title=self.tray_title,
                menu=self._create_tray_menu()
            )
            # 运行托盘（阻塞线程，守护线程随主进程退出）
            self.tray.run()

        # 启动守护线程
        self.tray_thread = Thread(target=tray_run, daemon=True)
        self.tray_thread.start()
        # 等待托盘初始化完成（避免立即调用托盘方法报错）
        time.sleep(0.5)

    # ---------------------- 通知核心方法（美化+可调节时长） ----------------------
    def send_notify(self, title: str, content: str, duration: int = None, align: bool = True):
        """
        发送美化版托盘通知（支持格式优化、时长调节）
        :param title: 通知标题
        :param content: 通知内容（支持\n换行、-/*分隔符，自动格式化）
        :param duration: 本次显示时间（秒），None则用全局默认
        :param align: 是否内容对齐（美化布局，默认开启）
        """
        # 时长优先级：单次调用 > 全局默认
        show_duration = duration if duration is not None else self.default_duration
        # 内容美化格式化（核心布局优化，解决单调问题）
        beautified_content = self._beautify_content(content, align)
        # 发送跨平台美化通知
        plyer.notification.notify(
            title=f"【{title}】",  # 标题加符号包裹，更醒目
            message=beautified_content,
            timeout=show_duration,
            app_name=self.tray_title  # 通知归属应用名，美化通知头部
        )
        self.after_send(title, beautified_content)  # 调用后置钩子

    def _beautify_content(self, content: str, align: bool):
        """内容美化核心：换行整理、分隔符优化、左对齐补全"""
        # 替换特殊分隔符，统一格式
        content = content.replace("|", "\n").replace("；", "\n").replace("；", "\n")
        # 按行分割并去除空行
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        if not lines:
            return "无通知内容"
        # 左对齐补全（优化布局，使内容整齐）
        if align:
            max_len = max([len(line) for line in lines])
            lines = [line.ljust(max_len) for line in lines]
        # 拼接美化符号，提升视觉效果
        return "\n".join([f"• {line} •" for line in lines])

    # ---------------------- 托盘菜单核心功能（可扩展） ----------------------
    def _action_close_notify(self, icon, item):
        """关闭所有通知：跨平台通用处理"""
        self.send_notify("操作反馈", "已关闭所有托盘通知\n通知中心历史可在系统设置中清除", duration=3)
        # 可添加系统级关闭通知逻辑（如Windows通知中心、macOS通知中心）
        self.after_close_notify()  # 关闭通知后置钩子

    def _action_create_task(self, icon, item):
        """创建任务：核心扩展接口，可自定义业务逻辑（如创建定时任务、新建文件等）"""
        self.send_notify("任务创建", "开始执行任务创建逻辑\n✅ 可扩展：新建文件/定时任务/调用接口\n✅ 支持传参/多任务批量创建", duration=4)
        # ------------- 此处添加自定义业务逻辑 -------------
        # 示例1：创建本地文本文件
        # with open("新建任务.txt", "w", encoding="utf-8") as f:
        #     f.write(f"任务创建时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n任务描述：自定义任务")
        # 示例2：调用其他业务函数
        # self.custom_task_fun("参数1", "参数2")
        # --------------------------------------------------
        self.after_create_task()  # 创建任务后置钩子

    def _action_about(self, icon, item):
        """关于：显示工具信息"""
        about_info = "美化版Python托盘工具\n版本：v2.0\n特性：单例/美化布局/右键菜单\n支持：Windows/macOS/Linux"
        self.send_notify("关于托盘工具", about_info, duration=5)

    def _action_quit(self, icon, item):
        """退出程序：关闭托盘+终止主进程"""
        self.send_notify("程序退出", "即将退出托盘工具\n感谢使用，下次见！", duration=2)
        # 延迟退出，确保通知显示
        time.sleep(2)
        # 停止托盘运行
        if self.tray:
            self.tray.stop()
        # 终止主进程
        sys.exit(0)

    # ---------------------- 全局扩展钩子（对扩展开放，对修改关闭） ----------------------
    def after_send(self, title, content):
        """通知发送后钩子：可重写实现日志、统计、回调"""
        pass

    def after_close_notify(self):
        """关闭通知后钩子：可重写实现日志、状态更新"""
        pass

    def after_create_task(self):
        """创建任务后钩子：可重写实现任务回调、结果通知"""
        pass

    def custom_task_fun(self, *args, **kwargs):
        """自定义任务扩展方法：可重写实现具体业务"""
        pass

# 单一实例化
tray = TrayNotifier(
    default_duration=4,  # 全局默认通知显示4秒
    tray_title="美化版托盘工具",  # 托盘悬浮提示文字
    # tray_icon="your_icon.ico"  # 可选：自定义托盘图标路径
)


# ------------------- 测试使用示例（直接运行，效果立现） -------------------
if __name__ == "__main__":
    # 1. 初始化单例托盘实例（全局仅一个，参数可配）
    # 不传tray_icon则用默认"通"字图标，传本地路径如"icon.ico"可自定义
    tray = TrayNotifier(
        default_duration=4,  # 全局默认通知显示4秒
        tray_title="美化版托盘工具",  # 托盘悬浮提示文字
        # tray_icon="your_icon.ico"  # 可选：自定义托盘图标路径
    )

    # 2. 发送基础美化通知（自动格式化，布局美观）
    tray.send_notify(
        title="基础美化通知",
        content="这是优化布局后的通知\n支持自动换行•分隔符美化•左对齐\n解决原纯文本单调问题！"
    )

    # 3. 自定义时长通知（覆盖全局默认，本次显示6秒）
    time.sleep(5)  # 延迟显示，避免通知重叠
    tray.send_notify(
        title="自定义时长",
        content="本次通知显示6秒|优先级高于全局默认|支持多种分隔符自动转换",
        duration=6
    )

    # 4. 验证单例模式（多次实例化返回同一个对象）
    time.sleep(7)
    tray2 = TrayNotifier()
    print(f"是否为同一个实例：{tray is tray2}")  # 输出：True

    # 5. 单例复用发送通知
    tray2.send_notify(
        title="单例复用",
        content="多次实例化仍为同一个对象|避免资源重复占用|托盘常驻不中断",
        duration=5
    )

    # 6. 保持主程序运行（否则守护线程随主进程退出，托盘消失）
    print("✅ 托盘已常驻系统显示隐藏图标区域！")
    print("✅ 右键托盘图标可执行：关闭通知/创建任务/关于/退出")
    print("✅ 按Ctrl+C终止程序（或右键托盘选择「退出」）")
    while True:
        time.sleep(1)