from django import forms 


class PublicForm(forms.Form):
    public_key = forms.CharField(
        label='Введите ссылку',
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': 'Введите публичную ссылку:', 'style': 'width: 400px'}))
    type = forms.ChoiceField(
        label='Тип файла',
        choices=[
            ('all', 'Все файлы'),
            ('image', 'Изображения'),
            ('doc', 'Документы')
        ],
        required=False
    )