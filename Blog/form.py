from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'content': FroalaEditor(),
            # style title
            'title': forms.TextInput(attrs={'class': 'mb-4 form-control bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-green-600 focus:border-green-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            
            
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'image': 'Image',
        }
        
        
        