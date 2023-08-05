import sys

from PySide6.QtWidgets import QApplication
from import_task import ImportTask

app = QApplication()
nt = ImportTask(None)
nt.show()

app.exec_()
#print(r.report())
#print(r._actual_data_len)
#print(r.report()[:r._actual_data_len])
#print(l._data["2020-02"].keys())
