from django import forms
from .models import Beneficiary, Intervention

class BeneficiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        
        super(BeneficiaryForm, self).__init__(*args, **kwargs)
        
        if user and user.is_authenticated and hasattr(user, 'userprofile'):
            if user.userprofile.role == 'center_staff':
                if 'center' in self.fields:
                    del self.fields['center']
    class Meta:
        model = Beneficiary
        fields = ['unique_id', 'name', 'date_of_birth', 'center']
        
        labels = {
            'unique_id': 'Unique ID (e.g., AADHAAR)',
            'date_of_birth': 'Date of Birth (YYYY-MM-DD)',
        }
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['intervention_type', 'details']
        
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}), 
        }