__all__ = ['OrderNumber']

import re
import os
import time
from .clear_module import Clear
from .utils.log_module import Logs
from .number_module import NumberChinese as nTc


_logger = Logs()


class OrderNumber:
    def __init__(self) -> None:
        self.__ntc = nTc()
        self.__last_index = 1
        self.__clear = Clear()
        self.__index_chain = [0] * 100
        self.__origin_reg = re.compile('#+\s([一-十]+\.|[\d\.]+\d+)\s')
        self.__contents_reg = re.compile('#+\s?')
        self.__mark_reg = re.compile('')

    def __sub_index(self, index):
        return '.'.join(str(self.__index_chain[i]) for i in range(2, index + 1))

    def __reset_chain_index(self, index):
        if self.__last_index > index:
            for i in range(index + 1, self.__last_index + 1):
                self.__index_chain[i] = 0
        elif index - self.__last_index > 1:
            index = self.__last_index + 1
        self.__last_index = index
        self.__index_chain[index] += 1
        return index

    def __generate_index(self, index: int) -> str:
        if index == 1:
            return ''
        index = self.__reset_chain_index(index)
        index_tag = f'{self.__ntc.get_number_chinese(self.__index_chain[2])}.' if index == 2 else self.__sub_index(
            index)
        return '#' * index + ' ' + index_tag + ' '

    @staticmethod
    def __get_index(line: str) -> int:
        index = 0
        for c in line:
            if c == '#':
                index += 1
            else:
                break
        return index

    def __replace_index(self, index_tag: str, line: str) -> str:
        return (self.__origin_reg if self.__origin_reg.match(line) else self.__contents_reg).sub(index_tag, line,
                                                                                                 count=0)

    def __add_index_to_contents(self, line: str) -> str:
        index = self.__get_index(line)
        if not index:
            return line
        tag = self.__generate_index(index)
        return tag

    def __add_order_number(self, line: str) -> str:
        # 清洗内容
        line = self.__clear.main(line)
        if line:
            # 代码区直接返回内容
            return (line if self.__clear.code_zone else (
                self.__replace_index(tag, line) if (tag := self.__add_index_to_contents(line)) else line)) + '\n'

    @staticmethod
    def __new_file_path(filepath: str) -> str:
        tmp = os.path.splitext(filepath)
        return tmp[0] + str(int(time.time())) + tmp[1]

    @_logger.decorator('markdown, 执行错误')
    def main(self, filepath: str, inplace=False) -> bool:
        if not os.path.exists(filepath):
            print('invalid filepath')
            return False
        new_contents = []
        with open(filepath, mode='r+', encoding='utf-8') as f:
            for line in f.readlines():
                if new_line := self.__add_order_number(line):
                    new_contents.append(new_line)
                elif self.__clear.need_insert_blank:
                    new_contents.append('\n')
            if inplace:
                f.seek(0)
                f.truncate()
                f.write(''.join(new_contents))
            elif new_contents:
                new_file = self.__new_file_path(filepath)
                with open(new_file, encoding='utf-8', mode='w') as f2:
                    f2.write(''.join(new_contents))
        print('finish')
        return True
