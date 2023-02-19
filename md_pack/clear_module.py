__all__ = ['Clear']

import os
import re


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
        self.__blank_reg = re.compile('\s{2,}')
        self.__url_pic_reg = re.compile('\!?\[.+\]\(.+\)')
        self.__list_mark = ('* ', '- ', '+ ')
        self.__blank_times = 0
        self.__zero_character = chr(8023)
        self.__need_insert = False
        with open(os.path.dirname(__file__) + '\punctuation_mark.txt', mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                self.__data.append(tuple(line.strip().split(',')))

    def __zh_to_en_convertor(self, line: str) -> str:
        # 将中文符号转为英文符号
        for e in self.__data:
            line = line.replace(e[0], e[1])
        return line

    def __clear_tow_blank(self, line: str) -> str:
        # 剔除多空格（超过1） => 单空格
        return self.__blank_reg.sub(self.__one_blank, line)

    def __check_code(self, strip_line: str) -> bool:
        # 检查是否处于代码区块
        # 如果处于代码区, 就不执行大面积清除空格操作
        # 代码区的内容只执行右侧清除操作 避免清除代码格式
        # 数学公式
        mode = False
        if strip_line[:2] == '$$' or strip_line[:3] == '```':
            self.__code_flag = not self.__code_flag
            mode = True
        else:
            self.__code_flag = False
        # 这里需要注意, 不能缩进, 假如是代码的标记
        return mode or self.__code_flag

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

    def main(self, line: str) -> str:
        self.__need_insert = False
        if strip_line := line.strip():
            self.__blank_times = 0
            return self.__zh_to_en_convertor(self.__clear_zero_character(line.rstrip())) if self.__check_code(
                strip_line) or self.__check_tag_mark(strip_line) else self.__handle_list(line, strip_line)
        else:
            if self.__blank_times == 0:
                self.__blank_times += 1
                self.__need_insert = True
            return ''
