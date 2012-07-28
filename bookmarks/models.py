import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Displayable, Ownable, RichText


class Page(models.Model):
    
    url = models.URLField(unique=True)
    
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    create_date = models.DateTimeField(_("create time"), default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        ordering = ["-create_date", ]


class Bookmark(Displayable, Ownable, RichText):
    
    page = models.ForeignKey(Page, verbose_name=_("page"))

    @models.permalink
    def get_absolute_url(self):
        url_name = "bookmark"
        kwargs = {'pk': self.pk}
        return (url_name, (), kwargs)
    
    def __unicode__(self):
        return self.title
