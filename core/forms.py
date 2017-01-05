from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm, fields_for_model, TextInput, Select, DateInput, ModelChoiceField
from django import forms
from django.utils.crypto import get_random_string

from core.models import Customer, Employee, Branch


class LoginForm(ModelForm):
    username = fields_for_model(User)['username']
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
            raise forms.ValidationError("password invalid")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("user is shasgool")
        return cleaned_data


class EmployeeCreateForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'sex', 'birth_date', 'birth_place',
                  'social_id', 'address', 'education', 'relationship']
        labels = {
            'first_name': "نام",
            'last_name': "نام خانوادگی",
            'sex': "جنسیت",
            'birth_date': "تاریخ تولد",
            'birth_place': "محل تولد",
            'social_id': "کد ملی",
            'address': "آدرس",
            'education': "تحصیلات",
            'relationship': "وضعیت تاهل",
            'branch': 'شعبه'
        }

    def clean(self):
        cleaned_data = super(EmployeeCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        username = get_random_string(length=8)
        password = get_random_string(length=8)
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name)
        employee = Employee(user=user, **self.cleaned_data)
        return employee
