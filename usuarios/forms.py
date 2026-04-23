from django import forms
from .models import Usuario, Direccion

class UsuarioRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    terminos = forms.BooleanField(
        required=True,
        error_messages={'required': 'Debes aceptar los términos y condiciones.'}
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo puede contener letras.') 
        return nombre

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo puede contener letras.')
        return apellido

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.rol = 'cliente'
        if commit:
            user.save()
        return user
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números.')
        if len(telefono) != 10:
            raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        if not telefono.startswith('3'):
            raise forms.ValidationError('El teléfono debe comenzar con 3 (celular colombiano).')
        return telefono

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'barrio', 'referencia', 'es_principal']
        widgets = {
            'referencia': forms.Textarea(attrs={'rows': 2}),
        }