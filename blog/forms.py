from . models import BlogComments, Post, BlogCategory
from  django import forms

class PostForms(forms.ModelForm):
    class Meta:
        model = Post
        fields =(
            'author',
            'title',
            'image',
            'body',
            'slug',
            'category',
            'status'
        )



         
class CommentsForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        fields =(

            'text',
        )

    def __init__(self, *args, **kwargs):
        super(CommentsForm,self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'form form-control px-5', 'placeholder' : 'Surname', 'id':'floatingInput','style':'border-radius:16px;border:2px solid white;'})                              

         


    