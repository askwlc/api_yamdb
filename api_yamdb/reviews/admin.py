from django.contrib import admin

from .models import Comment, Review, User, Genre, Category, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name', 'year', 'description')
    search_fields = ('name',)
    list_filter = ('category', 'year')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'author', 'title')
    search_fields = ('title', 'author')
    list_filter = ('score', 'text',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Comment, CommentAdmin)

