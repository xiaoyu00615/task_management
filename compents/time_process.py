import datetime
from compents.log import logger


class TimeProcess:
    FORMAT_TEMPLATE = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def calculate_time_poor(start_time:str, end_time:str,rest_type="second",format_str=True):
        """
        计算时间差 datetime
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param rest_type: 处理类型 second, minute, hour, day, week, month, str
        :param format_str: 结果bool -> True -> 格式化后的字符串
        :return: 返回对应数据
        """
        # 字符串转换为 -> datetime 进行计算
        dt_start = datetime.datetime.strptime(start_time, TimeProcess.FORMAT_TEMPLATE)
        dt_end = datetime.datetime.strptime(end_time, TimeProcess.FORMAT_TEMPLATE)

        time_poor = dt_end - dt_start
        total_seconds = time_poor.total_seconds()

        if rest_type == "second":
            return total_seconds

        if rest_type == "minute":
            return total_seconds // 60

        if rest_type == "hour":
            return total_seconds // 3600

        if rest_type == "day":
            return total_seconds // 86400

        if rest_type == "week":
            return total_seconds // 604800

        if rest_type == "month":
            return total_seconds // 31557600

        if rest_type == "str":
            if not format_str:
                return time_poor

            return TimeProcess.seconde_format(total_seconds)

        return None

    @staticmethod
    def seconde_format(total_seconds):
        # print(total_seconds, "全部秒数")
        """
        格式化日期
        :param total_seconds: 总秒数
        :return: 格式化日期
        """
        if total_seconds < 0:
            total_seconds = 0  # 处理负秒数，返回0秒

        # 1. 核心换算：拆出总天数和当日剩余秒数
        seconds_per_day = 86400
        total_days = total_seconds // seconds_per_day  # 总天数
        remain_seconds = total_seconds % seconds_per_day  # 当日剩余秒数

        # 2. 拆分当日剩余秒数为 时、分、秒
        hours = int(remain_seconds // 3600)
        minutes = int((remain_seconds % 3600) // 60)
        seconds = int(remain_seconds % 60)

        # 3. 换算总天数为 年、月、剩余天（按平均标准）
        days_per_year = 365
        days_per_month = 30
        years = int(total_days // days_per_year)  # 年数
        remain_days_after_year = total_days % days_per_year  # 年剩余天数
        months = int(remain_days_after_year // days_per_month)  # 月数
        days = int(remain_days_after_year % days_per_month)  # 月剩余天数

        # 修复：重新梳理判断逻辑，按 年→月→总天数 的层级显示
        # 有年：显示 年+月+天+时+分+秒
        if years > 0:
            return f"{years}年{months}月{int(days)}天{hours}时{minutes}分{seconds}秒"
        # 有月无年：显示 月+天+时+分+秒
        elif months > 0:
            return f"{months}月{int(days)}天{hours}时{minutes}分{seconds}秒"
        # 有天无月无年：显示 总天数+时+分+秒（关键：用total_days而非days）
        elif total_days > 0:
            return f"{int(total_days)}天{hours}时{minutes}分{seconds}秒"
        # 无天：显示 时/分秒/秒
        else:
            if hours > 0:
                return f"{hours}时{minutes}分{seconds}秒"
            elif minutes > 0:
                return f"{minutes}分{seconds}秒"
            else:
                return f"{seconds}秒"

    @staticmethod
    def get_time_percent(create_time:str,end_time:str) -> int:
        """
        获取时间比率
        :param create_time: 创建时间
        :param end_time: 结束时间
        :return: 对应的数值
        """
        try:
            dt_create = datetime.datetime.strptime(create_time,TimeProcess.FORMAT_TEMPLATE)
            dt_end = datetime.datetime.strptime(end_time,TimeProcess.FORMAT_TEMPLATE)
            dt_now = datetime.datetime.now()

            # 时间差
            total_poor = (dt_end - dt_create).total_seconds()

            # 已过时间
            pass_through = (dt_now - dt_create).total_seconds()

            if total_poor <= 0:
                return 100

            percent = int((pass_through / total_poor) * 100)
            # print(percent)
            return percent
        except Exception as e:
            logger.error(f"获取进度率失败 -> {e}")




if __name__ == '__main__':
    print(TimeProcess.calculate_time_poor("2026-02-03 20:50:31","2027-09-03 20:51:00","str"," %H时%M分%S秒"))