from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import *


# домашняя
class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(status='В').order_by('-created')[:4]
        applications_count = Application.objects.filter(status='П').count()
        context = {'applications': applications, 'applications_count': applications_count}
        return render(request, self.template_name, context)

# регистрация
class RegisterView(TemplateView):
    form_class = UserForm
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid(): # проверяем форму регистрации
            user =form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request,user)
                return HttpResponseRedirect("/")

        return render(request, self.template_name, locals())

# логин
class LoginView(TemplateView):
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect("/")
        err = "Неправильное имя пользователя или пароль"
        return render(request, self.template_name, locals())

# выход
class LogoutView(TemplateView):
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")

class ApplicationCreateView(TemplateView, LoginRequiredMixin):
    form_class = ApplicationForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():  # проверяем форму регистрации
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            return redirect('profile')

        return render(request, self.template_name, locals())

class ProfileView(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(applicant=request.user).order_by('-created')
        context = {'application_list': applications}
        return render(request, self.template_name, context)

class FilterProfileView(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(
            applicant=self.request.user, status=self.request.GET.get('status')[0]).order_by('-created')
        context = {'application_list': applications}
        return render(request, self.template_name, context)

class ApplicationDeleteView(TemplateView, LoginRequiredMixin):
    success_url = reverse_lazy('application_delete_confirm')

    def get(self, request, pk, *args, **kwargs):
        application = Application.objects.get(id=pk)
        if application.status == 'Н':
            return render(request, self.template_name, locals())

class ApplicationDeleteConfirmView(TemplateView, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        application = Application.objects.get(id=pk)
        application.delete()
        return redirect('profile')

class ApplicationListView(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(status='Н')
        context = {'applications': applications}
        return render(request, self.template_name, context)

class ApplicationDoneChangeStatusView(TemplateView, LoginRequiredMixin):
    form_class = ApplicationDoneForm
    def get(self, request, pk, *args, **kwargs):
        form = self.form_class(None)
        application = Application.objects.get(id=pk)
        context = {'application': application, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        application = Application.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=application)

        if form.is_valid():  # проверяем форму регистрации
            instance = form.save(commit=False)
            instance.status = 'В'
            instance.save()
            return redirect('applications_list')

        return render(request, self.template_name, locals())

class ApplicationWorkChangeStatusView(TemplateView, LoginRequiredMixin):
    form_class = ApplicationWorkForm
    def get(self, request, pk, *args, **kwargs):
        form = self.form_class(None)
        application = Application.objects.get(id=pk)
        context = {'application': application, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        application = Application.objects.get(id=pk)
        form = self.form_class(request.POST, instance=application)

        if form.is_valid():  # проверяем форму регистрации
            instance = form.save(commit=False)
            instance.status = 'П'
            instance.save()
            return redirect('applications_list')

        return render(request, self.template_name, locals())

class CategoryListView(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, self.template_name, context)

class CategoryCreateView(TemplateView, LoginRequiredMixin):
    form_class = CategoryForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():  # проверяем форму регистрации
            form.save()
            return redirect('categories_list')

        return render(request, self.template_name, locals())

class CategoryDeleteView(TemplateView, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(id=pk)
        category.delete()
        return redirect('categories_list')
