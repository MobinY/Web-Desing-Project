import random

import sys

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView

from core.forms import LoginForm, EmployeeCreateForm
from core.models import Customer, Employee
from django.shortcuts import render


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'core/create_employee.html'
    success_url = reverse_lazy('mainPage')
    form_class = EmployeeCreateForm

    # def form_valid(self, form):
    #     response = super(SystemUserCreateView, self).form_valid(form)
    #     username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
    #     new_user = authenticate(username=username, password=password)
    #     user = User.objects.get(username=username)
    #     SystemUser.objects.filter(user=user).update(role=Patient.load())
    #     login(self.request, new_user)
    #     return response

