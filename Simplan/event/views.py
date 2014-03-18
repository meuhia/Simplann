# coding: utf-8
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.views.decorators.http import require_POST

from Simplan import settings
from Simplan.event.forms import EventUserForm, EventGuestForm, OptionTimeForm, \
    OptionFreeForm, ChoiceForm, MailingListForm
from Simplan.event.models import OptionTime, OptionFree, Option, EventGuest, \
    EventUser, MakeUserChoice, Choice, MakeGuestChoice
from Simplan.settings import SETTING_CHOICES
from Simplan.utils import render_template
from models import Event
from validate_email import validate_email
from django.contrib import messages


def view_event(request, evt_id1, evt_id2, evt_id3, evt_id4, evt_id5):
    '''
    View an event
    '''
    
    evt_id = evt_id1 +"-"+evt_id2 +"-"+evt_id3 +"-"+evt_id4 +"-"+evt_id5
    try:
        username = request.GET['username'] #in case of edit participation
    except KeyError:
        username = None
    
    event = get_object_or_404(Event, slug_public = evt_id)
    
    return render_template('event/view_event.html', {
                'event': event,
                'username': username
            })
    
    
def new_event(request):
    '''
    Creates a new event
    '''
    
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EventUserForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # Creating event
                event = EventUser()
                event.author = request.user
                event.title = data['title']
                event.description = data['description']
                event.place = data['place']
                event.save()
                
                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug]))
    
            else:
                return render_template('event/new_event.html', {
                    'form': form
                })
        else:
    
            form = EventUserForm(request.user)
            return render_template('event/new_event.html', {
                'form': form
            })
    else:
        if request.method == 'POST':
            form = EventGuestForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # Creating event
                event = EventGuest()
                event.author = data['author']
                event.email = data['email']
                event.title = data['title']
                event.description = data['description']
                event.place = data['place']
                event.save()
                
                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug]))
    
            else:
                return render_template('event/new_event.html', {
                    'form': form
                })
        else:
            form = EventGuestForm(request.user)
            return render_template('event/new_event.html', {
                'form': form
            })

def edit_event(request, evt_id):
    '''
    Edit a new event
    '''
    event = get_object_or_404(Event, slug = evt_id)
    try :
        eg = EventGuest.objects.get(pk=event.pk)
        if request.method == 'POST':
            form = EventGuestForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # Edit event
                eg.author = data['author']
                eg.email = data['email']
                eg.title = data['title']
                eg.description = data['description']
                eg.place = data['place']
                eg.save()
                
                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[eg.slug]))
            else:
                raise Http404
        else:
            form = EventGuestForm(request.user, {
            'title': eg.title,
            'description': eg.description,
            'place': eg.place,
            'email': eg.email,
            'author': eg.author,
            })
            return render_template('event/new_event.html', {
                'form': form
            })
    except:
        ef = EventUser.objects.get(pk=event.pk)
        if request.method == 'POST':
            form = EventUserForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # edit event
                ef.author = request.user
                ef.title = data['title']
                ef.description = data['description']
                ef.place = data['place']
                ef.save()

                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[ef.slug]))
            else:
                raise Http404
        else:
    
            form = EventUserForm(request.user, {
            'title': ef.title,
            'description': ef.description,
            'place': ef.place
            })
            return render_template('event/new_event.html', {
                'form': form
            })

@require_POST
def make_choice(request, evt_id):
    event = get_object_or_404(Event, slug = evt_id)
    
    if request.user.is_authenticated():
        #User Choice
        for option in event.get_time_options():
            if str(option.pk) in request.POST:
                #check if this user have already make choice
                try :
                    muc = MakeUserChoice.objects.get(choice__option__pk=option.pk, user__pk=request.user.pk)
                except:
                    muc = MakeUserChoice()
                    muc.user = request.user
                
                muc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                muc.save()
            else :
                print('réponse introuvable')
        for option in event.get_free_options():
            if str(option.pk) in request.POST:
                #check if this user have already make choice
                try :
                    muc = MakeUserChoice.objects.get(choice__option__pk=option.pk, user__pk=request.user.pk)
                except:
                    muc = MakeUserChoice()
                    muc.user = request.user
                
                muc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                muc.save()
            else :
                print('réponse introuvable')
    else:
        #Guest choice
        for option in event.get_time_options():
            if str(option.pk) in request.POST:
                if 'edit' in request.POST:
                    mgc = MakeGuestChoice.objects.get(choice__option__pk=str(option.pk), username=request.POST['pseudo'])
                    mgc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                else:
                    mgc = MakeGuestChoice()
                    mgc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                    mgc.username = request.POST['pseudo']
                mgc.save()
            else :
                print('réponse introuvable')
        for option in event.get_free_options():
            if str(option.pk) in request.POST:
                if 'edit' in request.POST:
                    mgc = MakeGuestChoice.objects.get(choice__option__pk=str(option.pk), username=request.POST['pseudo'])
                    mgc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                else:
                    mgc = MakeGuestChoice()
                    mgc.choice = Choice.objects.get(pk=request.POST[str(option.pk)])
                    mgc.username = request.POST['pseudo']
                mgc.save()
            else :
                print('réponse introuvable')
    
    return HttpResponseRedirect(reverse('Simplan.event.views.view_event', args=[event.slug_public[0:8], event.slug_public[9:13], event.slug_public[14:18], event.slug_public[19:23], event.slug_public[24:36]]))
    
