from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *
from bib.models import *


class GenericFilterFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))


class QuoteFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(QuoteFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'text',
                    'book_source',
                    css_id="basic_search_fields"
                ),
            )
        )


class PersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'first_name',
                    'last_name',
                    'person_gnd',
                    css_id="basic_search_fields"
                ),
            )
        )


class WorkFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WorkFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'title',
                    'work_author',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Enstehungszeit',
                    'creation_start_date',
                    'start_date_sure',
                    'creation_end_date',
                    'end_date_sure',
                    css_id="entstehungszeit"
                ),
                AccordionGroup(
                    'Advanced search options',
                    'work_translator',
                    'alt_title',
                    'main_language',
                    css_id="lexicon_search_options"),
                css_id="accordion",
                )
            )
