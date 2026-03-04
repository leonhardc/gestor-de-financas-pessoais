from django import forms
from .models import Conta, Transacao, Categoria, OrcamentoMensal

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
        fields = ['conta', 'tipo', 'categoria','valor', 'data', 'paga', 'descricao', 'parcela_numero', 'total_parcelas', 'recorrente']
        widgets = {
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paga': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'parcela_numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'recorrente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        tipo = cleaned_data.get('tipo')

        if categoria and tipo:
            if categoria.tipo != tipo:
                raise forms.ValidationError('A categoria selecionada não é compatível com o tipo da transação.')
        return cleaned_data

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class OrcamentoMensalForm(forms.ModelForm):
    class Meta:
        model = OrcamentoMensal
        fields = ['conta', 'categoria', 'ano', 'mes', 'valor_orcado']
        widgets = {
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_orcado': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PesquisarTransacaoForm(forms.Form):
    tipo = forms.ChoiceField(choices=(('', 'Todos'), ('receita', 'Receita'), ('despesa', 'Despesa')), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)