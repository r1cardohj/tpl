# Author: r1cardohj
# Data: 2024/07/25
# xlsx-tpl is simple template for xlsx file.
# it can make generate xlsx much easier.
from openpyxl import load_workbook
import re

# to match like "{{ person.name }}" {{ persons }} in the cell
SYMBOL = r'{{ (\S+) }}'


def is_symbol_valid(text):
    res = re.match(SYMBOL, text)
    if res:
        return True, res.group(1)
    else:
        return False, None


class Render:
    def __init__(self, synx: str, ctx):
        self.synx = synx
        self.ctx = ctx

    def render_single(self):
        """
        if your param a common obj, you can use it like this:
        :::
            class Dog:
                name = "bobo"
                age = 12
            dog = Dog()
        now your template like :
            {{ dog.name }}
        you will get:
            "bobo"
        :return: any
        """
        obj_name, *props = self.synx.split(".")
        obj = self.ctx[obj_name]
        for prop in props:
            obj = getattr(obj, prop)
        return obj

    def render_iter(self):
        """
        if you param a iterable obj, you can use it like this:
        :::
            class Person:
                name = "baby"
                birthday = "2022-11-01"

            persons = [Person(), Person()]
        now your template like:
            {{ persons.name }}
        you will get a list like:
            ["baby", "baby"]
        :return:
        """
        objs_name, *props = self.synx.split(".")
        objs = self.ctx[objs_name]
        res = []
        for obj in objs:
            value = None
            for prop in props:
                value = getattr(obj, prop)
            res.append(value)
        return res

