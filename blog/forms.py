from django import forms
from models import BlogEntry
from epiceditor.widgets import AdminEpicEditorWidget


class BlogEntryAdminForm(forms.ModelForm):
    body_markdown = forms.CharField(
        widget=AdminEpicEditorWidget(themes={'editor': 'epic-light.css', 'preview': 'github.css'}))

    class Meta:
        model = BlogEntry
        exclude = ['body']