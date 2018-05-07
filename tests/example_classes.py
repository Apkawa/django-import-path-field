from .models import IMPORT_CHOICES


@IMPORT_CHOICES.register("Nya")
def example_function():
    return 1


class ExampleClassStrategy:
    attribute = 10

    @classmethod
    def class_method(cls):
        return 1

    @staticmethod
    def static_method():
        return 2

    def method(self):
        return 3


class DescriptionClassStrategy:
    short_description = 'Strategy description'

    @classmethod
    def class_method(cls):
        return 1

    @classmethod
    def class_method_description(cls):
        """Class method description"""
        return 1

    def method(self):
        return 3


def example_function_description():
    return 1


example_function_description.short_description = 'Function description'
