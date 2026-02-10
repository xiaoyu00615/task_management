import logging
import os
import inspect
from logging.handlers import RotatingFileHandler
from typing import Optional
from datetime import datetime

# 定义日志颜色（控制台输出带颜色，便于快速区分级别）
LOG_COLORS = {
    logging.DEBUG: "\033[0;36m",  # 青色
    logging.INFO: "\033[0;32m",   # 绿色
    logging.WARNING: "\033[0;33m",# 黄色
    logging.ERROR: "\033[0;31m",  # 红色
    logging.CRITICAL: "\033[0;35m"# 紫色
}
RESET_COLOR = "\033[0m"  # 重置颜色

class ColoredFormatter(logging.Formatter):
    """自定义带颜色的日志格式器，仅控制台输出生效"""
    def format(self, record: logging.LogRecord) -> str:
        color = LOG_COLORS.get(record.levelno, "")
        log_msg = super().format(record)
        return f"{color}{log_msg}{RESET_COLOR}"

class CommonLogger:
    """Python通用日志类（单例+控制台+分层文件存储+按大小切割）
    日志目录结构：logs/YYYY-MM-DD/HH-MM-SS.log（每次运行生成独立文件，按日期分类）
    精准显示：真实业务调用方的【文件名 - ln:行号】，格式[时间] - 级别 - 文件名 - ln:行号 - 信息
    兼容Python3.2+：解决extra覆盖内置字段的KeyError问题
    """
    # 单例实例
    _instance: Optional["CommonLogger"] = None
    # 日志格式：严格匹配要求 [时间] - 级别 - 文件名 - ln:行号 - 信息
    _LOG_FORMAT = "[%(asctime)s] - %(levelname)s - %(caller_filename)s - ln:%(caller_lineno)d - %(message)s"
    # 时间格式（保持原有）
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __new__(cls, *args, **kwargs):
        """单例模式：确保全局只有一个日志实例，避免重复输出/重复创建文件"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        logger_name: str = "python_common_log",  # 日志器名称
        log_level: int = logging.INFO,           # 日志级别
        root_log_dir: str = "logs",              # 日志根目录
        max_file_size: int = 10 * 1024 * 1024,   # 单个日志文件最大大小（10MB）
        backup_count: int = 3,                   # 单文件备份数量（切割用）
        console_output: bool = True,             # 是否输出到控制台
        file_output: bool = True,                # 是否输出到文件
        file_suffix: str = "log"                 # 日志文件后缀（默认log）
    ):
        # 单例模式下避免重复初始化处理器和文件
        if hasattr(self, "_logger"):
            return

        # 1. 初始化基础参数，获取程序启动时间（固定不变）
        self._now = datetime.now()
        self._date_dir = self._now.strftime("%Y-%m-%d")
        self._file_name = self._now.strftime("%H-%M-%S")
        self._file_suffix = file_suffix.strip(".")
        self._root_log_dir = root_log_dir
        # 记录当前日志框架文件的绝对路径（用于精准排除）
        self._current_log_file = os.path.abspath(__file__)

        # 2. 获取日志器并配置基础属性
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(log_level)
        self._logger.propagate = False  # 关闭根日志传播，避免重复输出

        # 3. 递归创建分层日志目录
        if file_output:
            self._log_full_dir = os.path.join(self._root_log_dir, self._date_dir)
            os.makedirs(self._log_full_dir, exist_ok=True)
            self._log_file_path = os.path.join(
                self._log_full_dir,
                f"{self._file_name}.{self._file_suffix}"
            )

        # 4. 定义格式器（控制台带颜色，文件无颜色，格式统一）
        file_formatter = logging.Formatter(fmt=self._LOG_FORMAT, datefmt=self._DATE_FORMAT)
        console_formatter = ColoredFormatter(fmt=self._LOG_FORMAT, datefmt=self._DATE_FORMAT)

        # 5. 添加处理器（控制台+文件，保留所有原功能）
        if console_output:
            self._add_console_handler(console_formatter)
        if file_output:
            self._add_file_handler(file_formatter, max_file_size, backup_count)

    def _get_caller_info(self):
        """核心：精准获取真实业务调用方的【文件名+行号】
        遍历调用栈，跳过日志框架自身、logging模块的帧，返回第一个业务文件的信息
        """
        # 获取完整调用栈，从外层到内层遍历（跳过当前方法、日志方法的帧）
        frames = inspect.stack()[2:]
        for frame in frames:
            file_path = os.path.abspath(frame.filename)
            # 排除：当前日志文件、logging内置模块文件
            if file_path == self._current_log_file or "logging/__init__.py" in file_path:
                continue
            # 返回真实调用方的【文件名（仅basename）+ 行号】
            return os.path.basename(file_path), frame.lineno
        # 兜底：若未找到，返回默认信息（避免报错）
        return "unknown_file.py", 0

    def _add_console_handler(self, formatter: logging.Formatter):
        """添加控制台处理器（原逻辑不变）"""
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def _add_file_handler(
        self,
        formatter: logging.Formatter,
        max_file_size: int,
        backup_count: int
    ):
        """添加分层文件处理器（按大小切割，备份文件同目录，原逻辑不变）"""
        file_handler = RotatingFileHandler(
            filename=self._log_file_path,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding="utf-8",  # 强制utf-8，解决中文乱码
            delay=False        # 立即创建文件
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    # 重写所有日志方法：用自定义字段传递调用方信息，避免覆盖内置字段
    def debug(self, msg: str, *args, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.debug(msg, *args, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.info(msg, *args, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.warning(msg, *args, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.error(msg, *args, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.critical(msg, *args, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

    # 异常记录快捷方法：同样用自定义字段，精准定位真实调用方
    def exception(self, msg: str, *args, exc_info=True, **kwargs):
        caller_filename, caller_lineno = self._get_caller_info()
        self._logger.error(msg, *args, exc_info=exc_info, extra={
            "caller_filename": caller_filename,
            "caller_lineno": caller_lineno
        }, **kwargs)

# 初始化全局通用日志实例（开箱即用，调用方式和之前完全一样！）
logger = CommonLogger(
    log_level=logging.DEBUG,
    file_suffix="log"
)