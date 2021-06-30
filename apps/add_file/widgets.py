from django.forms import FileInput
from django.utils.html import format_html


class SimpleFileInput(FileInput):
    template_name = 'add_file/widgets/file_input.html'
    def __init__(self, attrs = None):
        super().__init__(attrs)
        self.text = attrs['text']
        self.id = attrs['id']
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({'text': self.text, 'id': self.id})
        return context
