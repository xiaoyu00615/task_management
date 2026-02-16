
class ToolDef:

    @staticmethod
    def del_all_tasks_ui(del_layout):
        while del_layout.count():
            item = del_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        return True