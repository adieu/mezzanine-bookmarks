import datetime
import urllib2
import urllib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from mezzanine.utils.views import render, paginate
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword

from bookmarks.forms import BookmarkForm
from bookmarks.models import Bookmark


def bookmarks(request, slug=None):
    if not slug:
        bookmarks = Bookmark.objects.all().order_by("-publish_date")
        keyword = None
    else:
        try:
            keyword = Keyword.objects.get(slug=slug)
        except Keyword.DoesNotExist:
            raise Http404

        bookmarks = Bookmark.objects.filter(keywords__keyword_id=keyword.pk).order_by("-publish_date")
        if len(bookmarks) == 0:
            raise Http404

    bookmarks = paginate(
        bookmarks,
        request.GET.get("page", 1),
        15,
        settings.MAX_PAGING_LINKS,
    )
    return render(request, ["bookmarks/bookmarks.html"], {
        "bookmarks": bookmarks,
        "tag": keyword,
    })


def bookmark(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    return render(request, ["bookmarks/bookmark.html"], {
        "bookmark": bookmark,
    })


@csrf_exempt
@login_required(login_url='/admin/')
def suggest(request):
    content = request.REQUEST.get('content', None)
    if content:
        params = {
            'method': 'zemanta.suggest',
            'api_key': settings.BOOKMARKS_ZEMANTA_API_KEY,
            'text': smart_str(content),
            'format': 'json',
            'return_images': '0',
        }
        result = urllib2.urlopen('http://api.zemanta.com/services/rest/0.0/', urllib.urlencode(params)).read()
    else:
        result = '{}'
    return HttpResponse(result, mimetype="application/json")


@login_required(login_url='/admin/')
def extract(request):
    url = request.GET.get('url', None)
    if url:
        params = {
            'token': settings.BOOKMARKS_DIFFBOT_API_KEY,
            'url': url,
            'html': '1',
            'tags': '1',
        }
        result = urllib2.urlopen('http://www.diffbot.com/api/article?%s' % urllib.urlencode(params)).read()
    else:
        result = '{}'
    return HttpResponse(result, mimetype="application/json")


@login_required(login_url='/admin/')
def add(request):
    if request.method == "POST":
        bookmark_form = BookmarkForm(request.user, request.POST)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save()

            if bookmark_form.should_redirect():
                return HttpResponseRedirect(bookmark.page.url)
            else:
                return HttpResponseRedirect(reverse("all_bookmarks"))
    else:
        initial = {}
        if "url" in request.GET:
            initial["url"] = request.GET["url"]
        if "title" in request.GET:
            initial["title"] = request.GET["title"]
        if "redirect" in request.GET:
            initial["redirect"] = request.GET["redirect"]

        if initial:
            bookmark_form = BookmarkForm(initial=initial)
        else:
            bookmark_form = BookmarkForm()

    bookmarks_add_url = "http://" + Site.objects.get_current().domain + reverse("add_bookmark")
    bookmarklet = "javascript:location.href='%s?url='+encodeURIComponent(location.href)+';title='+encodeURIComponent(document.title)+';redirect=on'" % bookmarks_add_url
    return render(request, ["bookmarks/add.html"], {
        "bookmarklet": bookmarklet,
        "bookmark_form": bookmark_form,
    })
