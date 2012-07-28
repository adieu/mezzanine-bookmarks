from django import forms
from django.utils.translation import ugettext_lazy as _

from mezzanine.generic.models import Keyword

from bookmarks.models import Bookmark, Page


class BookmarkForm(forms.ModelForm):
    url = forms.URLField(label="URL", verify_exists=False, widget=forms.TextInput(attrs={"size": 40}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    content = forms.Textarea()
    redirect = forms.BooleanField(label="Redirect", required=False)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BookmarkForm, self).__init__(*args, **kwargs)
        # hack to order fields
        self.fields.keyOrder = ["url", "title", "content", "keywords", "redirect"]

    def clean(self):
        if not self.cleaned_data.get("url", None):
            return self.cleaned_data
        if Bookmark.objects.filter(page__url=self.cleaned_data["url"], user=self.user).count() > 0:
            raise forms.ValidationError(_("You have already bookmarked this link."))
        return self.cleaned_data

    def clean_keywords(self):
        """docstring for clean_keywords"""
        ids = []
        for title in self.cleaned_data['keywords'].split(","):
             title = "".join([c for c in title if c.isalnum() or c in "- "])
             title = title.strip().lower()
             if title:
                 keyword, created = Keyword.objects.get_or_create(title=title)
                 id = str(keyword.id)
                 if id not in ids:
                     ids.append(id)
        return ",".join(ids)

    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False

    def save(self, commit=True):
        try:
            page = Page.objects.get(url=self.cleaned_data['url'])
        except Page.DoesNotExist:
            page = Page.objects.create(url=self.cleaned_data['url'], creator=self.user)

        instance = super(BookmarkForm, self).save(False)
        instance.page = page
        instance.user = self.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Bookmark
        fields = [
            "url",
            "title",
            "content",
            "redirect",
            "keywords",
        ]
