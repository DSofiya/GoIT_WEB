from django import forms
from .models import Author, Tag, Quote


class AddQuoteForm(forms.Form):
    quote = forms.CharField(label="Quote", widget=forms.Textarea)
    author = forms.CharField(label="Author")
    tags = forms.CharField(label="Tags", help_text="Separate tags with commas")


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["quote", "tags", "author"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
