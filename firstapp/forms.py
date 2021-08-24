from django import forms


class UserForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=30,
        error_messages={"max_length": "Имя не должно превышать 30 символов"})

    age = forms.IntegerField(
        label="Возраст",
        min_value=0,
        max_value=200,
        error_messages={
            "min_value": "Возраст не должен быть отрицательным",
            "max_value": "возраст не должен превышать 200 лет",
            })
