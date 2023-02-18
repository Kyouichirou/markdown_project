__all__ = ['NumberChinese']


class NumberChinese:
    def __init__(self):
        self.__index_chinese = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        self.__number_unit = ('十', '百', '千')

    def __get_bigger_number_zh(self, number: str):
        zero_mode = False
        arr = ['']
        i = len(number) - 1
        tmp = list(reversed(number))
        j = 0
        while True:
            a = int(tmp[j])
            if j == 0:
                if a > 0:
                    arr.append(self.__index_chinese[a])
            else:
                if a > 0:
                    arr.append(self.__index_chinese[a] + self.__number_unit[j - 1])
                else:
                    if not zero_mode:
                        arr.append(self.__index_chinese[a])
            j += 1
            if j > i:
                break
            b = int(tmp[j])
            zero_mode = False
            if b == 0:
                zero_mode = True
                if a > 0:
                    arr.append(self.__index_chinese[0])
            else:
                arr.append(self.__index_chinese[b] + self.__number_unit[j - 1])
            j += 1
            if j > i:
                if j == 2 and b == 1:
                    arr[len(arr) - 1] = self.__number_unit[0]
                break

        return ''.join(reversed(arr))

    def get_number_chinese(self, number: int) -> str:
        tmp = str(number)
        if len(tmp) == 1:
            return self.__index_chinese[number]
        return self.__get_bigger_number_zh(tmp)
