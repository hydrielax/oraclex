from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Agent
from .forms import UserForm, AgentForm, RespoForm
from django.http import HttpResponseRedirect


def EditProfile(request, username):
    '''Vue d'édition du profil'''

    my_user = User.objects.get(username = username)
    my_agent = Agent.objects.get(user = my_user)

    if request.method == 'POST':
        #affichage de la page
        user_form = UserForm(request.POST, instance=my_user)
        agent_form = AgentForm(request.POST, instance=my_agent)
        #validation du formulaire
        if user_form.is_valid() and agent_form.is_valid():
            user_form.save()
            agent_form.save()
            url = reverse("account:edit-profile", kwargs={'username': username})
            return HttpResponseRedirect(url)

    else:
        user_form = UserForm(instance=my_user)
        agent_form = AgentForm(instance=my_agent)
    
    context = {'user_form': user_form, 'agent_form': agent_form}

    return render(request, 'account/update_profile.html', context)


def ChangeResponsable(request):
    '''Vue pour changer le responsable'''

    if request.method == 'POST':
        #affichage de la page
        respo_form = RespoForm(request.POST)
        #validation du formulaire
        if respo_form.is_valid():
            respo = respo_form.cleaned_date['respo']
            respo.responsable = True
            respo.save()
            for user in Agent.objects.all():
                if user != respo and user.responsable:
                    user.responsable = False
                    user.save()
            url = reverse("account:edit-respo")
            return HttpResponseRedirect(url)

    else:
        respo_form = RespoForm()
    
    context = {'respo_form': respo_form}
    
    return render(request, 'account/update_respo.html', context)


'''
class EditProfile(UserPassesTestMixin, UpdateView):
    model = Agent
    fields = ['first_name', 'last_name', 'username', 'email', 'telephone' ]
    template_name = 'account/update_profile.html'

    def get_success_url(self):
        return reverse("account:edit-profile", kwargs={'username': self.object.username})

    def get_object(self):
        # We get records by primary key, which ensures that
        # changes in the title or slug doesn't break links
        return get_object_or_404(Agent, username=self.kwargs['username'])

    def test_func(self):
        self.object = self.get_object()
        return self.object == self.request.user or self.request.user.is_superuser
'''