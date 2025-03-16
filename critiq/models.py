from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    release_year = models.PositiveIntegerField()
    director = models.CharField(max_length=255)
    synopsis = models.TextField()
    poster = models.ImageField(upload_to="movie_posters/", blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Average rating will be calculated from related reviews

    class Meta:
        ordering = ["-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a slug from the title and release year
            base_slug = slugify(f"{self.title}-{self.release_year}")
            # Check if the slug exists
            if Movie.objects.filter(slug=base_slug).exists():
                # If it exists, append a UUID to make it unique
                base_slug = f"{base_slug}-{str(uuid.uuid4())[:6]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("critiq:movie_detail", kwargs={"slug": self.slug})

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return None


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        # Ensure a user can only review a movie once
        unique_together = ["movie", "user"]

    def __str__(self):
        return f"Review of {self.movie.title} by {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a slug from the title and movie title
            base_slug = slugify(f"{self.title}-{self.movie.title}")
            # Check if the slug exists
            if Review.objects.filter(slug=base_slug).exists():
                # If it exists, append a UUID to make it unique
                base_slug = f"{base_slug}-{str(uuid.uuid4())[:6]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("critiq:review_detail", kwargs={"slug": self.slug})
