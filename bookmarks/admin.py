from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

bookmark_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
bookmark_fieldsets[0][1]["fields"].insert(1, "page")
bookmark_fieldsets[0][1]["fields"].extend(["content",])

from bookmarks.models import Page, Bookmark


class BookmarkAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for bookmarks.
    """
    fieldsets = bookmark_fieldsets

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Page)
