# coding: utf-8

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Div, Fieldset, Submit, Field, \
    HTML
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from Simplan.account.models import Profile
from validate_email import validate_email


class ProfileForm(forms.Form):
    id_facebook = forms.CharField(
        label='Id Facebook',
        required=False)
    id_twitter = forms.CharField(
        label='Id Twitter',
        required=False)
    id_gplus = forms.CharField(
        label='Id Google Plus',
        required=False)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
                Field('id_facebook'),
                Field('id_twitter'),
                Field('id_gplus'),
                
                Submit('submit', 'Editer mon profil'),
        )
        super(ProfileForm, self).__init__(*args, **kwargs)
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Adresse email')
    username = forms.CharField(label='Nom d\'utilisateur', max_length=30)
    password = forms.CharField(
        label='Mot de passe', max_length=76, widget=forms.PasswordInput,
    )
    password_confirm = forms.CharField(
        label='Confirmation', max_length=76, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            Field('password_confirm'),
            Field('email'),
            Submit('submit', 'Valider mon inscription'),
            HTML('<a href="/" class="button secondary">Annuler</a>')
        )
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Les mots de passe sont différents'
            self._errors['password'] = self.error_class([''])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password' in cleaned_data:
                del cleaned_data['password']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        # Check that the user doesn't exist yet
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            msg = u'Ce nom d\'utilisateur est déjà utilisé'
            self._errors['username'] = self.error_class([msg])
        
        # Check that email doesn't exist yet
        email = cleaned_data.get('email')
        
        print('-----------------> '+str(email))
        if email==None :
            msg = u'Veuillez renseigner votre adresse email'
            self._errors['email'] = self.error_class([msg])
        elif not validate_email(email):
            msg = u'Cette adresse email ne respecte pas le format'
            self._errors['email'] = self.error_class([msg])
        elif User.objects.filter(email=email).count() > 0:
            msg = u'Cette adresse email est déjà utilisée'
            self._errors['email'] = self.error_class([msg])

        return cleaned_data


#to update email/username
class ChangeUserForm(forms.Form):
    
    username_new = forms.CharField(
        label='Nouveau pseudo ',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Laissez vide pour conserver l\'ancien'}))
    
    email_new = forms.EmailField(
        label='Nouvel email ',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Laissez vide pour conserver l\'ancien'}))
    
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.user = user

        self.helper.layout = Layout(
            Field('username_new'),
            Field('email_new'),
            Submit('submit', 'Changer'),
        )
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        
# to update a password

class ChangePasswordForm(forms.Form):
    password_new = forms.CharField(
        label='Nouveau mot de passe ', max_length=76, widget=forms.PasswordInput)
    password_old = forms.CharField(
        label='Mot de passe actuel ', max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label='Confirmer le nouveau mot de passe ', max_length=76, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.user = user

        self.helper.layout = Layout(
                Field('password_old'),
                Field('password_new'),
                Field('password_confirm'),
                
                Submit('submit', 'Changer mon mot de passe'),
        )
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        password_old = cleaned_data.get('password_old')
        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if the actual password is not empty
        if password_old:
            user_exist = authenticate(
                username=self.user.username, password=password_old
            )
            if not user_exist and password_old != "":
                self._errors['password_old'] = self.error_class(
                    [u'Mot de passe incorrect.'])
                if 'password_old' in cleaned_data:
                    del cleaned_data['password_old']

        # Check that the password and it's confirmation match
        if not password_confirm == password_new:
            msg = u'Les mots de passe sont différents.'
            self._errors['password_new'] = self.error_class([msg])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password_new' in cleaned_data:
                del cleaned_data['password_new']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        return cleaned_data

# Reset the password

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('username'),
            Submit('submit', 'Envoyer'),
            HTML('<a href="/" class="button secondary">Annuler</a>')
        )
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

class NewPasswordForm(forms.Form):
    password = forms.CharField(
        label='Mot de passe', max_length=76, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Confirmation', max_length=76, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('password'),
            Field('password_confirm'),
            Submit('submit', 'Envoyer'),
            HTML('<a href="/" class="button secondary">Annuler</a>')
        )
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(NewPasswordForm, self).clean()

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Les mots de passe sont différents'
            self._errors['password'] = self.error_class([''])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password' in cleaned_data:
                del cleaned_data['password']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        return cleaned_data
