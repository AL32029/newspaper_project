from allauth.account.forms import SignupForm, UserForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.http.request import HttpRequest


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        common_group = Group.objects.get(name="common")
        common_group.user_set.add(user)
        return user

class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if self.user is None:
            raise ValidationError('Ошибка: пользователь не определен')

        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise ValidationError('Данное имя пользователя уже занято')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.user is None:
            raise ValidationError('Ошибка: пользователь не определен')

        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise ValidationError('Данный адрес электронной почты уже занят')

        return email
