#!/usr/bin/env python3
import signal
import sys
from functools import partial
from pathlib import Path

import desktop_file

from fime.config import Config

try:
    from PySide6 import QtCore, QtWidgets
    PYSIDE_6 = True
except ImportError:
    from PySide2 import QtCore, QtWidgets
    PYSIDE_6 = False

# noinspection PyUnresolvedReferences
import fime.icons
from fime.data import Tasks, Log, Data
from fime.exceptions import FimeException
from fime.import_task import ImportTask
from fime.report import Report
from fime.task_edit import TaskEdit
from fime.util import get_screen_height, get_icon


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        data = Data()
        self.tasks = Tasks(data)
        self.log = Log(data)
        self._active_task = self.log.last_log() or "Nothing"

        self.config = Config()
        if self.config.tray_theme == "light":
            icon = get_icon("appointment-new-light")
        else:
            icon = get_icon("appointment-new")

        self.menu = QtWidgets.QMenu(None)

        self.import_task = ImportTask(self.config, None)
        self.import_task.accepted.connect(self.new_task_imported)

        self.taskEdit = TaskEdit(None)
        self.taskEdit.accepted.connect(self.tasks_edited)

        self.reportDialog = Report(self.tasks, None)
        self.reportDialog.accepted.connect(self.report_done)

        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("fime")
        self.update_tray_menu()

    @QtCore.Slot()
    def new_task_imported(self):
        if self.import_task.task_text:
            self.tasks.add_jira_task(self.import_task.task_text)
            self.update_tray_menu()

    @QtCore.Slot()
    def tasks_edited(self):
        self.tasks.tasks = self.taskEdit.tasks
        self.update_tray_menu()

    @QtCore.Slot()
    def report_done(self):
        self.active_task = self.log.last_log() or "Nothing"

    @property
    def active_task(self):
        return self._active_task

    @active_task.setter
    def active_task(self, task):
        self._active_task = task
        self.tasks.update_jira_task_usage(self._active_task)
        self.update_tray_menu()

    def change_task(self, task):
        self.active_task = task
        self.log.log(task)

    def update_tray_menu(self):
        def add_tasks(tasks):
            for t in tasks:
                action = self.menu.addAction(t)
                action.triggered.connect(partial(self.change_task, t))
                if t == self.active_task:
                    action.setIcon(get_icon("go-next"))

        tmp_action = self.menu.addAction("tmp")
        action_height = self.menu.actionGeometry(tmp_action).height()

        self.menu.clear()
        add_tasks(self.tasks.tasks)

        self.menu.addSeparator()
        already_taken = (len(self.tasks.tasks) + 4) * action_height
        available_space = get_screen_height(self.menu) * 0.8 - already_taken
        jira_entry_count = int(available_space // action_height)
        add_tasks(self.tasks.jira_tasks[:jira_entry_count])

        self.menu.addSeparator()
        add_tasks(["Pause"])
        if self.active_task == "Nothing":
            add_tasks(["Nothing"])

        self.menu.addSeparator()

        new_action = self.menu.addAction("Import Jira task")
        new_action.triggered.connect(self.new_task_slot)

        edit_action = self.menu.addAction("Edit tasks")
        edit_action.triggered.connect(self.edit_tasks)

        report_action = self.menu.addAction("Report")
        report_action.triggered.connect(self.report)

        self.menu.addSeparator()

        exit_action = self.menu.addAction("Close")
        exit_action.triggered.connect(self.app.quit)

    def sigterm_handler(self, signo, _frame):
        print(f'handling signal "{signal.strsignal(signo)}"')
        self.app.quit()

    @staticmethod
    def write_icon():
        icon_path = str(Path(__file__).parent / "fime.svg")
        if "main" not in sys.argv[0]:
            QtCore.QFile.copy(":/icons/appointment-new.svg", icon_path)
        return icon_path

    @staticmethod
    def create_shortcut(icon_path):
        shortcut_file = Path(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)) \
                     / "shortcut"
        print(f"shortcut file: {shortcut_file}")
        shortcut_file_contents = ""
        if shortcut_file.exists():
            with open(shortcut_file, "r") as f:
                shortcut_file_contents = f.read()
        if shortcut_file_contents.strip() == __file__:
            return
        shortcut = desktop_file.Shortcut(desktop_file.getMenuPath(), "fime", sys.argv[0])
        shortcut.setTitle("Fime")
        shortcut.setComment("Simple time tracking app written with Python and Qt")
        shortcut.setIcon(icon_path)
        shortcut.save()
        if "main" not in sys.argv[0]:
            print("Successfully created menu shortcut")
            shortcut_file.parent.mkdir(parents=True, exist_ok=True)
            with open(shortcut_file, "w") as f:
                f.write(__file__)

    def run(self):
        icon_path = self.write_icon()
        self.create_shortcut(icon_path)
        timer = QtCore.QTimer(None)
        # interrupt event loop regularly for signal handling
        timer.timeout.connect(lambda: None)
        timer.start(500)
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGINT, self.sigterm_handler)
        if PYSIDE_6:
            self.app.exec()
        else:
            self.app.exec_()

    @QtCore.Slot()
    def report(self):
        self.reportDialog.set_data(self.log.report())
        self.reportDialog.show()

    @QtCore.Slot()
    def new_task_slot(self):
        self.import_task.reset_task_text()
        self.import_task.show()

    @QtCore.Slot()
    def edit_tasks(self):
        self.taskEdit.tasks = self.tasks.tasks
        self.taskEdit.show()


def main():
    try:
        # important for QStandardPath to be correct
        QtCore.QCoreApplication.setApplicationName("fime")
        app = App()
        app.run()
    except FimeException as e:
        QtWidgets.QMessageBox.critical(None, "Error", str(e), QtWidgets.QMessageBox.Ok)


if __name__ == "__main__":
    main()
