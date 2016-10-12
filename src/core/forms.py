# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from core.models import Round, UserExtension, Software, SingleImage, SingleVideo


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput())
    password_repeat = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password_repeat')

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.all()
        for user in users:
            if username.lower() == user.username.lower():
                raise forms.ValidationError('Username schon vorhanden.')

        return username


class UserProfileForm(forms.ModelForm):
    birthdate = forms.DateField(label="Geburtstag", input_formats=settings.DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = UserExtension
        fields = ('user', 'birthdate', 'avatar')

    def clean_user(self):
        return self.cleaned_data['user']

    def clean_birthdate(self):
        return self.cleaned_data['birthdate']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            #w, h = get_image_dimensions(avatar)

            #validate dimensions
            #max_width = max_height = 100
            #if w > max_width or h > max_height:
            #    raise forms.ValidationError(
            #        u'Please use an image that is '
            #         '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError('Erlaubte Bildformate sind: JPEG, GIF und PNG.')

            #validate file size
            if len(avatar) > (3 * 1024 * 1024):
                raise forms.ValidationError(
                    'Datei überschreitet die maximale Größe von 3 MB')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'file', 'description',)


class ImageForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data['image']
        content_type = image.content_type.split('/')[0]
        if content_type == "image":
            if image._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return image


class VideoForm(forms.Form):
    video = forms.FileField()

    def clean_video(self):
        video = self.cleaned_data['video']
        content_type = video.content_type.split('/')[0]
        if content_type == "video":
            if video._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(video._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return video


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ('pkt1', 'pkt2')
