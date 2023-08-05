import atexit
import base64
import json
import os
from collections.abc import MutableMapping
from datetime import datetime, date, timedelta
from threading import Thread, Event
from typing import List

try:
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtCore

save_delay = 3 * 60
max_jira_tasks = 50


class Tasks:
    def __init__(self, data):
        self._data = data
        if "tasks" in self._data:
            self._tasks = list(map(lambda x: base64.b64decode(x.encode("utf-8")).decode("utf-8"), self._data["tasks"]))
        else:
            self._tasks = []
        if "jira_tasks" in self._data:
            self._jira_tasks_usage = dict()
            for k, v in self._data["jira_tasks"].items():
                key = base64.b64decode(k.encode("utf-8")).decode("utf-8")
                self._jira_tasks_usage[key] = datetime.fromisoformat(v)
                self._jira_tasks = sorted(self._jira_tasks_usage.keys(), key=lambda x: self._jira_tasks_usage[x])
        else:
            self._jira_tasks_usage = dict()
            self._jira_tasks = []

    @property
    def tasks(self) -> List[str]:
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks
        encoded_tasks = list(map(lambda x: base64.b64encode(x.encode("utf-8")).decode("utf-8"), self._tasks))
        self._data["tasks"] = encoded_tasks

    @property
    def jira_tasks(self):
        return self._jira_tasks

    def add_jira_task(self, task_name):
        if task_name in self._jira_tasks_usage:
            self._jira_tasks.remove(task_name)  # move to end, to make visible again
        self._jira_tasks.append(task_name)
        self._jira_tasks_usage[task_name] = datetime.now()
        if len(self._jira_tasks_usage) > max_jira_tasks:
            sorted_tasks = sorted(self._jira_tasks_usage.keys(), key=lambda x: self._jira_tasks_usage[x])
            overhang_tasks = sorted_tasks[:len(sorted_tasks) - max_jira_tasks]
            for task in overhang_tasks:
                del self._jira_tasks_usage[task]
        self._save_jira_tasks()

    def update_jira_task_usage(self, task_name):
        if task_name in self._jira_tasks_usage:
            self._jira_tasks_usage[task_name] = datetime.now()
            self._save_jira_tasks()

    def _save_jira_tasks(self):
        serialized = dict()
        for k, v in self._jira_tasks_usage.items():
            key = base64.b64encode(k.encode("utf-8")).decode("utf-8")
            serialized[key] = datetime.isoformat(v)
        self._data["jira_tasks"] = serialized

    @property
    def all_tasks(self):
        return self.tasks + self.jira_tasks


class Data(MutableMapping):
    def __init__(self):
        data_dir_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
        self.data_path = os.path.join(data_dir_path, "data_{}.json")
        if not os.path.exists(data_dir_path):
            os.mkdir(data_dir_path)
        self._cache = {}
        self._hot_keys = set()
        self._trunning = False
        self._tevent = Event()
        self._thread = None

        def cleanup():
            self._trunning = False
            self._tevent.set()
            if self._thread:
                self._thread.join()

        atexit.register(cleanup)

    def __getitem__(self, key):
        dpath = self.data_path.format(key)
        if key not in self._cache and os.path.exists(dpath):
            with open(dpath, "r") as f:
                self._cache[key] = json.loads(f.read())
        return self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value
        self._hot_keys.add(key)
        self._schedule_save()

    def _schedule_save(self):
        if self._trunning:
            return
        self._trunning = True
        self._thread = Thread(target=self._executor, daemon=True)
        self._thread.start()

    def _executor(self):
        while self._trunning:
            self._tevent.wait(save_delay)
            self._save()

    def _save(self):
        for key in self._hot_keys:
            print(f"... saving dict {key} ...")
            to_write = self._cache[key]  # apparently thread-safe
            with open(self.data_path.format(key), "w+") as f:
                f.write(json.dumps(to_write))
        self._hot_keys = set()
        self._saving = False

    def __delitem__(self, key):
        return NotImplemented

    def __iter__(self):
        return NotImplemented

    def __len__(self):
        # TODO use glob?
        return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self._cache})"


