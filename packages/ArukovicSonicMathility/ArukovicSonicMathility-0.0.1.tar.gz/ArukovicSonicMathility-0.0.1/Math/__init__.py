from typing import List, Optional


class Math:
    name = None

    @staticmethod
    def add(add_num_one: int, add_num_two: int) -> int | str:
        """
        Adds an integer to another.
        param: two ints
        return_type: int
        """
        try:
            return add_num_one + add_num_two
        except:
            return "Invalid values."

    @staticmethod
    def smart_subtract(sub1: int, sub2: int) -> int | str:
        """
        Swaps two values if one is greater than another.
        :param sub2:
        :param sub1:
        :return int (can't be a float etc..)
        """
        try:
            if sub2 > sub1:
                sub2, sub1 = sub1, sub2
                return sub1 - sub2
        except:
            return "Invalid values."

    @staticmethod
    def subtract(sub_a: int, sub_b: int) -> int | str:
        """
        Normal subtraction.
        :param sub_b:
        :param sub_a:
        :return int (may differ)
        """
        try:
            return sub_a - sub_b
        except:
            return "Invalid values."

    @staticmethod
    def division(a, b) -> int | float | str | float:
        """
        Division.
        :param b:
        :param a:
        :return may differ/vary
        """
        try:
            return a / b
        except:
            return "Invalid values."

    @staticmethod
    def floor_division(f_div: int, f_div2: int) -> int | str:
        """
        Floor Division.
        :param f_div:
        :param f_div2:
        :return int
        """
        try:
            return f_div // f_div2
        except:
            return "Invalid values"

    @staticmethod
    def mults(num: int, start: int, end: int) -> list[int] | str:
        """
        Multiples of a given num.
        :param end:
        :param start:
        :param num:
        :param ints
        :return: List[int]
        """
        try:
            a: List[int] = []
            for i in range(start, end):
                if i % num == 0:
                    a.append(i)
            return a
        except:
            return "Invalid values."

    @classmethod
    def owner_user(cls, new_name: Optional[str] = "Not mentioned") -> str:
        cls.name = new_name
        return f"Owner: Arukovic. Licensing: MIT licensing, Optional username for user: {cls.name}"

    @staticmethod
    def ranges(s: int, e: int) -> list[int]:
        """
        :param e:
        :param s:
        :return: str | int:
        """
        l = [i for i in range(s, e)]
        return l

    @staticmethod
    def reversed(listv: List[int]) -> List[int]:
        """
        :param listv:
        :return: List[int]
        """
        return listv[::-1]

    @staticmethod
    def first(a: List[int]) -> int:
        """
        :param a:
        :return List[int]
        """
        return a[0]

    @staticmethod
    def last(a) -> List[int]:
        return a[-1]

    @staticmethod
    def sort(lists: List[int]) -> List[int] | str:
        """
        :param lists:
        :return List[int]
        """
        try:
            lists.sort()
            return list(lists)
        except:
            return "Invalid values"
        
    @staticmethod
    def rmdups(arrr: List[int]) -> List[int] | str:
        try:
            return list(set(arrr))
        except:
            return "Invalid values"

    @staticmethod
    def updates() -> str:
        return 'Added new functions. Will update this in new updates.'

    def __repr__(self):
        return "Math()"
