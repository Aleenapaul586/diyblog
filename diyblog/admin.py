from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('logout/', LogoutView.as_view(
                template_name='registration/logged_out.html',
                next_page='/',
                http_method_names=['get', 'post']
            ), name='admin-logout'),
        ]
        return custom_urls + urls

admin.site = CustomAdminSite() 