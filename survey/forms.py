from django import forms  
from survey.models import Survey 

#class EmployeeForm(forms.ModelForm):  
#    class Meta:  
#        model = Employee  
#       fields = "__all__"  
class SurveyForm(forms.ModelForm):  
    class Meta:  
        model = Survey  
        fields = "__all__"  
