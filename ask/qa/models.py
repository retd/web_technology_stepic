from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def new():
        pass

    def popular():
        pass

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name="question_author")
    likes = models.ManyToManyField(
        User, related_name="question_like", blank=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'id': self.id})


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ('added_at',)

    def __unicode__(self):
        return self.author.first_name
