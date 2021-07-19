from django.forms import FileInput


class InvisibleFileInput(FileInput):
    template_name = 'add_file/widgets/invisible_file_input.html'
