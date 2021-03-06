"""Module for question entry."""
import json
import xlrd
import xlwt
from urllib import urlencode
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import View
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


class QuestionListView(SuperuserRequiredMixin, View):
    """Render dashboard for question management."""

    template_name = 'listquestions.html'
    url_name = 'qlist'

    def get_context_data(self, request):
        context = {}
        search_text = self.request.GET.get('q', '')
        topics = self.request.GET.getlist('topic', [])
        topics = [int(i) for i in topics]
        filter_dict = {}
        if search_text:
            filter_dict['text__icontains'] = search_text
        if topics:
            filter_dict['article__in'] = topics
        queryset = Question.objects.filter(**filter_dict).order_by('article')
        # queryset = Question.objects.all().order_by('article')

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
        start = (page - 1) * page_limit
        end = page * page_limit
        end = paginator.count if end > paginator.count else end
        context['start'] = start + 1 if end else start
        context['end'] = end
        context['total'] = paginator.count
        context['object_list'] = queryset

        current_path = request.path
        query_params = dict(request.GET)
        filtered_query_params = {key: value[0] for key, value in query_params.items() if key != 'page'}
        params = urlencode(filtered_query_params)
        if params:
            current_path += '?' + params
        current_path = current_path + '?' if current_path.find('?') == -1 else current_path + '&'
        context['current_path'] = current_path
        context['selected_topics'] = topics
        context['articles'] = Article.objects.active().order_by(
            'level__name', 'title')
        return context

    def get(self, request, *args, **kwargs):
        """Get Values from database."""
        context = self.get_context_data(request)
        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('inputFile')
        # article_id = request.POST.get('article')
        book = xlrd.open_workbook(file_contents=excel_file.read())
        error_messages = []
        if book.nsheets:
            first_sheet = book.sheet_by_index(0)
            for row in range(1, first_sheet.nrows):
                row_data = first_sheet.row_values(row)
                article_id = int(float(str(row_data[1])))  # article title
                try:
                    article = Article.objects.get(id=article_id)
                except Article.DoesNotExist:
                    error_msg = 'ERROR : Topic ID {} does not exist.'.format(article_id)
                    if error_msg not in error_messages:
                        error_messages.append(error_msg)
                    continue
                text = row_data[0]  # question text
                correct = str(row_data[2])[0]  # correct answer
                question = Question(
                    text=text, question_type='objective',
                    correct=correct, difficulty=1,
                    category=article.category,
                    article=article
                )
                question.save()
                for i in range(3, len(row_data)):
                    Option.objects.create(
                        name=str(i - 2),
                        text=row_data[i],
                        question=question
                    )
        context = self.get_context_data(request)
        if error_messages:
            context['error_messages'] = error_messages
        else:
            context['import_msg'] = 'Bulk Question Import completed successfully !'
        return render(
            request,
            self.template_name,
            context
        )


class QuestionFormatExport(View):
    """Module to export question import format."""

    def get(self, *args, **kwargs):
        style0 = xlwt.easyxf(
            'font: name FreeSans, bold on')
        # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')
        header = [
            'Question', 'Article ID', 'Correct',
            'Option 1', 'Option 2', 'Option 3', 'Option 4'
        ]
        for count, i in enumerate(header):
            ws.write(0, count, i, style0)
        questions = Question.objects.all().order_by('article__id')
        for row, question in enumerate(questions):
            ws.write(row + 1, 0, question.text)
            ws.write(row + 1, 1, question.article.id)
            ws.write(row + 1, 2, question.correct)
            options = question.option_set.all().order_by('name')
            for opt_count, opt in enumerate(options):
                ws.write(row + 1, opt_count + 3, opt.text)
        ws2 = wb.add_sheet('Sheet2')
        for count, j in enumerate(['Article Name', 'Level', 'Category', 'Article ID']):
            ws2.write(0, count, j, style0)
        articles = Article.objects.all().order_by('level', 'title')
        for count, article in enumerate(articles):
            ws2.write(count + 1, 0, article.title)
            ws2.write(count + 1, 1, str(article.level))
            ws2.write(count + 1, 2, str(article.category))
            ws2.write(count + 1, 3, article.id)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = 'question-import-format.xls'
        response['Content-Disposition'] = 'attachment; filename=' + filename
        wb.save(response)
        return response
