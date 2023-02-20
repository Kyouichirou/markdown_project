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
        self.__content_names = {}
        self.__index_chain = [0] * 20
        self.__mark_reg = re.compile('')
        self.__table_contents = ['## 目录']
        self.__contents_reg = re.compile('#+\s?')
        self.__origin_reg = re.compile('#+\s([一-十]+\.|[\d\.]+\d+)\s')

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

    def __generate_index(self, line: str, index: int) -> str:
        if index == 1:
            return line
        index = self.__reset_chain_index(index)
        index_tag = f'{self.__ntc.get_number_chinese(self.__index_chain[2])}.' if index == 2 else self.__sub_index(
            index)
        return self.__add_index('#' * index + ' ' + index_tag + ' ', line, index)

    @staticmethod
    def __get_index(line: str) -> int:
        index = 0
        for c in line:
            if c == '#':
                index += 1
            else:
                break
        return index

    def __get_suffix(self, tag: str):
        # 同名标题
        times = self.__content_names.get(tag, 0)
        if times > 0:
            self.__content_names[tag] = times + 1
            return '-' + times
        else:
            self.__content_names[tag] = 1
            return ''

    def __add_index(self, index_tag: str, line: str, index) -> str:
        line = (self.__origin_reg if self.__origin_reg.match(line) else self.__contents_reg).sub(index_tag, line,
                                                                                                 count=0)
        tag = line[index + 1:]
        blank = ' ' * (index - 1) * 2
        self.__table_contents.append(f'{blank}- [{tag}](#{tag.replace(" ", "-")}{self.__get_suffix(tag)})')
        return line

    def __handle_line(self, line: str, line_number: int) -> str:
        # 清洗内容
        if line := self.__clear.main(line, line_number):
            # 代码区直接返回内容
            if not self.__clear.code_zone:
                if index := self.__get_index(line):
                    line = self.__generate_index(line, index)
            return line + '\n'

    @staticmethod
    def __new_file_path(filepath: str) -> str:
        tmp = os.path.splitext(filepath)
        return tmp[0] + str(int(time.time())) + tmp[1]

    @_logger.decorator('markdown, 执行错误')
    def main(self, filepath: str, inplace=False, contents=False) -> bool:
        if not os.path.exists(filepath):
            print('invalid filepath')
            return False
        new_contents = []
        with open(filepath, mode='r+', encoding='utf-8') as f:
            line_number = 1
            for line in f.readlines():
                if new_line := self.__handle_line(line, line_number):
                    new_contents.append(new_line)
                elif self.__clear.need_insert_blank:
                    new_contents.append('\n')
                line_number += 1
            if new_contents:
                if contents and self.__table_contents:
                    new_contents.insert(1, '\n' + '\n'.join(self.__table_contents) + '\n')
                if inplace:
                    # 需要先将指针移回起始位置
                    f.seek(0)
                    # 假如不移动, 直接f.truncate(0), 内容被清理, 但是出现一些异常的字符
                    f.truncate()
                    f.write(''.join(new_contents))
                else:
                    new_file = self.__new_file_path(filepath)
                    with open(new_file, encoding='utf-8', mode='w') as f2:
                        f2.write(''.join(new_contents))
                self.__clear.check_code_close()
        print('markdown typesetting finish')
        return True
