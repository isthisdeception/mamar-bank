from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import UserRegistrationForm # Use the renamed form
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import UpdateView
from .forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')
    success_message = "Account created successfully. Please login to continue."


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.info(self.request, "Login successful.")
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out.")
        return super().post(request, *args, **kwargs)


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Your profile has been updated successfully."

    def get_object(self):
        """
        By returning self.request.user, we ignore any ID in the URL.
        This prevents users from trying to edit other people's profiles
        by guessing their User ID.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Optional: Use this if you want to pass extra data to the template,
        like a page title or specific bank stats.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile Settings'
        return context

    def form_invalid(self, form):
        """
        If the form is invalid, we add an error message so the user
        knows exactly why the update failed.
        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)