

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QPushButton, QSizePolicy, QCheckBox, QSpinBox, \
    QLineEdit, QHBoxLayout


class Pyqt5WidgetLayout:
    @staticmethod
    def create_border_block(title,layout_type="qv_layout",bg_color="#f8f9fa"):
        """
        创建边框块
        :param title: 边框内部标题
        :param layout_type:  边框布局类型 qv_layout,form_layout
        :param bg_color: 背景颜色
        :return: 返回部件和布局
        """
        border_block = QWidget()
        border_block.setContentsMargins(8,8,8,8)
        border_block.setObjectName("border_widget")
        border_block.setStyleSheet(f"background-color:{bg_color}")
        border_block_layout = None

        # 边框标题
        title = QLabel(title)
        title.setObjectName("title_border")

        if layout_type == "qv_layout":
            border_block_layout = QVBoxLayout(border_block)
            border_block_layout.addWidget(title)
        if layout_type == "form_layout":
            border_block_layout = QFormLayout(border_block)
            border_block_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            border_block_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            border_block_layout.addRow(title)

        border_block_layout.setSpacing(12)


        return border_block,border_block_layout


    @staticmethod
    def add_label(text,align=Qt.AlignLeft | Qt.AlignVCenter,obj_class="label_style",bg_color="transparent",warp=True):
        """
        添加一个新标签
        :param text: 标签内容
        :param align: 对齐方式 Qt对象
        :param obj_class qss 样式
        :param bg_color transparent
        :return: label_widget
        """
        new_label = QLabel(text)
        new_label.setAlignment(align)
        new_label.setWordWrap(warp)
        new_label.setObjectName(obj_class)
        new_label.setStyleSheet(f"""background-color:{bg_color}""")
        return new_label


    @staticmethod
    def add_button(text,obj_class="",size_width=180):
        """
        添加一个按钮
        :param text: 文本
        :param obj_class: 添加一个样式多行字符串
        :param size_width: 宽度
        :return:
        """
        button_widget = QPushButton(text)
        if not size_width is None:
            button_widget.setFixedWidth(size_width)
        button_widget.setFlat(False)
        button_widget.setCursor(Qt.PointingHandCursor)
        button_widget.setStyleSheet(obj_class)
        return button_widget

    @staticmethod
    def add_switch(text, checked=False, obj_class="switch_style"):
        """
        创建一个开关样式的复选框
        :param text: 开关旁边的文本（通常在form布局中，我们会把文本放在左边，所以这里可以留空）
        :param checked: 初始是否选中
        :param obj_class: QSS样式名
        :return: QCheckBox
        """
        switch = QCheckBox(text)
        switch.setChecked(checked)
        switch.setObjectName(obj_class)
        # 设置尺寸策略，防止开关被拉伸
        switch.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        return switch

    @staticmethod
    def add_spinbox(num,max_num=1440,min_num=5,obj_class="spinbox_style",width=150,align=Qt.AlignCenter):
        spin_box = QSpinBox()
        spin_box.setMinimum(min_num)
        spin_box.setMaximum(max_num)
        spin_box.setValue(num)
        if not width is None:
            spin_box.setMinimumWidth(width)
        spin_box.setAlignment(align)  # 数字居中显示
        spin_box.setObjectName(obj_class)
        return spin_box

    @staticmethod
    def add_edit(text,read_only=False,place="提示词",min_num=200,align=Qt.AlignLeft | Qt.AlignVCenter,obj_class="editor_style"):
        """
        输入框
        :param text: 默认提示框
        :param read_only: False
        :param place: 提示词
        :param min_num: 最小宽度
        :return: 返回 edit 实例
        """
        edit = QLineEdit()
        edit.setText(text)
        edit.setAlignment(align)
        edit.setReadOnly(read_only)
        edit.setPlaceholderText(place)
        edit.setObjectName(obj_class)
        edit.setStyleSheet("""border:1px solid #dddddd;""")
        edit.setMinimumWidth(min_num)
        return edit

    @staticmethod
    def create_div(direction="row"):
        div = QWidget()
        div.setContentsMargins(0,0,0,0)

        div_layout = None
        if direction == "row":
            div_layout = QHBoxLayout(div)
        if direction == "col":
            div_layout = QVBoxLayout(div)
        div_layout.setContentsMargins(0,0,0,0)
        div_layout.setSpacing(12)

        return div,div_layout

