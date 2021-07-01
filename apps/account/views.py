from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Agent
from .forms import ChangePassForm
from django.shortcuts import get_object_or_404


class EditProfile(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email',] # 'telephone', 'responsable']
    template_name = 'account/update_profile.html'

    def get_object(self):
        # We get records by primary key, which ensures that
        # changes in the title or slug doesn't break links
        return get_object_or_404(User,
            username=self.kwargs['username'],
        )

    def test_func(self):
        self.object = self.get_object()
        return self.object == self.request.user or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = ChangePassForm(self.object)
        return context