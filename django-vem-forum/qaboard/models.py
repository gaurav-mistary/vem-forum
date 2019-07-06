from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

class Topic(models.Model):
	name = models.CharField(max_length=150, unique=True)
	details = models.TextField(max_length=2000)

	def __str__(self):
		return self.name

	def last_updated_info(self):
		return Answer.objects.filter(a_question__topic=self).order_by('-created_at').first()

class Question(models.Model):
	question = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, related_name="quest", on_delete=models.CASCADE)
	writer = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
	last_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		truncated_quest = Truncator(self.question)
		return truncated_quest.chars(30)

	def get_last_ten_ans(self):
		return self.ans.order_by('-created_at')[:3]

class Answer(models.Model):
	a_question = models.ForeignKey(Question, related_name="ans", on_delete=models.CASCADE, null=True)
	a_writer = models.ForeignKey(User, related_name="ans", on_delete=models.CASCADE)
	answer = models.TextField(max_length=10000, null=False, blank=False)
	likes = models.ManyToManyField(User, blank=True, related_name="likes")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.	DateTimeField(null=True)

	def __str__(self):
		truncated_ans = Truncator(self.answer)
		return truncated_ans.chars(30)

	def get_ans_as_markdown(self):
		return mark_safe(markdown(self.answer, safe_mode='escape'))


class Upvote(models.Model):
	if_upvote = models.BooleanField(default=False)
	if_downvote = models.BooleanField(default=False)
	user = models.ForeignKey(User, related_name="vote", on_delete=models.CASCADE)
	quest_key = models.ForeignKey(Question, related_name="vote", on_delete=models.CASCADE)