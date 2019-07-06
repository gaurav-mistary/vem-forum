from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Question, Answer
from django.contrib.auth.models import User
from .forms import QuestionForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home_view(request):
	topic = Topic.objects.all()
	return render(request, 'home.html', {'topics':topic})

def topic_ques(request, pk):
	topic = get_object_or_404(Topic, pk=pk)
	queryset = topic.quest.order_by('-last_updated').annotate(replies=Count('ans'))
	page = request.GET.get('page', 1)

	paginator = Paginator(queryset, 10)

	try:
		ques = paginator.page(page)
	except PageNotAnInteger:
		ques = paginator.page(1)
	except EmptyPage:
		ques = paginator.page(paginator.num_pages)

	return render(request, 'topic_questions.html', {'topic':topic, 'ques':ques})

@login_required
def new_ques(request, pk):
	topic = get_object_or_404(Topic, pk=pk)
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			ques = form.save(commit=False)
			ques.topic = topic
			ques.writer = request.user
			ques.save()

			return redirect('forum-topic_ques', pk=pk)
	else:
		form = QuestionForm()

	return render(request, 'new_question.html', {'topic':topic, 'form':form})

def ques_ans(request, pk, ques_pk):
	ques = get_object_or_404(Question, topic__pk=pk, pk=ques_pk)
	return render(request, 'ques_ans.html', {'ques': ques})

@login_required
def ques_reply(request, pk, ques_pk):
	ques = get_object_or_404(Question, topic__pk=pk, pk=ques_pk)
	if request.method=="POST":
		form = ReplyForm(request.POST)
		if form.is_valid():
			answ = form.save(commit=False)
			answ.a_question = ques
			answ.a_writer = request.user
			answ.save()

			ques.updated_at = timezone.now()
			ques.save()

			return redirect('forum-question_answers', pk=pk, ques_pk=ques_pk)
	else:
		form = ReplyForm()

	return render(request, 'ques_reply.html', {'ques':ques, 'form':form})

@method_decorator(login_required, name='dispatch')
class ReplyUpdateView(UpdateView):
	model = Answer
	fields = ('answer',)
	template_name = 'edit_reply.html'
	pk_url_kwarg = 'ans_pk'
	context_object_name = 'ans'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(a_writer=self.request.user)

	def form_valid(self, form):
		ans = form.save(commit=False)
		ans.updated_by = self.request.user
		ans.updated_at = timezone.now()
		ans.save()
		return redirect('forum-question_answers', pk=ans.a_question.topic.pk, ques_pk=ans.a_question.pk)

