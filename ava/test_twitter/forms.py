from django.forms import ModelForm

from . import models


class TwitterTestForm(ModelForm):

    class Meta:
        model = models.TwitterTest
        exclude = ['project', 'user', 'test_status', 'test_type', 'redirect_url', 'page_template', 'link']
        labels = {
            'name': 'Test Name',
            'description': 'Test Description',
        }
