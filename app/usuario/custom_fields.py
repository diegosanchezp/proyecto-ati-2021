from wtforms import  Field
from wtforms.widgets import TextInput

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