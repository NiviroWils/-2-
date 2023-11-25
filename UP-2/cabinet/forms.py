from django.contrib.auth.models import User
from django import forms

from cabinet.models import Application, Category


class ConfirmField(forms.Field):
    def validate(self, value):
        super(ConfirmField, self).validate(value)
        if value is None:
            raise forms.ValidationError(
                "Ошибка: "
                "Поставьте галочку о согласии"
            )

class UserForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()  # Используйте EmailField для валидации email
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    confirm = ConfirmField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

    def clean_password2(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
            raise forms.ValidationError(
                "Ошибка: "
                "введенные пароли не совпадают"
            )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # Проверка ФИО на кириллические буквы, дефис и пробелы
        if not all(char.isalpha() or char in ('-', ' ') for char in first_name):
            raise forms.ValidationError(
                "Ошибка: "
                "ФИО должно содержать только кириллические буквы, дефис и пробелы"
            )
        return first_name

class ApplicationForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data.get("image")
        image_size = image.size
        str_file = str(image)
        if str_file.endswith('.jpg') and image_size <= 2097152:
            return image
        elif str_file.endswith('.jpeg') and image_size <= 2097152:
            return image
        elif str_file.endswith('.png') and image_size <= 2097152:
            return image
        elif str_file.endswith('.bpm') and image_size <= 2097152:
            return image
        else:
            raise forms.ValidationError(
                "Ошибка: "
                "Файл должен иметь формат: jpg, jpeg, png, bmp и размер не более 2МБ"
            )
        return file

    class Meta:
        model = Application
        fields = ('title', 'description', 'category', 'image', )

class ApplicationDoneForm(forms.ModelForm):
    image_done = forms.ImageField(label='Созданный дизайн', required=True)

    class Meta:
        model = Application
        fields = ('image_done', )

class ApplicationWorkForm(forms.ModelForm):
    comment = forms.CharField(label='Комментарий', required=True)

    class Meta:
        model = Application
        fields = ('comment', )

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', )