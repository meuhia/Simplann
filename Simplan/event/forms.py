# coding: utf-8

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field, HTML
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from validate_email import validate_email

from Simplan.settings import MAX_UPLOAD_SIZE, CONTENT_TYPES


class EventGuestForm(forms.Form):
    author = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _(u'Votre nom ou pseudonyme')}))
    
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _(u'Renseignez votre adresse email')}))
    
    title = forms.CharField(
        required=True
        )
    
    description = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'placeholder': ''})
        )
    
    place = forms.CharField(
        required=False
        )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not validate_email(email):
            raise forms.ValidationError("Veuillez saisir une adresse email valide")
        return email
    
    def clean_author(self):
        author = self.cleaned_data['author']
        if author.strip()=='':
            raise forms.ValidationError("Vous devez saisir un nom ou pseudonyme")
        return author
        
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'


        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('place'),
            Field('email'),
            Field('author'),
            Submit('submit', 'Suivant'),
        )
        super(EventGuestForm, self).__init__(*args, **kwargs)

class EventUserForm(forms.Form):
    
    title = forms.CharField(
        required=True
        )
    
    description = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'placeholder': _(u'Décrivez votre événement')})
        )
    
    place = forms.CharField(
        required=False
        )
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('place'),
            Submit('submit', 'Suivant'),
        )
        super(EventUserForm, self).__init__(*args, **kwargs)

        
class OptionTimeForm(forms.Form):
    
    date = forms.DateTimeField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _(u'Selectionnez une date')}))
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            HTML('<div class="large-10 column">'),
            Field('date', css_class='datepicker'),
            HTML('</div>'),
            HTML('<div class="large-2 column">'),
            HTML('<input type="submit" name="submit" value="Valider" class="submit button tiny radius" id="submit-id-submit">'),
            HTML('</div>'),
        )
        super(OptionTimeForm, self).__init__(*args, **kwargs)
        
class OptionFreeForm(forms.Form):
    
    text = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _(u'Saisissez votre option')}))
    
    image = forms.ImageField(
        required=False,
        )
    
    def clean_image(self):
        image = self.cleaned_data['image']
        if image != None:
            content_type = image.content_type
            if content_type in CONTENT_TYPES:
                if image._size > MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(('Votre image est trop grande (%s), La taille maximum autorisee est de %s')\
                           % (filesizeformat(image._size), filesizeformat(MAX_UPLOAD_SIZE)))
            else:
                raise forms.ValidationError(_(u'Ce type de fichier n\'est pas supporté'))
        
        return image
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form_optionfree'

        self.helper.layout = Layout(
            HTML('<div class="large-5 column">'),
            Field('text'),
            HTML('</div>'),
            HTML('<div class="large-5 column">'),
            Field('image'),
            HTML('</div>'),
            HTML('<div class="large-2 column">'),
            HTML('<input type="submit" name="submit" value="Valider" class="submit button tiny radius" id="submit-id-submit">'),
            HTML('</div>'),
        )
        super(OptionFreeForm, self).__init__(*args, **kwargs)

class ChoiceForm(forms.Form):
    
    title = forms.CharField(
        required=True
        )
    
    description = forms.CharField(
        label='Description du choix',
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': _(u'Description du choix')})
        )
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Submit('submit', 'Valider'),
        )
        super(ChoiceForm, self).__init__(*args, **kwargs)

class MailingListForm(forms.Form):
    
    mailing_list = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _(u'Séparez les emails par des virgules')})
        )
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('mailing_list'),
            Submit('submit', 'Valider'),
        )
        super(MailingListForm, self).__init__(*args, **kwargs)

