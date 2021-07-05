from django.forms import FileInput, CheckboxInput


class SimpleFileInput(FileInput):

    template_name = 'add_file/widgets/simple_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs'].update({'id': id(self)})
        text = context['widget']['attrs'].pop('text', '')
        context['widget'].update({'text': text, 'form': self.form})
        return context

class PersistentCheckbox(CheckboxInput):

    template_name = 'add_file/widgets/persistent_checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs'].update({'id': name + str(id(self))})
        return context