class Log:
    def __init__(self, data):
        self._data = data

        def cleanup():
            self.log("End")

        atexit.register(cleanup)

    def log(self, task, ptime=None):
        if ptime is None:
            ptime = datetime.now()
        # round to nearest minute
        round_min = timedelta(minutes=round(ptime.second/60))
        ptime = ptime - timedelta(seconds=ptime.second) + round_min
        # month dance necessary to trigger Data.__setitem__
        month = self._data.setdefault(ptime.strftime("%Y-%m"), {})
        month.setdefault(ptime.strftime("%d"), [])\
            .append(f"{ptime.strftime('%H:%M')} {base64.b64encode(task.encode('utf-8')).decode('utf-8')}")
        self._data[ptime.strftime("%Y-%m")] = month

    def last_log(self, pdate=None):
        if pdate is None:
            pdate = date.today()
        if pdate.strftime("%Y-%m") not in self._data \
                or pdate.strftime("%d") not in self._data[pdate.strftime("%Y-%m")] \
                or len(self._data[pdate.strftime("%Y-%m")][pdate.strftime("%d")]) == 0:
            return None
        last = base64.b64decode(
            self._data[pdate.strftime("%Y-%m")][pdate.strftime("%d")][-1].split()[1].encode("utf-8")).decode("utf-8")
        if last == "End":
            month = self._data[pdate.strftime("%Y-%m")]
            del month[pdate.strftime("%d")][-1]
            self._data[pdate.strftime("%Y-%m")] = month
            if len(self._data[pdate.strftime("%Y-%m")][pdate.strftime("%d")]) == 0:
                return None
            last = base64.b64decode(
                self._data[pdate.strftime("%Y-%m")][pdate.strftime("%d")][-1].split()[1].encode("utf-8")).decode("utf-8")
        return last

    def report(self, pdate=None):
        if pdate is None:
            pdate = date.today()
        return Report(self._data, pdate)


class Report:
    def __init__(self, data, pdate):
        self._data = data
        self._date = pdate
        self._sum_len = 0
        self._prev = None
        self._next = None
        self._update_prev_next()

    def report(self):
        tmp = []
        if self._date.strftime("%Y-%m") in self._data \
                and self._date.strftime("%d") in self._data[self._date.strftime("%Y-%m")]:
            for e in self._data[self._date.strftime("%Y-%m")][self._date.strftime("%d")]:
                tstr, b64str = e.split()
                task = base64.b64decode(b64str.encode("utf-8")).decode("utf-8")
                start_time = datetime.combine(self._date, datetime.strptime(tstr, "%H:%M").time())
                tmp.append((task, start_time))
        if self._date == date.today():
            tmp.append(("End", datetime.now()))

        ret = []
        tasks_sums = {}
        total_sum = timedelta()
        for i, t in enumerate(tmp):
            task, start_time = t
            if i < len(tmp) - 1:
                end_time = tmp[i+1][1]
                duration = end_time - start_time
                if task != "Pause":
                    task_sum = tasks_sums.setdefault(task, timedelta())
                    task_sum += duration
                    tasks_sums[task] = task_sum
                    total_sum += duration
                dhours, rem = divmod(duration.seconds, 3600)
                dmins, _ = divmod(rem, 60)
                ret.append([task, start_time.strftime("%H:%M"), f"{dhours:02d}:{dmins:02d}"])
            else:
                ret.append([task, start_time.strftime("%H:%M"), ""])

        ret.append(["", "", ""])
        ret.append(["", "Sums", ""])
        for k, v in tasks_sums.items():
            dhours, rem = divmod(v.seconds, 3600)
            dmins, _ = divmod(rem, 60)
            ret.append([k, "", f"{dhours:02d}:{dmins:02d}"])
        dhours, rem = divmod(total_sum.seconds, 3600)
        dmins, _ = divmod(rem, 60)
        ret.append(["Total sum", "", f"{dhours:02d}:{dmins:02d}"])
        self._sum_len = 3 + len(tasks_sums)
        if self._date == date.today():
            self._sum_len += 1
        return ret, len(ret) - (4 + len(tasks_sums))

    def save(self, report):
        report = report[:-self._sum_len]
        if not report:
            return
        save_list = []
        for tstr, ttime, _ in report:
            b64str = base64.b64encode(tstr.encode("utf-8")).decode("utf-8")
            save_string = f"{ttime} {b64str}"
            save_list.append(save_string)
        # month dance necessary to trigger Data.__setitem__
        month = self._data[self._date.strftime("%Y-%m")]
        if month[self._date.strftime("%d")] == save_list:  # no changes
            return
        month[self._date.strftime("%d")] = save_list
        self._data[self._date.strftime("%Y-%m")] = month

    def _update_prev_next(self):
        self._prev = None
        self._next = None
        for i in range(1, 32):
            new_date = self._date - timedelta(days=i)
            if new_date.strftime("%Y-%m") not in self._data:
                break
            if new_date.strftime("%d") in self._data[new_date.strftime("%Y-%m")]:
                self._prev = new_date
                break
        for i in range(1, 32):
            new_date = self._date + timedelta(days=i)
            if new_date > date.today():
                break
            if new_date.strftime("%Y-%m") not in self._data:
                break
            if new_date.strftime("%d") in self._data[new_date.strftime("%Y-%m")]:
                self._next = new_date
                break

    def prev_next_avail(self):
        return self._prev is not None, self._next is not None

    def previous(self):
        self._date = self._prev
        self._update_prev_next()

    def next(self):
        self._date = self._next
        self._update_prev_next()

    def date(self):
        return self._date.strftime("%Y-%m-%d")
