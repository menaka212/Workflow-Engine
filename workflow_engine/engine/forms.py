from django import forms
from .models import Workflow, Step, Rule

class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ['name', 'input_schema']


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'step_type', 'order', 'metadata']


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['condition', 'next_step', 'priority']