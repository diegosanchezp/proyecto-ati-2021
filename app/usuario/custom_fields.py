from flask import url_for
from wtforms import  Field
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

class ImageField(Field):
    widget = FileInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = open('app/static/img/' + valuelist[0], "wb")