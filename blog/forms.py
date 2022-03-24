from . models import BlogComments, Post, BlogCategory
from  django import forms

class PostForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
       
        self.fields['author'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['image'].widget.attrs.update({'class' : 'form-control'})        
        self.fields['body'].widget.attrs.update({'class' : 'form-control'})
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})
        self.fields['category'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})








         
class CommentsForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        fields =(
            'text',
        )

    def __init__(self, *args, **kwargs):
        super(CommentsForm,self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'form form-control px-5', 'placeholder' : 'Surname', 'id':'floatingInput','style':'border-radius:16px;border:2px solid white;'})                              

         


    