def new_option(request, evt_id):
    event = get_object_or_404(Event, slug = evt_id)
    try:
        type = request.GET['type']
    except KeyError:
        type = 'time'
    
    if request.method == 'POST':
        if type == 'time': 
            form = OptionTimeForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # Creating option
                option = OptionTime()
                option.start_date = data['date']
                option.event = event
                option.position = event.next_free_position()
                option.save()
                
            else:
                raise Http404
        if type == 'free':
            form = OptionFreeForm(request.user, request.POST, request.FILES)
            if form.is_valid():
                data = form.data
                # Creating option
                option = OptionFree()
                if 'image' in request.FILES: option.image = request.FILES['image']
                option.text = data['text']
                option.event = event
                option.position = event.next_free_position()
                option.save()
                
            else:
                raise Http404
        
         #create default choice
        cpt=0
        for cle, valeur in SETTING_CHOICES[0].items():
            choice = Choice()
            choice.title = cle
            choice.description = cle
            choice.position = cpt
            choice.positive = valeur
            choice.option = option
            choice.save()
            cpt+=1
            
        return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug])+'?type={0}'.format(type))
    else:
        if type == 'time': 
            form = OptionTimeForm(request.user)
            return render_template('event/new_option.html', {
                'form': form,
                'event': event,
                'type': type,
            })
        if type == 'free':
            form = OptionFreeForm(request.user)
            return render_template('event/new_option.html', {
                'form': form,
                'event': event,
                'type': type,
            }) 

def edit_option(request, opt_id):

    try:
        type = request.GET['type']
    except KeyError:
        raise Http404
    
    if type == 'time':
        option = get_object_or_404(OptionTime, pk = opt_id)
    else:
        option = get_object_or_404(OptionFree, pk = opt_id)
        
    event = option.event

    if request.method == 'POST':
        if type == 'time': 
            form = OptionTimeForm(request.user, request.POST)
            if form.is_valid():
                data = form.data
                # Edit option
                option.start_date = data['date']
                option.event = event
                option.save()

                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug])+'?type={0}'.format(type))
            else:
                raise Http404
        if type == 'free':
            form = OptionFreeForm(request.user, request.POST, request.FILES)
            if form.is_valid():
                data = form.data
                # Edit option
                if 'image' in request.FILES: option.image = request.FILES['image']

                option.text = data['text']
                option.event = event
                option.save()
                
                return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug])+'?type={0}'.format(type))
            else:
                raise Http404 
    else:
        if type == 'time': 
            form = OptionTimeForm(request.user, {'date': option.start_date})
            return render_template('event/new_option.html', {
                'form': form,
                'event': event,
                'type': type,
            })
        if type == 'free':
            form = OptionFreeForm(request.user, {'text': option.text})
            return render_template('event/new_option.html', {
                'form': form,
                'event': event,
                'type': type,
            }) 

def up_option(request, opt_id):
    
    option = get_object_or_404(Option, pk = opt_id)
    event = option.event
    
    pos = option.position
    next_options = Option.objects.filter(position__lt = option.position, event__pk = option.event.pk).order_by('-position')
    if next_options.count()>0:
        next_option = next_options[0]
        
        option.position = next_option.position
        option.save()
        
        next_option.position = pos
        next_option.save()
    else:
        raise Http404
    
    return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug]))

