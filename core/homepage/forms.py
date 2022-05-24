from django import forms

class HomeForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={        
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Tu Nombre',
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={        
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Tu Email',
    }))

    asunto = forms.CharField(widget=forms.TextInput(attrs={        
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Asunto',
    }))

    mensaje = forms.CharField(widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Tu Mensaje',
                }))