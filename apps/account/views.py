from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404


class EditProfile(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email',] # 'telephone', 'responsable']
    template_name = 'account/update_profile.html'

    def get_success_url(self):
        return reverse("account:edit-profile", kwargs={'username': self.object.username})

    def get_object(self):
        # We get records by primary key, which ensures that
        # changes in the title or slug doesn't break links
        return get_object_or_404(User, username=self.kwargs['username'])

    def test_func(self):
        self.object = self.get_object()
        return self.object == self.request.user or self.request.user.is_superuser
