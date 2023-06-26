from django.contrib import admin

from bookmark.models import Bookmark

# Register your models here.

# 데코레이터 패턴을 사용 하지 않는 방법
# admin.site.register(Bookmark, BookmarkAdmin)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'url')
