from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Users


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Users
        fields = ('email','password','first_name','last_name','phone_num','pol_district',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('email','password','first_name','last_name','phone_num','pol_district',)

