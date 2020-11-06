from django.forms import ModelForm,TextInput
from .models import ExactLockdownEntries

class LockdownEntryForm(ModelForm):
    class Meta:
        model = ExactLockdownEntries
        fields = ('title','phone_number','slides')
        widgets = {
            'phone_number':TextInput(attrs={'placeholder':'08012345678'})
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].help_text = 'Give a title in this format (firstname_last name) e.g shade_olumide'
        # self.fields['entry_video'].label = 'Video'
