from django.forms import FileInput, CheckboxInput


class CustomFileInput(FileInput):

    template_name = 'add_file/widgets/custom_file_input.html'

class PersistentCheckbox(CheckboxInput):

    template_name = 'add_file/widgets/persistent_checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs'].update({'id': id(self)})
        return context
