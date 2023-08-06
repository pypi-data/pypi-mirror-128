from ..filehandler import FileHandler
from portalocker import Lock
from ..util import DEFAULT_TIMEOUT, DEFAULT_CHECK_INTERVAL, DEFAULT_FAIL_WHEN_LOCKED, LOCK_METHOD
from gc import collect
from copy import deepcopy


class OpenReader(FileHandler):
    def __init__(self, file_path, mode='a', timeout=DEFAULT_TIMEOUT, check_interval=DEFAULT_CHECK_INTERVAL,
                 fail_when_locked=DEFAULT_FAIL_WHEN_LOCKED, flags=LOCK_METHOD, **file_open_kwargs):
        super().__init__(file_path=file_path, mode=mode, timeout=timeout, check_interval=check_interval,
                         fail_when_locked=fail_when_locked, flags=flags, **file_open_kwargs)

    def parse(self):
        if self.streams:
            for handler, buffer in self.streams:
                self.__parse(handler=handler, buffer=buffer)
        else:
            return Lock(filename=self.file_path, mode=self.mode, timeout=self.timeout,
                        check_interval=self.check_interval, fail_when_locked=self.fail_when_locked, flags=self.flags,
                        **self.kwargs)

    def __parse(self, handler, buffer):
        data = list()
        row_num = 0
        header = None

        try:
            with Lock(filename=self.file_path, mode=self.mode, timeout=self.timeout, check_interval=self.check_interval,
                      fail_when_locked=self.fail_when_locked, flags=self.flags) as lines:
                for line in lines:
                    data.append(line)

                    if buffer <= len(data):
                        handler(deepcopy(self.file_path), deepcopy(data), deepcopy(row_num - len(data) + 1),
                                deepcopy(row_num), **self.kwargs)
                        data.clear()

                    row_num += 1

            if data:
                row_num -= 1
                handler(deepcopy(self.file_path), deepcopy(data), deepcopy(row_num - len(data) + 1),
                        deepcopy(row_num), **self.kwargs)
            else:
                return data
        finally:
            collect()
