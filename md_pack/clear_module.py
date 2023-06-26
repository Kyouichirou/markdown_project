__all__ = ['Clear']

import os
import re
from .base64_module import convert
from .utils.log_module import Logs

_logger = Logs()


class Clear:
    @property
    def code_zone(self) -> bool:
        return self.__code_flag

    @property
    def need_insert_blank(self) -> bool:
        return self.__need_insert

    def __init__(self):
        self.__one_blank = ' '
        self.__data = []
        self.__code_flag = False
        self.__list_flag = False
        self.__blank_reg = re.compile('\w+(?=\))')
        self.__url_pic_reg = re.compile('\!?\[.+\]\(.+\)')
        self.__local_pic_reg = re.compile('[a-z]+:\\\.+(?=\))', re.I)
        self.__sub_pic_reg = re.compile('\[.+\]:data:image\/')
        self.__list_mark = ('* ', '- ', '+ ')
        self.__blank_times = 0
        self.__code_mark = 0
        self.__math_mark = 0
        self.__code_first = 0
        self.__code_last = 0
        self.__math_first = 0
        self.__math_last = 0
        self.__zero_character = chr(8203)
        self.__need_insert = False
        with open(os.path.dirname(__file__) + '\punctuation_mark.txt', mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                self.__data.append(tuple(line.strip().split(',')))

    def __zh_to_en_convertor(self, line: str) -> str:
        # 将中文符号转为英文符号
        for e in self.__data:
            line = line.replace(e[0], e[1] + ' ')
        return line

    def __clear_tow_blank(self, line: str) -> str:
        # 剔除多空格（超过1） => 单空格
        return self.__blank_reg.sub(self.__one_blank, line)

    def check_code_close(self) -> bool:
        # 检查代码区间是否闭合
        is_close = True
        if self.__code_last != self.__code_first:
            is_close = False
            _logger.warning(f'code zone is not closed, first: {self.__code_first}; last: {self.__code_last}')
        if self.__math_first != self.__math_last:
            is_close = False
            _logger.warning(f'math zone is not closed, first: {self.__math_first}; last: {self.__math_last}')
        return is_close

    def __check_code(self, strip_line: str, line_number: int) -> bool:
        # 检查是否处于代码区块
        # 如果处于代码区, 就不执行大面积清除空格操作
        # 代码区的内容只执行右侧清除操作 避免清除代码格式
        # 数学公式
        # 注意typora的编辑器的标签没有闭合也可以正常显示
        # 当标签内包含标签本身, 标签就会自增来表示
        # 不一定是三个```符号
        mode = False
        ic = 0
        ib = 0
        last_e = ''
        for e in strip_line:
            if e == '`' and (not last_e or last_e == '`'):
                ic += 1
                last_e = '`'
            elif e == '$' and (not last_e or last_e == '$'):
                ib += 1
                last_e = '$'
            else:
                break
        if ic > 2:
            if ic >= self.__code_mark:
                mode = True
                self.__code_mark = ic
                self.__code_flag = not self.__code_flag
                if self.__code_flag:
                    self.__code_first += 1
                else:
                    # 假如带有标签, 则大概率是开始的标志
                    if strip_line[ic:]:
                        _logger.warning(f'code zone is not closed, may be in front of this row: {line_number}')
                        self.__code_flag = True
                        self.__code_first += 1
                    else:
                        self.__code_last += 1
        elif ib > 1:
            if ib >= self.__math_mark:
                mode = True
                self.__math_mark = ib
                self.__code_flag = not self.__code_flag
                if self.__code_flag:
                    self.__math_first += 1
                else:
                    self.__math_last += 1
        if not (mode or self.__code_flag):
            self.__code_mark = 0
            self.__math_mark = 0
            return False
        return True

    def __check_tag_mark(self, line: str) -> bool:
        # 检查图片/链接
        return True if self.__url_pic_reg.match(line) else (line.startswith('<') and line.endswith('>'))

    def __handle_list(self, line: str, strip_line: str):
        # 有标记的
        # 无标记的
        mode = any(strip_line.startswith(e) for e in self.__list_mark)
        if mode or self.__list_flag:
            ic = 0
            for e in line:
                if e == ' ':
                    ic += 1
                else:
                    break
            self.__list_flag = mode or (False if ic < 2 else True)
            return self.__zh_to_en_convertor((' ' * (ic if self.__list_flag else 0)) + self.__clear_tow_blank(
                self.__clear_zero_character(strip_line)))
        else:
            self.__list_flag = False
        return self.__zh_to_en_convertor(self.__clear_zero_character(self.__clear_tow_blank(strip_line)))

    def __clear_zero_character(self, line: str) -> str:
        # 清理掉隐藏的字符
        return line.replace(self.__zero_character, '')

    def __check_local_pic(self, line: str) -> str:
        # 检查本地的文件
        if ms := self.__local_pic_reg.findall(line):
            return convert(ms[0])
        return ''

    def __check_base64(self, line: str) -> bool:
        return True if self.__sub_pic_reg.match(line) else False

    def main(self, line: str, line_number: int) -> str:
        self.__need_insert = False
        if strip_line := line.strip():
            self.__blank_times = 0
            if local_pic := self.__check_local_pic(strip_line):
                return local_pic
            elif self.__check_base64(strip_line):
                return strip_line
            return self.__zh_to_en_convertor(self.__clear_zero_character(line.rstrip())) if self.__check_code(
                strip_line, line_number) or self.__check_tag_mark(strip_line) else self.__handle_list(line, strip_line)
        else:
            if self.__blank_times == 0:
                self.__blank_times += 1
                self.__need_insert = True
            return ''
