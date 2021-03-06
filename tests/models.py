from django.db import models

from importpath_field import ImportPathField, ImportPathChoices



IMPORT_CHOICES = ImportPathChoices()


class ExampleModel(models.Model):
    example_class = ImportPathField()
    example_class_choices = ImportPathField(choices=IMPORT_CHOICES)

    example_class_null = ImportPathField(null=True, blank=True)
