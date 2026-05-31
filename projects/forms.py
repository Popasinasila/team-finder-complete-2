from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""

    class Meta:
        model = Project
        fields = ["title", "description", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название проекта"}),
            "description": forms.Textarea(attrs={"placeholder": "Описание проекта", "rows": 5}),
            "status": forms.Select(),
        }
        labels = {
            "title": "Название",
            "description": "Описание",
            "status": "Статус",
        }
