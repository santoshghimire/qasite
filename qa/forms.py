from django import forms
from .models import Question, Article


class QuestionForm(forms.Form):
    """
    This module handles following activities.

        1. Add Questions for admin
        2. Edit Questions for admin
    """
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': "form-control",
            "required": "required",
            "rows": 3
        })
    )
    image = forms.ImageField(
        required=False
    )
    audio = forms.ImageField(
        required=False
    )
    video = forms.ImageField(
        required=False
    )
    correct = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'required': "required",
        })
    )
    difficulty = forms.ChoiceField(
        required=True,
        choices=[(1, "Easy"), (2, "Medium"), (3, "Hard")],
        widget=forms.Select(attrs={'class': "form-control"})
    )
    # question_type = forms.ChoiceField(
    #     required=True,
    #     choices=[('objective', "Objective"), ('subjective', "Subjective")],
    #     widget=forms.Select(attrs={'class': "form-control"})
    # )

    def __init__(self, previous=None, *args, **kwargs):
        """
        During Form initialization following things are done.

            1. populate the choices corrent options
            2. populate the options choices text, image and html dynamically

        """
        self.instance = kwargs.pop('instance', None)
        self.request = kwargs.pop('request', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['article'] = forms.ChoiceField(
            label='Article',
            choices=[(i.slug, i.title) for i in Article.objects.all()],
            widget=forms.Select(
                attrs={'class': "form-control", 'type': "button"}))

        if self.instance:
            # This is for updating questions,
            # instance sent as kwargs and inititalized here
            self.fields['verified'] = forms.ChoiceField(
                choices=[('0', 'Unverified'), ('1', 'Verified')],
                required=True,
                widget=forms.Select(
                    attrs={
                        'class': "form-control",
                        'type': "button",
                        "required": "required"
                    })
            )

            if self.instance.is_verified:
                self.fields['verified'].initial = '1'
            else:
                self.instance.is_verified = '0'

            self.fields['text'].initial = self.instance.text
            self.fields['image'].initial = \
                self.instance.image
            self.fields['audio'].initial = \
                self.instance.audio
            self.fields['video'].initial = \
                self.instance.video

            self.fields['difficulty'].initial = self.instance.difficulty
            self.fields['correct'].initial = self.instance.correct
            self.fields['article'].initial = \
                self.instance.article.slug

            # self.fields['question_type'].initial = self.instance.question_type

    def clean(self):
        """
        Override base class and handle following.

            1. Form Validation
            2. Put all the error message here for form validation

        """
        super(QuestionForm, self).clean()
        try:
            if not self.cleaned_data['text']:
                raise forms.ValidationError(
                    "Question cannot be empty !!"
                )
        except:
            self.add_error('question_text', "Question cannot be empty !!")

        try:
            int(self.cleaned_data['difficulty'])
        except:
            self.add_error('difficulty', "Please enter a valid difficulty !!")
            raise forms.ValidationError(
                "Difficulty needs to be a valid number !!"
            )

    def save(self, *args, **kwargs):
        """
        Override base class to save following.

            1. Save the form data values on question form

        """
        if self.instance:
            question = self.instance
            if self.cleaned_data['verified'] == '0':
                question.is_verified = False
            else:
                question.is_verified = True

            question.updated_by = self.request.user
            if self.cleaned_data['verified'] == '1':
                question.verified_by = self.request.user
        else:
            question = Question()
            question.created_by = self.request.user

        question.text = self.cleaned_data['text']
        question.image = self.cleaned_data['image']
        question.audio = self.cleaned_data['audio']
        question.video = self.cleaned_data['video']
        question.difficulty = self.cleaned_data['difficulty']
        question.article = Article.objects.get(
            slug=self.cleaned_data['article']
        )
        question.category = question.article.category

        # question.question_type = self.cleaned_data['question_type']
        question.question_type = 'objective'
        # if question.question_type == 'objective':
        question.correct = self.cleaned_data['correct']
        # else:
        #     question.correct = None

        question.save()
        return question
