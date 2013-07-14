from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("",
    url(r"^$", "bookmarks.views.bookmarks", name="all_bookmarks"),
    url(r"^(?P<pk>\d+)/$", "bookmarks.views.bookmark", name="bookmark"),
    url(r"^add/$", "bookmarks.views.add", name="add_bookmark"),
    url(r"^extract/$", "bookmarks.views.extract", name="extract_content"),
    url(r"^suggest/$", "bookmarks.views.suggest", name="suggest_content"),
    url(r"^tags/(?P<slug>[-\w]+)/$", "bookmarks.views.bookmarks", name="tagged_bookmarks"),
    url(r"^user/(?P<username>[-\w]+)/$", "bookmarks.views.bookmarks", name="user_bookmarks"),
    url(r"^user/(?P<username>[-\w]+)/tags/(?P<slug>[-\w]+)$", "bookmarks.views.bookmarks", name="user_tagged_bookmarks"),
)
