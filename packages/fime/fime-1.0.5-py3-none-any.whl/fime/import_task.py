from fime.config import Config

try:
    from PySide6 import QtGui, QtWidgets
except ImportError:
    from PySide2 import QtGui, QtWidgets

from fime.task_completer import TaskCompleter
from fime.util import get_icon


class ImportTask(QtWidgets.QDialog):
    def __init__(self, config: Config, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("New Tasks")

        self.line_edit = QtWidgets.QLineEdit()
        completer = TaskCompleter(config)
        self.line_edit.setCompleter(completer)
        self.line_edit.textChanged.connect(completer.update_picker)

        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setIcon(get_icon("dialog-ok"))
        ok_button.pressed.connect(self.accept)
        ok_button.setAutoDefault(True)

        cancel_button = QtWidgets.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setIcon(get_icon("dialog-cancel"))
        cancel_button.pressed.connect(self.reject)
        cancel_button.setAutoDefault(False)

        blayout = QtWidgets.QHBoxLayout()
        blayout.addSpacing(300)
        blayout.addWidget(cancel_button)
        blayout.addWidget(ok_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addLayout(blayout)
        self.setLayout(layout)
        self.resize(500, 0)

    @property
    def task_text(self):
        return self.line_edit.text()

    def reset_task_text(self):
        self.line_edit.setText("")
