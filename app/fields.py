from django import forms

class ListTextWidget(forms.Select):
    template_name = 'recherche/listtxt.html'

    def format_value(self, value):
        # Copied from forms.Input - makes sure value is rendered properly
        if value == '' or value is None:
            return ''
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)


class ChoiceTxtField(forms.ModelChoiceField):
    widget=ListTextWidget()


class MySelectMultiple(forms.SelectMultiple):
    '''Personnalisation des champs option pour le form des mots-clés.'''
    def render_option(self, selected_choices, option_value, option_label):
        # original forms.Select code #
        return f'<option data-id="{option_value}" selected>{option_label}</option>'
