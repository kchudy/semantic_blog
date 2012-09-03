from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea
from semantic_blog.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        widgets = {
            'title': TextInput(),
            'content': Textarea(),
        }

        exclude = ('enhancements')