from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, default="Not set")
    age = models.IntegerField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class CourseSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    fee = models.CharField(max_length=20)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.course}"
