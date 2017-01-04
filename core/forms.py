from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm, fields_for_model
from django import forms

from core.models import Employee


class LoginForm(ModelForm):
    username = fields_for_model(User)['username']
    # password = fields_for_model(User)['password']
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = []

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        try:
            User.objects.get(username=cleaned_data.get("username"))
        except User.DoesNotExist:
            raise forms.ValidationError('Username "%s" Does not exist.' % cleaned_data.get("username"))

        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password or len(password) < 1:
            raise forms.ValidationError("لطفا رمز عبور خود را وارد نمایید")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("رمز عبور شما نادرست است!")
        return cleaned_data