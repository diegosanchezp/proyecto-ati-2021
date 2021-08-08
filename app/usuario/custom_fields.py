from flask import url_for
from wtforms import fields, Field

from wtforms.widgets import TextInput, FileInput
import os
class StringListField(Field):
    widget = TextInput()
    
    def _value(self):
        if self.data:
            return ', '.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].split(', ')

class ImageField(fields.FileField):
    def pre_validate(self, form):
        pass
    def process_data(self, value):
        pass

