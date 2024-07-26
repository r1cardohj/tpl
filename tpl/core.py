# Author: r1cardohj
# Data: 2024/07/25
# tpl is simple template for xlsx, xls, word, txt, even markdown file.
# you can use it anywhere.
import re

# to match like "{{ person.name }}" {{ persons }} in the cell
SYMBOL = r'{{ (\S+) }}'


def get_symbol(text):
    res = re.match(SYMBOL, text)
    if res is None:
        return None
    return res.group(1)


def iterable(obj):
    try:
        iter(obj)
    except TypeError as e:
        return False
    return True


class Tpl:
    def __init__(self, synx: str, ctx):
        self.synx = synx
        self.ctx = ctx

    def set_synx(self, synx):
        self.synx = synx

    def _get_obj_and_props(self):
        obj_name, *props = self.synx.split('.')
        obj = self.ctx[obj_name]
        return obj, props

    def _render_single(self):
        obj, props = self._get_obj_and_props()
        for prop in props:
            obj = getattr(obj, prop)
        return obj

    def _render_iter(self):
        objs, props = self._get_obj_and_props()
        # some obj like namedtuple is iter obj,
        # but we just want to get property.
        # so try to get property first.
        try:
            value = None
            for prop in props:
                value = getattr(objs, prop)
            return value
        except AttributeError:
            pass
        # then enumerate it like common iterable obj
        res = []
        for obj in objs:
            value = None
            for prop in props:
                value = getattr(obj, prop)
            res.append(value)
        return res

    def _is_obj_in_synx_iterable(self):
        obj, props = self._get_obj_and_props()
        # str is iterable type but in the common case you will
        # never want to enumerate it.
        if isinstance(obj, str):
            return False
        if iterable(obj):
            return True
        return False

    def render(self):
        res = None
        if self._is_obj_in_synx_iterable():
            res = self._render_iter()
        else:
            res = self._render_single()
        return res


def render_template_string(text: str, **ctx):
    while match := re.search(SYMBOL, text):
        r = Tpl(match.group(1), ctx=ctx)
        text = text[:match.start()] + r.render() + text[match.end():]
    return text

