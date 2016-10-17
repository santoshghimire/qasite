"""Module for question entry."""
import json
# from django.db.models import Q
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView
from braces.views import SuperuserRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Article, Option
from .forms import QuestionForm


class QuestionCreateView(SuperuserRequiredMixin, View):
    """View to handle form rendering and update for question additon."""

    model = Question
    form_class = QuestionForm
    template_name = 'question_entry_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(
            request, self.template_name, context)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        print('get_form_kwargs called')
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self):
        context = {}
        context['form'] = QuestionForm()
        return context

    def post(self, request, *args, **kwargs):
        save_question(request, **kwargs)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """For Success on question addition."""
        url = reverse(
            "qa:question-create"
        ) + "?success=true"
        return url


class QuestionUpdateView(SuperuserRequiredMixin, View):
    """View to handle question update."""

    model = Question
    form_class = QuestionForm
    template_name = 'question_entry_form.html'

    def get_context_data(self, **kwargs):
        """Pass question id on template."""
        context = {}
        context['question_id'] = self.kwargs['id']
        self.object = self.get_object()
        context['options'] = self.object.option_set.all()
        context['form'] = QuestionForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            'qa:question-update',
            kwargs={'id': self.kwargs.get('id')}
        ) + "?success=true"

    def get_object(self, queryset=None):
        """Return question object."""
        obj = Question.objects.get(id=self.kwargs['id'])
        return obj

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(QuestionUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(
            request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        save_question(request, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


def save_question(request, **kwargs):
    if kwargs.get('id'):
        # update
        question = Question.objects.get(id=int(kwargs.get('id')))
        if request.POST.get('verified') == '0':
            question.is_verified = False
        else:
            question.is_verified = True

        question.updated_by = request.user
        if request.POST.get('verified') == '1':
            question.verified_by = request.user
        question_created = False
    else:
        # create
        question = Question()
        question.created_by = request.user
        question_created = True

    question.text = request.POST.get('text')
    question.image = request.FILES.get('image')
    question.audio = request.FILES.get('audio')
    question.video = request.FILES.get('video')
    question.difficulty = request.POST.get('difficulty')

    question.article = Article.objects.get(
        slug=request.POST.get('article')
    )
    question.category = question.article.category

    question.question_type = request.POST.get('question_type', 'objective')
    if question.question_type == 'objective':
        question.correct = request.POST.get('correct')
    else:
        question.correct = None

    question.save()

    # save options
    option_fields = dict(request.POST)
    for key, value in option_fields.items():
        if key.startswith('option-name'):
            opt_number = key.split('option-name-')[-1]
            opt_text = 'option-text-' + opt_number
            if not question_created:
                try:
                    option = question.option_set.all().get(name=str(opt_number))
                    option.name = request.POST.get(key)
                    option.text = request.POST.get(opt_text)
                    option.save()
                except:
                    print('Exception in saving opt')
            else:
                Option.objects.create(
                    name=request.POST.get(key),
                    text=request.POST.get(opt_text),
                    question=question
                )
    return True


class QuestionDeleteView(View):
    """View to handle question delete."""

    model = Question

    def post(self, request, id):
        """Handle post request."""
        try:
            quest = Question.objects.get(id=id)
            quest.delete()
            return HttpResponse(
                json.dumps({
                    'status': 'ok',
                    'message': 'Question successfully deleted.'
                })
            )
        except:
            return HttpResponse(
                json.dumps({
                    'status': 'error',
                    'message': 'Cannot delete the question.'
                })
            )


class QuestionListView(SuperuserRequiredMixin, ListView):
    """Render dashboard for question management."""

    template_name = 'listquestions.html'
    url_name = 'qlist'

    def get(self, request, *args, **kwargs):
        """Get Values from database."""
        context = {}

        search_text = self.request.GET.get('q', '')
        if search_text:
            queryset = Question.objects.filter(
                text__icontains=search_text
            ).order_by('article')
        else:
            queryset = Question.objects.all().order_by('article')

        page_limit = 30
        paginator = Paginator(queryset, page_limit)  # Show 30 applications per page
        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
            page = int(page) if page else page
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
            queryset = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.num_pages
            queryset = paginator.page(page)

        context['start'] = (page - 1) * page_limit + 1
        end = page * page_limit
        end = paginator.count if end > paginator.count else end
        context['end'] = end
        context['total'] = paginator.count
        context['object_list'] = queryset
        return render(
            request,
            self.template_name,
            context
        )
