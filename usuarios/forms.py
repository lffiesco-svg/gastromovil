from django import forms
from .models import Usuario, Direccion

class UsuarioRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'rol', 'password1', 'password2']

        def clean(self):
            cleaned_data = super() .clean()
            p1 = cleaned_data.get('password1')
            p2 = cleaned_data.get('password2')
            if p1 and p2 and p1 != p2:
                raise forms.ValidationError('Las contraseñas no coinciden')
            return cleaned_data
        def save(self, commit= True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
                return user
            
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'barrio', 'referencia', 'es_principal']
        widgets ={
            'referencia': forms.Textarea(attrs={'rows':2}),
        }
        