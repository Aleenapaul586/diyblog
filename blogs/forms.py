from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Blogger, Tag
from django.utils.text import slugify

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create associated blogger profile
            Blogger.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                profile_picture=self.cleaned_data.get('profile_picture', None)
            )
        return user

class BlogPostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags (e.g., technology, programming, python)'}),
    )
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog post content here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # If editing an existing post, show existing tags
            self.initial['tags'] = ', '.join(tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Handle tags
            if 'tags' in self.cleaned_data:
                # Clear existing tags
                post.tags.clear()
                # Split tags by comma and strip whitespace
                tag_names = [t.strip() for t in self.cleaned_data['tags'].split(',') if t.strip()]
                # Create or get tags and add them to the post
                for tag_name in tag_names:
                    try:
                        tag = Tag.objects.get(name=tag_name)
                    except Tag.DoesNotExist:
                        tag = Tag(name=tag_name)
                        tag.save()  # This will handle unique slug generation
                    post.tags.add(tag)
        
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter your comment here...'
            })
        }

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Tell us about yourself"
    )
    profile_picture = forms.ImageField(
        required=False,
        help_text="Upload a profile picture"
    )

    class Meta:
        model = Blogger
        fields = ['bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'] = forms.CharField(
                initial=self.instance.user.username,
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            )

    def save(self, commit=True):
        blogger = super().save(commit=False)
        if commit:
            # Update user information
            user = blogger.user
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            user.save()
            # Save blogger profile
            blogger.save()
        return blogger 