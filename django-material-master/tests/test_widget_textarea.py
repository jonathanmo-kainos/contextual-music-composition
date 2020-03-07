import json

from django import forms
from django.test.utils import override_settings
from django_webtest import WebTest
from . import build_test_urls


class TextareaForm(forms.Form):
    test_field = forms.CharField(
        min_length=5,
        max_length=20,
        widget=forms.Textarea(attrs={'data-test': 'Test Attr'}))


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    default_form = TextareaForm

    def test_default_usecase(self):
        page = self.app.get(self.test_default_usecase.url)

        self.assertIn('id="id_test_field_container"', page.body.decode('utf-8'))
        self.assertIn('id="id_test_field"', page.body.decode('utf-8'))
        self.assertIn('maxlength="20"', page.body.decode('utf-8'))
        self.assertIn('data-test="Test Attr"', page.body.decode('utf-8'))

        form = page.form
        self.assertIn('test_field', form.fields)

        form['test_field'] = 'TEST CONTENT'
        response = json.loads(form.submit().body.decode('utf-8'))

        self.assertIn('cleaned_data', response)
        self.assertIn('test_field', response['cleaned_data'])
        self.assertEqual('TEST CONTENT', response['cleaned_data']['test_field'])

    def test_missing_value_error(self):
        form = self.app.get(self.test_missing_value_error.url).form
        response = form.submit()

        self.assertIn('has-error', response.body.decode('utf-8'))
        self.assertIn('This field is required.', response.body.decode('utf-8'))

    def test_render_with_value(self):
        form = self.app.get(self.test_render_with_value.url).form
        form['test_field'] = 'a'*21
        response = form.submit()

        self.assertIn('>{}<'.format('a'*21), response.body.decode('utf-8'))
        self.assertIn('Ensure this value has at most 20 characters', response.body.decode('utf-8'))

    def test_part_group_class(self):
        page = self.app.get(self.test_part_group_class.url)

        self.assertIn('class="yellow required input-field col s12"', page.body.decode('utf-8'))

    test_part_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class override %}yellow required input-field col s12{% endattr %}
        {% endform %}
    '''

    def test_part_add_group_class(self):
        page = self.app.get(self.test_part_add_group_class.url)

        self.assertIn('class="input-field col s12 required deep-purple lighten-5"', page.body.decode('utf-8'))

    test_part_add_group_class.template = '''
        {% form %}
             {% attr form.test_field 'group' class append %}deep-purple lighten-5{% endattr %}
        {% endform %}
    '''

    def test_part_prefix(self):
        response = self.app.get(self.test_part_prefix.url)
        self.assertIn('<i class="mdi-communication-email prefix"></i>', response.body.decode('utf-8'))

    test_part_prefix.template = '''
        {% form %}
             {% part form.test_field prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% endform %}
    '''

    def test_part_add_control_class(self):
        response = self.app.get(self.test_part_add_control_class.url)
        self.assertIn('class="materialize-textarea orange"', response.body.decode('utf-8'))

    test_part_add_control_class.template = '''
        {% form %}
             {% attr form.test_field 'widget' class append %}orange{% endattr %}
        {% endform %}
    '''

    def test_part_label(self):
        response = self.app.get(self.test_part_label.url)
        self.assertIn('<label for="id_test_field">My label</label>', response.body.decode('utf-8'))

    test_part_label.template = '''
        {% form %}
             {% part form.test_field label %}<label for="id_test_field">My label</label>{% endpart %}
        {% endform %}
    '''

    def test_part_add_label_class(self):
        response = self.app.get(self.test_part_add_label_class.url)
        self.assertIn('class="green-text"', response.body.decode('utf-8'))

    test_part_add_label_class.template = '''
        {% form %}
             {% attr form.test_field 'label' class append %}green-text{% endattr %}
        {% endform %}
    '''

    def test_part_help_text(self):
        response = self.app.get(self.test_part_help_text.url)
        self.assertIn('<div class="help-block">My help</div>', response.body.decode('utf-8'))

    test_part_help_text.template = '''
        {% form %}
             {% part form.test_field help_text %}<div class="help-block">My help</div>{% endpart %}
        {% endform %}
    '''

    def test_part_errors(self):
        response = self.app.get(self.test_part_errors.url)
        self.assertIn('<div class="errors"><small class="error">My Error</small></div>', response.body.decode('utf-8'))

    test_part_errors.template = '''
        {% form %}
             {% part form.test_field  errors%}<div class="errors"><small class="error">My Error</small></div>{% endpart %}
        {% endform %}
    '''

urlpatterns = build_test_urls(Test)
