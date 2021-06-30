from django.forms import FileInput

class SimpleFileInput(FileInput):

    template_name = 'add_file/widgets/file_input.html'

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', {})
        super().__init__(*args, **kwargs)
        self.text = attrs.get('text', '')

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({'text': self.text, 'id': attrs['id']})
        return context
