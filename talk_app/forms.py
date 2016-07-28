from django import forms

from talk_app.models import Video

class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ["name", "url"]
