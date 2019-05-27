#coding:utf-8

from django.test import SimpleTestCase


from tmc.forms import SearchForm



class SearchFormTest(SimpleTestCase):

    def test_form_group_field_label(self):
        form = SearchForm()
        self.assertTrue(form.fields['group'].label == "xxx")


