from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView, FormView

from .models import Agent
from .forms import UserForm, AgentForm, RespoForm, CreateUserForm



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
            #url = reverse("account:edit-profile", kwargs={'username': username})
            #return HttpResponseRedirect(url)

    else:
        user_form = UserForm(instance=my_user)
        agent_form = AgentForm(instance=my_agent)
    
    context = {'user_form': user_form, 'agent_form': agent_form}

    return render(request, 'account/update_profile.html', context)


def ChangeResponsable(request):
    '''Vue pour changer le responsable'''

    respo_actuel = Agent.objects.filter(responsable=True)
    if respo_actuel:
        respo_actuel = respo_actuel[0]
    else:
        respo_actuel = None

    if request.method == 'POST':
        #affichage de la page
        respo_form = RespoForm(request.POST, initial={'respo': respo_actuel})
        #validation du formulaire
        if respo_form.is_valid():
            respo = respo_form.cleaned_data['respo']
            if respo:
                respo.responsable = True
                respo.save()
            for user in Agent.objects.all():
                if user != respo and user.responsable:
                    user.responsable = False
                    user.save()

    else:
        respo_form = RespoForm(initial={'respo': respo_actuel})
    
    context = {'respo_form': respo_form}
    return render(request, 'account/update_respo.html', context)



def AddUser(request):
    '''Vue pour ajouter un utilisateur'''
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Agent.objects.create(user=user)
    else:
        form = CreateUserForm()
    return render(request, 'account/create_profile.html', {'form': form})



class AddUserView(FormView):
    template_name = 'account/create_profile.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save()
        # create a unique user name
        initial = form.cleaned_data.get('first_name')[0]
        last_name = slugify(form.cleaned_data.get('last_name'))
        username = initial+last_name
        if User.objects.filter(username=username):
            id = 1
            usernameid = f'{username}-{id}'
            while User.objects.filter(username = usernameid):
                id += 1
                usernameid = f'{username}-{id}'
            username = usernameid
        user.username = username
        print(username)
        user.save()
        agent = Agent(user = user)
        agent.save()
        return redirect(reverse('account:profile-created'))

