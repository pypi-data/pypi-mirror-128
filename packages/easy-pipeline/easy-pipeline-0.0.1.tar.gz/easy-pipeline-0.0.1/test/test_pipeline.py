from unittest import TestCase
from pipeline.pipeline import pipeline, inspect

class Plain:
    pass

def add_age(item):
    item.age = 22
    return item

def add_name(name):
    def fun(item):
        item.name = name
        return item
    return fun

class AddHeight:

    def __init__(self, height):
        self.height = height

    def __call__(self, item):
        item.height = 192
        return item


class TestPipeline(TestCase):

    def test_decorator(self):
        item = pipeline(Plain(), [
            add_age,
            # inspect,
            add_name('Tom'),
            #inspect(print),
            AddHeight(192),
            #inspect
        ])
        self.assertEqual('Tom', item.name)
        self.assertEqual(22, item.age)
        self.assertEqual(192, item.height)