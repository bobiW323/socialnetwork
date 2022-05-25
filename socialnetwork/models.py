from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    picture = models.FileField(default='xzkb.jpg')
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    # age = models.CharField(max_length=3, blank=True)
    bio = models.CharField(max_length=430, blank=True)
    created_by = models.OneToOneField(User, related_name="entry_creators", on_delete=models.CASCADE)
    # creation_time = models.DateTimeField()
    # update_time = models.DateTimeField(blank=True)
    followers = models.ManyToManyField(User, blank=True)
    content_type = models.CharField(max_length=50)

    def __str__(self):
        return 'id=' + str(self.id) + 'last_name' + str(self.last_name)


class Comments(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    comment = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now=True)
    postid = models.CharField(max_length=10000)

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'comment' + str(self.comment)


class Post(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    text = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now=True)

    # entry = models.ForeignKey(Profile, blank=True, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comments, blank=True, related_name="comments", null=True)

    def __str__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.text)
