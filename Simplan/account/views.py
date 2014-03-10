# coding: utf-8

from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
import uuid

from Simplan import settings
from Simplan.account.forms import ChangePasswordForm, ChangeUserForm, LoginForm, \
    RegisterForm, ForgotPasswordForm, NewPasswordForm, ProfileForm
from Simplan.account.models import Profile, TokenRegister, TokenForgotPassword
from Simplan.utils import render_template
from Simplan.utils.tokens import generate_token


def index(request):
    '''Displays the list of registered users'''
    accounts = User.objects.order_by('date_joined')
    return render_template('account/index.html', {
        'accounts': accounts
    })

def details(request, user_name):
    '''Displays details about a profile'''
    usr = get_object_or_404(User, username=user_name)
    
    try:
        profile = Profile.objects.get(user__pk = usr.pk)
    except:
        raise Http404

    return render_template('account/profile.html', {
        'usr': usr, 'profile': profile
    })

def plans(request):
    '''Returns all events of the authenticated user'''
    profile = Profile.objects.get(user=request.user)

    user_events = profile.get_events()
    
    return render_template('account/events.html', {
        'user_events': user_events,
    })

@login_required
def settings_profile(request):
    '''User's settings about his personal information'''
    # extra information about the current user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            profile.id_facebook = form.data['id_facebook']
            profile.id_twitter = form.data['id_twitter']
            profile.id_gplus = form.data['id_gplus']

            try:
                profile.save()
            except:
                messages.error(request, 'Une erreur est survenue.')
                return redirect(reverse('Simplan.account.views.settings_profile'))

            messages.success(
                request, 'Le profil a correctement été mis à jour.')
            
            return redirect(reverse('Simplan.account.views.settings_profile'))
        else:
            return render_to_response('account/settings_profile.html', c, RequestContext(request))
    else:
        form = ProfileForm(initial={
            'id_facebook': profile.id_facebook,
            'id_twitter': profile.id_twitter,
            'id_gplus': profile.id_gplus}
        )
        c = {
            'form': form
        }
        return render_to_response('account/settings_profile.html', c, RequestContext(request))


@login_required
def settings_account(request):
    '''User's settings about his account'''
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            try:
                request.user.set_password(form.data['password_new'])
                request.user.save()
                messages.success(
                    request, 'Le mot de passe a bien été modifié.')
                return redirect(reverse('Simplan.account.views.settings_account'))
            except:
                messages.error(request, 'Une erreur est survenue.')
                return redirect(reverse('Simplan.account.views.settings_account'))
        else:
            return render_to_response('account/settings_account.html', c, RequestContext(request))
    else:
        form = ChangePasswordForm(request.user)
        c = {
            'form': form,
        }
        return render_to_response('account/settings_account.html', c, RequestContext(request))

