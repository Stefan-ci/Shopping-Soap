from blog.models import Post, Comment
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin



class PostAdmin(ImportExportModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }
    list_display = ['title', 'is_public', 'date']
    list_filter = ['is_public', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'





class CommentAdmin(ImportExportModelAdmin):
    list_display = ['post', 'name', 'email', 'is_public', 'date']
    list_filter = ['is_public', 'date']
    search_fields = ['name', 'content', 'post__title', 'email', 'website']
    date_hierarchy = 'date'





admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
