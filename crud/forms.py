from django import forms
from .models import User
from .enumeraciones import *
from django.contrib.auth.forms import UserCreationForm

##FILTRO PRODUCTOS
class FiltroProductoForm(forms.Form):
    rangos_precios = forms.MultipleChoiceField(
        choices=PRICE_RANGES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

##CREA USUARIOS
class UserForm(UserCreationForm):

    class Meta:
        model=User
        fields=['username','rut','first_name','last_name','celular','email','direccion','postal','password1','password2']

##ACTUALIZA USUARIO
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','celular','email','direccion','postal','password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

##OLVIDO CONTRASEÑA
class UsernameEmailForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=150)
    email = forms.EmailField(label='Correo Electrónico', max_length=254)
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
