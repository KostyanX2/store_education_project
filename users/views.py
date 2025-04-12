from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from users.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileFrom
from products.models import Basket
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin
class UserLoginView(TitleMixin,LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegView(TitleMixin,SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегестрированы!"
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin,UpdateView):
    model = User
    form_class = UserProfileFrom
    template_name = "users/profile.html"
    title = 'Store - Личный кабинет'
    def get_success_url(self, **kwargs):
        return reverse_lazy("users:profile", args = (self.object.id, ))
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user = self.object)
        return context



# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {"form": form}
#     return render(request, "users/login.html", context)

# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm
#     context = {"form": form}
#     return render(request, 'users/registration.html', context)

# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileFrom(instance=request.user,data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:profile"))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileFrom(instance=request.user)
#
#
#
#     context = {"title": "Store - профиль",
#                'form': form,
#                "baskets": Basket.objects.filter(user=request.user),
#                }
#     return render(request, "users/profile.html", context)