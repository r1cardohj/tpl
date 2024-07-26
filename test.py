import unittest
from collections import namedtuple
from tpl.core import Tpl, render_template_string


class TestCore(unittest.TestCase):

    def test_render(self):
        Person = namedtuple('Person', ['fname', 'lname'])
        r1 = Tpl("user.fname", {'user': Person('John', 'Doe')})
        self.assertEqual(r1.render(), 'John')
        r2 = Tpl('users.fname', {'users': [
            Person('John', 'Doe'),
            Person('Jame', 'Harden'),
            Person('Kobe', 'Bryant')
        ]})
        self.assertEqual(r2.render(), ['John', 'Jame', 'Kobe'])

    def test_render_single(self):
        Person = namedtuple('Person', 'name age')
        r = Tpl("user.name", {'user': Person(name='who', age=12)})
        self.assertEqual(r._render_single(), "who")

    def test_render_single_more_prop(self):
        Person = namedtuple('Person', 'name age child')
        r = Tpl("person.child.name",
                {"person": Person(name="aa", age=32, child=Person(name="bb", age=12, child=None))})
        self.assertEqual(r._render_single(), "bb")

    def test_render_template_string(self):
        Person = namedtuple("Person", 'name age')
        s = "{{ person.name }} is a good boy, he have a dog named {{ dogname }}"
        self.assertEqual(render_template_string(s, person=Person(name="kiki", age=12), dogname="bibi"),
                         "kiki is a good boy, he have a dog named bibi")
