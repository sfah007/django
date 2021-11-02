from django import forms
from .models import *
from account.models import *

class ProfileForm(forms.ModelForm):
    
    #bio = forms.CharField(label='معلومات عنك', required=False)
    profile_image = forms.ImageField(label='صورة الغلاف', required=False)
    social_github = forms.URLField(label='حساب github الخاص بك ', required=False)
    social_instagram = forms.URLField(label='حساب instagram الخاص بك ', required=False)
    social_twitter = forms.URLField(label='حساب twitter الخاص بك ', required=False)
    social_website = forms.URLField(label='موقعك  ', required=False)
    notification = forms.BooleanField(label='الإشعارات ', required=False)
    information_public = forms.BooleanField(label='المعلومات  ', required=False, 
            help_text="رؤية الأخرين للملف الشخصي (Profile)")

    class Meta:
        model = UsersBack
        fields = ['bio',  'profile_image',
                  'social_github', 'social_instagram', 'social_twitter',
                   'social_website', 'notification', 'information_public']


#username = forms.CharField(label="اسم المستخدم ", max_length=30, help_text="اسم المستخدم يجب ألا يحتوي على مسافات")