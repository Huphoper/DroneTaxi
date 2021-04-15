from django import forms


class UserForm(forms.Form):
    login = forms.CharField(label='Логин', label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', label_suffix='')


class RegForm(forms.Form):
    lastname = forms.CharField(label='Фамилия *', label_suffix='')
    firstname = forms.CharField(label='Имя *', label_suffix='')
    patronymic = forms.CharField(label='Отчество *', label_suffix='')
    email = forms.CharField(label='Email *', label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль *', label_suffix='')
    confpassword = forms.CharField(widget=forms.PasswordInput, label='Подтвердить пароль *', label_suffix='')