def down_option(request, opt_id):
    
    option = get_object_or_404(Option, pk = opt_id)
    event = option.event
    
    pos = option.position
    next_options = Option.objects.filter(position__gt = option.position, event__pk = option.event.pk).order_by('position')
    if next_options.count()>0:
        next_option = next_options[0]
        
        option.position = next_option.position
        option.save()
        
        next_option.position = pos
        next_option.save()
    else:
        raise Http404
    
    return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug]))

def del_option(request, opt_id):
    
    option = get_object_or_404(Option, pk = opt_id)
    event = option.event
    option.delete()
    
    return HttpResponseRedirect(reverse('Simplan.event.views.new_option', args=[event.slug]))

def recap_event(request, evt_id):
    
    event = get_object_or_404(Event, slug = evt_id)
    
    if request.method == 'POST':
        form = MailingListForm(request.user, request.POST)
        if form.is_valid():
            data = form.data
            event.mailing_list = data['mailing_list']
            event.save()
    else:
        form = MailingListForm(request.user, {'mailing_list': event.mailing_list})
    
    return render_template('event/recap_event.html', {
                'event': event,
                'form': form
            }) 
    
def new_choice(request, opt_id):
    
    option = get_object_or_404(Option, pk = opt_id)

    if request.method == 'POST':
        form = ChoiceForm(request.user, request.POST)
        if form.is_valid():
            data = form.data
            # Creating choice
            choice = Choice()
            choice.title = data['title']
            choice.description = data['description']
            choice.option = option
            choice.positive = True
            choice.save()

            return HttpResponseRedirect(reverse('Simplan.event.views.new_choice', args=[option.pk]))
        else:
            raise Http404
    else:
        form = ChoiceForm(request.user)
        return render_template('event/new_choice.html', {
            'form': form
        })

def edit_choice(request, opt_id, ch_id):
    
    option = get_object_or_404(Option, pk = opt_id)
    choice = get_object_or_404(Choice, pk = ch_id)

    if request.method == 'POST':
        form = ChoiceForm(request.user, request.POST)
        if form.is_valid():
            data = form.data
            # Edit choice
            choice.title = data['title']
            choice.description = data['description']
            choice.option = option
            choice.save()

            return HttpResponseRedirect(reverse('Simplan.event.views.new_choice', args=[option.pk]))
        else:
            raise Http404
    else:
        form = ChoiceForm(request.user, {
            'title': choice.title,
            'description': choice.description,
                           })
        return render_template('event/edit_choice.html', {
            'form': form
        })

@require_POST
def modify_choice(request):
    if 'choice_maj' in request.POST:
        choice = Choice.objects.get(pk = request.POST['choice_pk'])
        choice.title = request.POST['choice_title']
        choice.positive = 'choice_positive' in request.POST
        choice.save()
        
        option = choice.option
        event = option.event
        return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[event.slug]))
    elif 'choice_add' in request.POST:
        option = Option.objects.get(pk = request.POST['option_pk'])
        
        choice = Choice()
        choice.title = request.POST['choice_title']
        choice.description = request.POST['choice_title']
        choice.positive = 'choice_positive' in request.POST
        choice.position = option.next_free_position()
        choice.option = option
        choice.save()
        
        event = option.event
        return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[event.slug]))
    elif 'answer_add' in request.POST:
        event = Event.objects.get(pk = request.POST['event_pk'])
        options = Option.objects.filter(event__pk = event.pk).all()
        for option in options :
            choice = Choice()
            choice.title = request.POST['choice_title']
            choice.description = request.POST['choice_title']
            choice.positive = 'choice_positive' in request.POST
            choice.position = option.next_free_position()
            choice.option = option
            choice.save()
        
        return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[event.slug]))

def del_choice(request, ch_id):
    
    choice = get_object_or_404(Choice, pk = ch_id)
    option = choice.option
    choice.delete()
    
    return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[option.event.slug]))

def del_makechoices(request, evt_id):
    
    event = get_object_or_404(Event, slug = evt_id)
    
    try: #find guest choice
        username = request.GET['username']
        makechoices = MakeGuestChoice.objects.filter(choice__option__event__slug=evt_id, username=username).all()
        for makechoice in makechoices:
            makechoice.delete()
    except: #just for user choice
        try :
            username = request.GET['user']
            if request.user.is_authenticated():
                if request.user.username==username:
                    makechoices = MakeUserChoice.objects.filter(choice__option__event__slug=evt_id, user__username=username).all()
                    for makechoice in makechoices:
                        makechoice.delete()
                else:
                    raise "Vous n'avez pas le droit d'effectuer cette action"
        except:
            raise "Vous n'avez pas le droit d'effectuer cette action"

    return HttpResponseRedirect(reverse('Simplan.event.views.view_event', args=[event.slug_public[0:8], event.slug_public[9:13], event.slug_public[14:18], event.slug_public[19:23], event.slug_public[24:36]]))

def end_event(request, evt_id):
    event = Event.objects.get(slug = evt_id)
    
    #send mail for admin
    try: 
        evt = EventGuest.objects.get(pk=event.pk)
        email_admin = evt.email
        author = evt.author
    except:
        try: 
            evt = EventUser.objects.get(pk=event.pk)
            email_admin = evt.author.email
            author = evt.author.username
        except:
            email_admin = ''
            author = ''
    if validate_email(email_admin):
        subject = "Simplan - Lien du sondage : "+event.title
        from_email = 'Simplan <noreply@simplann.eu>'
        message_html = get_template('email/admin.html').render(
                        Context({
                            'url_site': settings.SITE_URL,
                            'event': event,
                            'author': author
                        })
                    )
        message_txt = get_template('email/admin.txt').render(
                        Context({
                            'url_site': settings.SITE_URL,
                            'event': event,
                            'author': author
                        })
                    )
    
        msg = EmailMultiAlternatives(subject, message_txt, from_email, [email_admin])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
    else:
        if request.user.is_authenticated():
            messages.error(request, 'Votre adresse email est invalide. Allez dans les paramètres de votre profil pour la modifier')
        else:
            messages.error(request, 'Vous n\'avez pas saisi d\'adresse email valide au début de ce sondage. Retournez la modifier à la première étape')

        return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[event.slug]))
    
    return HttpResponseRedirect(reverse('Simplan.event.views.view_event', args=[event.slug_public[0:8], event.slug_public[9:13], event.slug_public[14:18], event.slug_public[19:23], event.slug_public[24:36]]))

def invit_end_event(request, evt_id):
    event = Event.objects.get(slug = evt_id)
    
    #send mail for admin
    try: 
        evt = EventGuest.objects.get(pk=event.pk)
        email_admin = evt.email
        author = evt.author
    except:
        try: 
            evt = EventUser.objects.get(pk=event.pk)
            email_admin = evt.author.email
            author = evt.author.username
        except:
            email_admin = ''
            author = ''
    
    if validate_email(email_admin):
        subject = "Simplan - Lien du sondage : "+event.title
        from_email = 'Simplan <noreply@simplann.eu>'
        message_html = get_template('email/admin.html').render(
                        Context({
                            'url_site': settings.SITE_URL,
                            'event': event,
                            'author': author
                        })
                    )
        message_txt = get_template('email/admin.txt').render(
                        Context({
                            'url_site': settings.SITE_URL,
                            'event': event,
                            'author': author
                        })
                    )
    
        msg = EmailMultiAlternatives(subject, message_txt, from_email, [email_admin])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
    else:
        if request.user.is_authenticated():
            messages.error(request, 'Votre adresse email est invalide. Allez dans les paramètres de votre profil pour la modifier')
        else:
            messages.error(request, 'Vous n\'avez pas saisi d\'adresse email valide au début de ce sondage. Retournez la modifier à la première étape')

        return HttpResponseRedirect(reverse('Simplan.event.views.recap_event', args=[event.slug]))
    
    subject = "Simplan - Participez au Sondage : "+event.title
    from_email = 'Simplan <noreply@simplann.eu>'
    mass = event.mailing_list.split(',')

    for mail in mass:
        if validate_email(mail):
            message_html = get_template('email/broadcast.html').render(
                            Context({
                                'url_site': settings.SITE_URL,
                                'event': event,
                                'author': author
                            })
                        )
            message_txt = get_template('email/broadcast.txt').render(
                            Context({
                                'url_site': settings.SITE_URL,
                                'event': event,
                                'author': author
                            })
                        )
            
            msg = EmailMultiAlternatives(subject, message_txt, from_email, [mail])
            msg.attach_alternative(message_html, "text/html")
            msg.send()

    return HttpResponseRedirect(reverse('Simplan.event.views.view_event', args=[event.slug_public[0:8], event.slug_public[9:13], event.slug_public[14:18], event.slug_public[19:23], event.slug_public[24:36]]))
