from django import forms
from .models import Conta, Transacao, Categoria

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo', 'ativa', 'saldo_inicial']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['conta', 'tipo', 'valor', 'data', 'paga', 'descricao', 'parcela_numero', 'total_parcelas', 'recorrente']
        widgets = {
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paga': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'parcela_numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'recorrente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))