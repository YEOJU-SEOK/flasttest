from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class SignUpForm(django_forms.ModelForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password']
        # 화면에 나타난 각 필드별 명칭 변경
        # labels = {
        #     'email': '이메일주소', 'name': '성명', 'username': '사용자이름', 'password': '비밀번호'
        # }
        # 비밀번호 입력시 보이지 않게함
        widgets = {
            'email': django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name':  django_forms.TextInput(attrs={'placeholder': '이름'}),
            'username': django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password' : django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }
