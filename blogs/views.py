from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import BlogPost, Blogger, Comment, Tag
from .forms import BlogPostForm, CommentForm, UserRegistrationForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm

def get_or_create_blogger(user):
    """Helper function to get or create a Blogger profile for a user"""
    try:
        return user.blogger
    except Blogger.DoesNotExist:
        return Blogger.objects.create(user=user)

def index(request):
    """View function for home page of site."""
    # Create blogger profile for admin if it doesn't exist
    if request.user.is_authenticated and request.user.is_staff:
        get_or_create_blogger(request.user)
        
    num_posts = BlogPost.objects.count()
    num_bloggers = Blogger.objects.count()
    
    context = {
        'num_posts': num_posts,
        'num_bloggers': num_bloggers,
    }
    return render(request, 'blogs/index.html', context)

class BlogListView(generic.ListView):
    model = BlogPost
    template_name = 'blogs/blogpost_list.html'
    context_object_name = 'blog_list'
    paginate_by = 5
    ordering = ['-post_date']

class BlogDetailView(generic.DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('post_date')
        context['comment_form'] = CommentForm()
        # Increment view count
        self.object.views += 1
        self.object.save()
        return context

class BlogPostCreateView(LoginRequiredMixin, generic.CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blogpost_form.html'

    def form_valid(self, form):
        # Get or create blogger profile for the user
        blogger = get_or_create_blogger(self.request.user)
        form.instance.author = blogger
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure user has a blogger profile
        get_or_create_blogger(self.request.user)
        return context

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blogpost_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BlogPost
    success_url = reverse_lazy('my-posts')
    template_name = 'blogs/blogpost_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user

class UserBlogListView(LoginRequiredMixin, generic.ListView):
    model = BlogPost
    template_name = 'blogs/user_blogpost_list.html'
    context_object_name = 'blog_list'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(author__user=self.request.user).order_by('-post_date')

class BloggerListView(generic.ListView):
    model = Blogger
    template_name = 'blogs/blogger_list.html'
    context_object_name = 'blogger_list'

class BloggerDetailView(generic.DetailView):
    model = Blogger
    template_name = 'blogs/blogger_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = self.object.blogpost_set.all().order_by('-post_date')
        return context

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blogs/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog_post = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.kwargs['pk']})

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Blogger
    template_name = 'blogs/profile.html'
    context_object_name = 'blogger'

    def get_object(self):
        return get_or_create_blogger(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'blogs/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Get or create blogger profile
        return get_or_create_blogger(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class SearchResultsView(generic.ListView):
    model = BlogPost
    template_name = 'blogs/search_results.html'
    context_object_name = 'blog_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__user__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return BlogPost.objects.none()

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog-detail', pk=pk)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog-detail', pk=comment.blog_post.pk)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})