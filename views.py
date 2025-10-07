from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Book, BookRequest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache

from django.contrib.auth import logout
from django.shortcuts import redirect

def homepage(request):
    return render(request, 'books/homepage.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page

# Check if the user is a staff member, superuser, or admin

def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

# User registration view
@never_cache
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.db.models import Q  # Import Q for complex queries

@login_required
@never_cache
def book_list(request):
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('genre', '')
    book_id = request.GET.get('book_id')
    
    # Start with all books
    books = Book.objects.all()
    
    # Filter by query: title or author
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    
    # Filter by genre if selected
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    # Fetch selected book by ID if provided
    selected_book = None
    if book_id:
        selected_book = get_object_or_404(Book, id=book_id)
    
    return render(request, 'books/book_list.html', {
        'books': books,
        'selected_book': selected_book,
        'query': query,
        'genre_filter': genre_filter,
    })


# Book request form
class BookRequestForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    author = forms.CharField(max_length=255, required=True)
    reason = forms.CharField(widget=forms.Textarea, required=True)

# View for handling book requests (requires login)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BookRequest

@login_required
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            # Create the BookRequest with the requested user
            BookRequest.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                reason=form.cleaned_data['reason'],
                requested_by=request.user  # Capture the user who is making the request
            )
            # Send an email notification (optional)
            send_mail(
                'New Book Request',
                f"Title: {form.cleaned_data['title']}\nAuthor: {form.cleaned_data['author']}\nReason: {form.cleaned_data['reason']}\nRequested by: {request.user.username}",
                'admin@virtualbookhub.com',
                ['aftabgani1@gmail.com'],  # Admin's email address
                fail_silently=False,
            )
            return redirect('book_list')
    else:
        form = BookRequestForm()

    return render(request, 'books/request_book.html', {'form': form})


# View for adding new books (requires login and staff/superuser permissions)
@login_required
@never_cache
@user_passes_test(is_staff_or_superuser)
def add_book(request):
    if request.method == 'POST':
        # Process the form submission to add a new book
        pass

    return render(request, 'books/add_book.html')