@login_required
def settings_user(request):
    '''User's settings about his email'''
    profile = get_object_or_404(Profile, user__pk=request.user.pk)
    
    if request.method == 'POST':
        form = ChangeUserForm(request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            email_exist = User.objects.filter(email = form.data['username_new']).count()
            username_exist = User.objects.filter(username = form.data['username_new']).count()
            
            old = User.objects.filter(pk = request.user.pk).all()[0]
            if form.data['username_new'] and username_exist > 0:
                raise Http404
            elif form.data['username_new']:
                if form.data['username_new'].strip() != '':
                    old.username = form.data['username_new']
                
            if form.data['email_new'] and email_exist > 0:
                raise Http404
            elif form.data['email_new']:
                if form.data['email_new'].strip() != '':
                    old.email = form.data['email_new']
                
            old.save()
            
            return redirect(profile.get_absolute_url())
        
        else:
            return render_to_response('account/settings_user.html', c, RequestContext(request))
    else:
        form = ChangeUserForm(request.user)
        c = {
            'form': form,
        }
        return render_to_response('account/settings_user.html', c, RequestContext(request))

def login_view(request):
    '''Log in user'''
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    error = False

    # Redirecting user once logged in?
    if request.GET.has_key('next'):
        next_page = request.GET['next']
    else:
        next_page = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['get_token'] = generate_token()
                if not 'remember' in request.POST:
                    request.session.set_expiry(0)
                
                try:
                    profile = get_object_or_404(Profile, user=request.user)
                    profile.save()
                    # Annotation isn't possible for this method. So we check
                    # if the user is ban when we retrieved him.
                    if not profile.can_read_now():
                        logout_view(request)
                except :
                    profile= None

                # redirect the user if needed
                try:
                    return redirect(next_page)
                except:
                    return redirect(reverse('Simplan.event.views.new_event'))
            else:
                error = 'Les identifiants fournis ne sont pas valides'
        else:
            error = 'Veuillez spécifier votre identifiant et votre mot de passe'
    else:

        form = LoginForm()
    csrf_tk['error'] = error
    csrf_tk['form'] = form
    csrf_tk['next_page'] = next_page
    return render_template('account/login.html', {
        'form': form,
        'csrf_tk': csrf_tk,
        'next_page': next_page,
    })

@login_required
def logout_view(request):
    '''Log out user'''
    
    if request.GET.has_key('next'):
        next_page = request.GET['next']
    else:
        next_page = None
        
    logout(request)
    request.session.clear()
    
    try:
        return redirect(next_page)
    except:
        return redirect(reverse('Simplan.event.views.new_event'))


def register_view(request):
    '''Register a new user'''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])
            user.is_active=False
            user.save()
            profile = Profile(user=user)
            profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # Generate a valid token during one hour.
            uuidToken = str(uuid.uuid4())
            date_end = datetime.now() + timedelta(days=0, hours=1, minutes=0, seconds=0)
            token = TokenRegister(user=user, token = uuidToken, date_end = date_end)
            token.save()

            #send email
            subject = "Simplan - Confirmation d'inscription"
            from_email = 'Simplan <noreply@simplann.eu>'
            message_html = get_template('email/confirm_register.html').render(
                            Context({
                                'username': user.username,
                                'url': settings.SITE_URL+token.get_absolute_url(),
                                'url_site': settings.SITE_URL,
                            })
                        )
            message_txt = get_template('email/confirm_register.txt').render(
                            Context({
                                'username': user.username,
                                'url': settings.SITE_URL+token.get_absolute_url(),
                                'url_site': settings.SITE_URL,
                            })
                        )

            msg = EmailMultiAlternatives(subject, message_txt, from_email, [user.email])
            msg.attach_alternative(message_html, "text/html")
            msg.send()
            
            return render_template('account/register_success.html', {
                'user': user
            })


    form = RegisterForm()
    return render_template('account/register.html', {
        'form': form
    })

def forgot_password(request):
    '''If the user forgot his password, he can have a new one'''
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            data = form.data
            username = data['username']

            usr = get_object_or_404(User, username=username)

            # Generate a valid token during one hour.
            uuidToken = str(uuid.uuid4())
            date_end = datetime.now() + timedelta(days=0, hours=1, minutes=0, seconds=0)
            token = TokenForgotPassword(user=usr, token = uuidToken, date_end = date_end)
            token.save()

            #send email
            subject = "Simplan - Mot de passe oublié"
            from_email = 'Simplan <noreply@simplann.eu>'
            message_html = get_template('email/confirm_forgot_password.html').render(
                            Context({
                                'username': usr.username,
                                'url': settings.SITE_URL+token.get_absolute_url(),
                                'url_site': settings.SITE_URL,
                            })
                        )
            message_txt = get_template('email/confirm_forgot_password.txt').render(
                            Context({
                                'username': usr.username,
                                'url': settings.SITE_URL+token.get_absolute_url(),
                                'url_site': settings.SITE_URL,
                            })
                        )
                
            msg = EmailMultiAlternatives(subject, message_txt, from_email, [usr.email])
            msg.attach_alternative(message_html, "text/html")
            msg.send()
            return render_template('account/forgot_password_success.html')
        else:
            return render_template('account/forgot_password.html', {'form': form})

    form = ForgotPasswordForm()
    return render_template('account/forgot_password.html', {
        'form': form
    })

def new_password(request):
    '''Create a new password for a user'''
    try:
        token = request.GET['token']
    except KeyError:
        return redirect(reverse('Simplan.event.views.new_event'))

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            data = form.data
            password = data['password']

            token = get_object_or_404(TokenForgotPassword, token = token)

            # User can't confirm his request if it is too late.
            if datetime.now() > token.date_end:
                return render_template('account/new_password_failed.html')

            token.user.set_password(password)
            token.user.save()
            token.delete()

            return render_template('account/new_password_success.html')
        else:
            return render_template('account/new_password.html', {'form': form})

    form = NewPasswordForm()
    return render_template('account/new_password.html', {
        'form': form
    })

def active_account(request):
    '''Active token for a user'''
    try:
        token = request.GET['token']
    except KeyError:
        return redirect(reverse('Simplan.event.views.new_event'))

    token = get_object_or_404(TokenRegister, token = token)
    usr = token.user
    # User can't confirm his request if it is too late.
    if datetime.now() > token.date_end:
        return render_template('account/token_account_failed.html')
    
    usr.is_active = True
    usr.save()
    
    token.delete()
    
    
    return render_template('account/token_account_success.html', {'user':usr})