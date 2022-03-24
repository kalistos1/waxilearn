from django.shortcuts import render,redirect
from .models import Course, StudentCourses, Lesson,Text
from django.contrib import messages
#from tutorials.models import Tutorial
from .forms import AddTextForm, SearchCourseForm, CommentForm, AddCourseForm, AddLessonForm,CategoryForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from membership.models import *
from django.contrib import messages




# list of all courses of a given user

@login_required
def courses_me(request):
    user_membership = UserMembership.objects.filter(user=request.user)
    user = request.user 
    try:   
        studentcourses = StudentCourses.objects.filter(user_id=user.id)

    except StudentCourses.DoesNotExist:
        studentcourses = None
    return render(request, "dashboard/student/student-my-courses.html", {'studentcourses':studentcourses, 'user_membership': user_membership,})



# list of all courses of a given instructor

@login_required
def instructor_courses(request):
    user = request.user 
    courses = Course.objects.filter(instructor_id=user.id)
    page_number = request.GET.get('page')
    course_paginator = Paginator(courses , 4)
    page = course_paginator.get_page(page_number)
   
    context ={
        'courses':courses,
        'count':course_paginator.count,
        'page':page,
        }
    
    return render(request, "dashboard/instructor/instructor-courses.html", context)



# this displays the list of all the courses in the database

@login_required
def courses_all(request):
    courses = Course.objects.all().order_by('-created_on')[:6]
    page_number = request.GET.get('page')
    course_paginator = Paginator(courses , 3)
    page = course_paginator.get_page(page_number)
   
    form = SearchCourseForm()
    context  = {
        'count':course_paginator.count,
        'form':form,
        'page':page,
    }
    return render(request, "dashboard/student/student-browse-courses.html", context)
    


# course search view

@login_required
def search_courses(request):
    if request.method == "POST":
        searched = request.POST['title']
        user_search = Course.objects.filter(title__icontains = searched)
        form = SearchCourseForm()
        
        #pagination
        page_number = request.GET.get('page')
        search_paginator = Paginator(user_search, 1)
        page = search_paginator.get_page(page_number)
        context = {
            'count': search_paginator.count,
            'searched':searched,
            'page':page,
            'form':form,
        }
        return render(request, "dashboard/student/student-course-search.html", context)
    else:
        
        return render(request, "dashboard/student/student-course-search.html")
         


# this loads the courses viewed on the browse course page or after listed by course search by a user

@login_required
def load_course(request, pk):
    user = request.user
    course = Course.objects.get(pk=pk)
    outline = course.lesson_set.all()
    comments = course.comment_set.all()
    user_bought_course = StudentCourses.objects.filter(user__pk=user.id, course__pk=pk).count()
    user_membership = UserMembership.objects.filter(user=request.user) 
    user_subscription = Subscription.objects.all

    if user_bought_course <= 0:
        user_bought_course = False
    else:
        user_bought_course = True

    context = {
            'course':course,
            'user_bought_course':user_bought_course,
            'outline':outline,
            'comments':comments,
             'user_membership':user_membership,
             'user':user,
             'user_subscription':user_subscription
        }
    return render(request, "dashboard/student/student-view-course.html", context)



 # load_course loads, the full content of a course enrolled to ,by a user so he can start learn
 
@login_required
def student_start_course(request, slug):
    user = request.user
    course = Course.objects.get(slug=slug)
    lessons = course.lesson_set.all()
    user_bought_course = StudentCourses.objects.filter(user__pk=user.id, course__slug=slug).count()
    comment_form = CommentForm()

    if user_bought_course <= 0:
        user_bought_course = False
    else:
        user_bought_course = True
    context = {
            'course':course,
            'user_bought_course':user_bought_course,
            'comment_form': comment_form,
            'lessons':lessons,
           
        }
    return render(request, "dashboard/student/student-take-course.html", context)


@login_required
def student_start_lesson(request,slug):
    user = request.user
    active_lesson= Lesson.objects.get(slug=slug)
    lesson_text = active_lesson.text_set.all()
    lessons= active_lesson.course.lesson_set.all()         
    context = {
        'lessons':lessons,
        'user':user,
        'active_lesson':active_lesson,
        'lesson_text':lesson_text,
    }
    return render(request,'dashboard/student/student-take-lesson.html',context)
    


# this view adds a course to  the list of courses a user is bought or has added to learn

@login_required
def buy_course(request, slug):   
    course = Course.objects.get(slug=slug)
    StudentCourses.objects.create(user=request.user, course=course,)
    messages.success(request,"successfully enrolled to course")
    return redirect('onlinecourses:courses_me')



@login_required
def open_course(request, pk):
    pass


