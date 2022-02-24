from django import forms
from .models import Course, Comment, Lesson, Text, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
    def __init__(self, *args ,**kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control', 'id':'title', 'placeholder':'Search for course'})



class SearchCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(SearchCourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control', 'id':'title', 'placeholder':'Search for course'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class' : 'form-control', 'id':'content', 'rows':'4', 'placeholder':'What do you think about this course'})


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'category', 'description', 'objective', 'eligibility', 'photo','slug')

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['category'].widget.attrs.update({'class' : 'form-control'})
        self.fields['description'].widget.attrs.update({'class' : 'form-control'})
        self.fields['objective'].widget.attrs.update({'class' : 'form-control'})
        self.fields['eligibility'].widget.attrs.update({'class' : 'form-control'})
        self.fields['photo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})
        

class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'course','add_video','description')

    def __init__(self, *args, **kwargs):
        super(AddLessonForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['course'].widget.attrs.update({'class' : 'form-control'})  
        self.fields['add_video'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['description'].widget.attrs.update({'class' : 'form-control'})
        
      
class AddTextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('lesson','course','title', 'body','slug')

    def __init__(self, *args, **kwargs):
        super(AddTextForm, self).__init__(*args, **kwargs)
       
        self.fields['lesson'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['course'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})        
        self.fields['body'].widget.attrs.update({'class' : 'form-control'})
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})
 
"""
class AddPDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ('title', 'size','url',)

    def __init__(self, *args, **kwargs):
        super(AddPDFForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})        
        self.fields['size'].widget.attrs.update({'class' : 'form-control'})
        self.fields['url'].widget.attrs.update({'class' : 'form-control'})

"""