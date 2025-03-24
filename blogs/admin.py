from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Blogger, BlogPost, Comment, Tag

class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False
    verbose_name_plural = 'blogger'

class CustomUserAdmin(UserAdmin):
    inlines = (BloggerInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_blogger_status')

    def get_blogger_status(self, obj):
        try:
            return bool(obj.blogger)
        except Blogger.DoesNotExist:
            return False
    get_blogger_status.short_description = 'Has Blogger Profile'
    get_blogger_status.boolean = True

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('post_date',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date', 'get_comment_count', 'views')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'content', 'author__user__username')
    readonly_fields = ('post_date', 'views')
    inlines = [CommentInline]

    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = 'Comments'

class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_post_count')
    search_fields = ('user__username', 'user__email', 'bio')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_post_count(self, obj):
        return obj.blogpost_set.count()
    get_post_count.short_description = 'Posts'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'author', 'blog_post', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('content', 'author__username', 'blog_post__title')
    readonly_fields = ('post_date',)

    def truncated_content(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    truncated_content.short_description = 'Content'

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def get_post_count(self, obj):
        return obj.blogpost_set.count()
    get_post_count.short_description = 'Posts'

# Unregister the default UserAdmin
admin.site.unregister(User)
# Register our CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

admin.site.register(Blogger, BloggerAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)