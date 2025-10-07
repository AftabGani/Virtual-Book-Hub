from django.db import models
from django.contrib.auth.models import User

class BookRequest(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    reason = models.TextField()
    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author} requested by {self.requested_by.username if self.requested_by else 'Unknown'}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    GENRE_CHOICES = [
               ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Mystery', 'Mystery'),
        ('Fantasy', 'Fantasy'),
        ('Science Fiction', 'Science Fiction'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('Horror', 'Horror'),
        ('Historical', 'Historical'),
        ('Biography', 'Biography'),
        ('Memoir', 'Memoir'),
        ('Self-Help', 'Self-Help'),
        ('Poetry', 'Poetry'),
        ('Adventure', 'Adventure'),
        ('Drama', 'Drama'),
        ('Crime', 'Crime'),
        ('Young Adult', 'Young Adult'),
        ('Children\'s', 'Children\'s'),
        ('Classics', 'Classics'),
        ('Graphic Novel', 'Graphic Novel'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/')
    file = models.FileField(upload_to='books/')
    # uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Fiction')

    def __str__(self):
        return self.title


