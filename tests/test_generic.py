# -*- coding: utf-8 -*-
from unittest.mock import Mock

import pytest

from importpath_field.db.descriptors import ProxyFieldDescriptor
from importpath_field.utils import get_path
from importpath_field.choices import ImportPathChoices
from tests.example_classes import example_function, ExampleClassStrategy, DescriptionClassStrategy, \
    example_function_description
from tests.models import ExampleModel


@pytest.mark.parametrize('obj,expected_path', [
    [ExampleClassStrategy, 'tests.example_classes.ExampleClassStrategy'],
    [ExampleClassStrategy.class_method, 'tests.example_classes.ExampleClassStrategy.class_method'],
    [example_function, 'tests.example_classes.example_function'],
])
def test_get_path(obj, expected_path):
    assert get_path(obj) == expected_path


@pytest.mark.parametrize('expected_resolve,expected_path', [
    [ExampleClassStrategy, 'tests.example_classes.ExampleClassStrategy'],
    [ExampleClassStrategy.class_method, 'tests.example_classes.ExampleClassStrategy.class_method'],
    [example_function, 'tests.example_classes.example_function'],

])
def test_proxy_class(expected_resolve, expected_path):
    field = Mock()
    field.name = 'example'

    class Example:
        example = ProxyFieldDescriptor(field)

    i = Example()
    assert i.example == None

    i.example = expected_resolve
    assert i.example.resolve == expected_resolve
    assert i.example.path == expected_path

    i = Example()
    assert i.example == None
    i.example = expected_path
    assert i.example.resolve == expected_resolve
    assert i.example.path == expected_path


def test_choices():
    choices = ImportPathChoices(
        ExampleClassStrategy,
        ExampleClassStrategy.class_method,
        example_function,
        DescriptionClassStrategy,
        [DescriptionClassStrategy.class_method, "Custom description"],
        DescriptionClassStrategy.class_method_description,
        example_function_description
    )
    assert choices == [
        ['tests.example_classes.ExampleClassStrategy', 'ExampleClassStrategy'],
        ['tests.example_classes.ExampleClassStrategy.class_method',
         'ExampleClassStrategy.class_method'],
        ['tests.example_classes.example_function', 'example_function'],
        ['tests.example_classes.DescriptionClassStrategy', 'Strategy description'],
        ['tests.example_classes.DescriptionClassStrategy.class_method',
         'Custom description'],
        ['tests.example_classes.DescriptionClassStrategy.class_method_description',
         'Class method description'],
        ['tests.example_classes.example_function_description', 'Function description']
    ]


def test_choices_register():
    choices = ImportPathChoices()

    obj_list = [
        ExampleClassStrategy,
        ExampleClassStrategy.class_method,
        example_function,
        DescriptionClassStrategy,
        [DescriptionClassStrategy.class_method, "Custom description"],
        DescriptionClassStrategy.class_method_description,
        example_function_description
    ]

    for o in obj_list:
        description = None
        if isinstance(o, list):
            o, description = o
        assert choices.register(description)(o) == o

    assert choices == [
        ['tests.example_classes.ExampleClassStrategy', 'ExampleClassStrategy'],
        ['tests.example_classes.ExampleClassStrategy.class_method',
         'ExampleClassStrategy.class_method'],
        ['tests.example_classes.example_function', 'example_function'],
        ['tests.example_classes.DescriptionClassStrategy', 'Strategy description'],
        ['tests.example_classes.DescriptionClassStrategy.class_method',
         'Custom description'],
        ['tests.example_classes.DescriptionClassStrategy.class_method_description',
         'Class method description'],
        ['tests.example_classes.example_function_description', 'Function description']
    ]


def test_model():
    ExampleModel()
