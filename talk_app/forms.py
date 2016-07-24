from django import forms

from talk_app.models import Survey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['discussion_level', 'change_mind', 'changed', 'made_choice', 'chose', 'top_area']
        widgets = {'change_mind': forms.RadioSelect, 'made_choice': forms.RadioSelect}
# this isn't being used. it was to put a second form on a page. but both can't be submitted at once.
# class OrderDrinkForm(forms.ModelForm):
#
#     class Meta:
#         model = OrderDrink
#         fields = ['order_tag', 'drink', 'drink_quantity', 'notes', 'order_up']


# class OrderDrinkForm(forms.ModelForm):
#     class Meta:
#         model = OrderDrink
#         fields = ['order_tag', 'drink', 'drink_quantity', 'notes']
#         widgets = {'drink': forms.RadioSelect}
