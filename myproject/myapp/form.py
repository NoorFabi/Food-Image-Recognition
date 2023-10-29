from django import forms
from .models import Images

#I want to create a form for uploading image
class ImageForm(forms.ModelForm):
    class Meta: #Meta class will connect the model to the form
        model=Images
        fields=("image",)


#"python -m pip install Pillow