# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Place, AlternativeName


class AlternativeNameForm(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AlternativeNameFormCreate(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceFormCreate(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlaceFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
