from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Blog posts
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='post-create'),
    path('blog/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='post-update'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='post-delete'),
    path('my-posts/', views.UserBlogListView.as_view(), name='my-posts'),

    # Bloggers
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),

    # Comments
    path('blog/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment-create'),

    # User Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),

    # Search
    path('search/', views.SearchResultsView.as_view(), name='search'),

    # Post interactions
    path('blog/<int:pk>/like/', views.like_post, name='like-post'),
    path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page='/profile/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]