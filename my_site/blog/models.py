from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
#Post Model
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    #PUBLISH DATE
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #COMMENTS TO POST
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)
    
    #GET_ABSOLUTE_URL
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={ 'pk':self.pk })

    def __str__(self):
        return self.title

#Comment Model
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.CharField(max_length=256)
    create_date = models.DateTimeField(default=timezone.now())
    approved_comments = models.BooleanField(default=False)

    #APPROVE COMMENTS
    def approve(self):
        self.approved_comments = True
        self.save()

    #GET_ABSOLUTE_URL
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text