@login_required
def add_comment(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

           #create new review, but don't save yet
            review = form.save(commit=False)
            review.course_id = pk
            review.user = request.user
             
            #Now save new review
            review.save()
            context = {
                'message' : 'New course review added successfully'                
            }   
            return render(request, "onlinecourses/course.html", context)
        else:
            pass

    else:
        pass

  

@login_required
def create_course(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False) 
            course.instructor_id = request.user.id
            course.save()
            messages.success(request,'course was added successfully go ahead to add lessons')
            return redirect('onlinecourses:add_lesson')             
        else:
            add_course_form = AddCourseForm() 
            messages.error(request,'course was not added reinput the data and resubmit')        
            context = {
                'form':add_course_form,
            }  
        return render(request, "dashboard/instructor/instructor-courses.html", context)      
    else:
        add_course_form = AddCourseForm()

        context = {
            'form':add_course_form,
        }
        return render(request, "dashboard/instructor/instructor-add-course.html", context)



# this is used to delete courses
@login_required
def delete_course(request, pk):
    Course.objects.filter(pk=pk).delete()
    courses = Course.objects.filter(instructor_id=request.user.id)
    context = {
        'courses':courses,
    }
    return render(request, "dashboard/instructor/instructor-courses.html", context)


# this view is used to edit courses

@login_required
def edit_course(request,pk):
    if request.method == 'POST':
        course = Course.objects.get(pk=pk)
      
        if courseForm.is_valid():
            courseForm.save()
            messages.success(request, ('course was successfully updated!'))
            return redirect('onlinecourses:instructor_courses_all')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        course = Course.objects.get(pk=pk)
        courseForm = AddCourseForm(instance=course)

        context={
            'form':courseForm,
        }  
    return render(request,"dashboard/instructor/instructor-edit-course.html",context)



@login_required
def instructor_course_preview(request,pk):
    user = request.user
    course = Course.objects.get(pk=pk)
    lessons = course.lesson_set.all()
    context ={
        'user':user,
        'course':course,
        'lessons':lessons,
    }
    return render(request, 'dashboard/instructor/instructor-preview-course.html', context)


@login_required
def instructor_lesson_preview(request,pk):
    lesson= Lesson.objects.get(pk=pk)
    lesson_text = lesson.text_set.all()
    no_video_url = Lesson.objects.filter(add_video__exact='')
    context = {
        'lesson':lesson,
        'lesson_text':lesson_text,
    }
    return render(request, 'dashboard/instructor/instructor-preview-lesson.html', context)



@login_required
def add_lesson(request):
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New lesson added successful add Text For lesson')
            return redirect('onlinecourses:add_text')
        else:
            messages.error(request,'unable to add lesson check your form and resubmit')
            context = {
                'form':form,
            }
        return render(request, "dashboard/instructor/instructor-add-lesson.html", context)
    else:
        form = AddLessonForm()
        context = {
           'form':form,           
        }  
    return render(request, "dashboard/instructor/instructor-add-lesson.html", context)



@login_required
def add_more_lesson(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request,'New lesson added successful add Text For lesson')
            return redirect('onlinecourses:add_text')
        else:
            messages.error(request,'unable to add lesson check your form and resubmit')
            context = {
                'form':form,
            }
        return render(request, "dashboard/instructor/instructor-add-lesson.html", context)
    else:
        form = AddLessonForm()
        context = {
           'form':form,           
        }  
    return render(request, "dashboard/instructor/instructor-add-lesson.html", context)


@login_required    
def Add_Lesson_text(request,id):

    if request.method == 'POST':
        form =AddTextForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'the lesson text was added successfully review the lesson')
            return redirect('onlinecourses:instructor_courses_all')   
        else:
            messages.error(request,'the text for this lesson was not added succesfully')
            context={
                 'form':form,
            }
            return render(request, "dashboard/instructor/instructor-add-lesson-text.html", context)
    else:
        form = AddTextForm()
        context ={
            'form':form,
        }
        return render(request, "dashboard/instructor/instructor-add-lesson-text.html", context)



def  AddCategory(request):
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            categoryform.save()
            messages.success(request,' category created successfully')
            return redirect('onlinecourses:create_course')
        else:
            messages.error(request,'unable to create category')
            categoryform = CategoryForm()
            context ={
                'categoryform':categoryform,
            }
            return render(request,"dashboard/instructor/instructor-add-category.html", context)
    else:
        categoryform = CategoryForm()
        context ={
                'categoryform':categoryform,
            }
        return render(request,"dashboard/instructor/instructor-add-category.html", context)



def terms(request):
    return render(request, "onlinecourses/terms.html", {})


