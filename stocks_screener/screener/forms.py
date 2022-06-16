from django import forms


class SelectOptionForm(forms.Form):
    choices_screeners = [
        ('russia', 'Россия'),
        ('america', 'Америка')
            ]
    screeners = forms.ChoiceField(label='Выберите страну', required=True, choices=choices_screeners)
    ema10_up = forms.BooleanField(label='EMA10-Вверх', required=False)
    ema10_down = forms.BooleanField(label='EMA10-Вниз', required=False)
    intersection_ema10_up = forms.BooleanField(label='Пересечение EMA10-Вверх', required=False)
    intersection_ema10_down = forms.BooleanField(label='Пересечение EMA10-Вниз', required=False)
    rsi_up = forms.BooleanField(label='RSI-Вверх', required=False)
    rsi_down = forms.BooleanField(label='RSI-Вниз', required=False)
    macd = forms.BooleanField(label='Пересечение MACD', required=False)
