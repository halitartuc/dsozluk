from django.db import models
from django.contrib.auth.models import User

class Title(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Title_Redirect(models.Model):
    name = models.CharField(max_length=150)
    real_name = models.ForeignKey(Title)

    def __str__(self):
        return u"{} ---> {}".format(self.name, self.real_name)


class Entry(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)
    entry = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    last_edited = models.DateTimeField(auto_now=True, blank=True, null=True)

    upVotes = models.ManyToManyField(User, blank=True, null=True, related_name='upVotes')
    downVotes = models.ManyToManyField(User, blank=True, null=True, related_name='downVotes')

    def count_up_votes(self):
        try:
            if self.upVotes:
                return self.upVotes.count()
        except:
            return "0"

    def count_down_votes(self):
        try:
            if self.downVotes:
                return self.downVotes.count()
        except:
            return "0"

    def __str__(self):
        return u"#{}".format(self.id)

