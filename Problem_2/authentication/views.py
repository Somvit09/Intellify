from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import LoginForm, SignUpForm_Student, SignUpForm_teacher
from django.contrib.auth.decorators import login_required
from .models import RegisterTeacher, RegisterStudent


def login_view(request):  # login view
    form = LoginForm(request.POST or None)  # login form

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")  # get the data
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # login the user if user have credentials
                return redirect("home")  # back to home with credentials
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})  # rendering the login template


def register_student(request):
    msg = None
    success = False

    if request.method == "POST":  # checking the method is POST or not
        form = SignUpForm_Student(request.POST)
        if form.is_valid():  # checking the form is valid or not
            form.save()
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            raw_password = form.cleaned_data.get("password1")
            standard = form.cleaned_data.get('standard')
            section = form.cleaned_data.get('section')
            stream = form.cleaned_data.get('stream')  # grabing the data from the form
            roll_no = form.cleaned_data.get('roll_no')
            student_id = form.cleaned_data.get('student_id')
            email = form.cleaned_data.get('email')
            student = RegisterStudent.objects.create_account(username=username, first_name=first_name,
                                                             last_name=last_name,
                                                             password=raw_password)  # creating a student object from the RegisterStudent model to store the credentials
            student.standard = standard
            student.section = section
            student.stream = stream
            student.roll_no = roll_no
            student.student_id = student_id
            student.email = email  # store the extra attributes
            student.save()  # save
            msg = 'User created successfully.'
            success = True

            return redirect("login")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm_Student()

    return render(request, "accounts/register_student.html", {"form": form, "msg": msg, "success": success})


def register_teacher(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm_teacher(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            raw_password = form.cleaned_data.get("password1")
            subject = form.cleaned_data.get("subject")
            classes_taught = form.cleaned_data.get("classes_taught")
            contact_number = form.cleaned_data.get("contact_number")  # getting the data from the form
            teacher_id = form.cleaned_data.get("teacher_id")
            email = form.cleaned_data.get("email")
            teacher = RegisterTeacher.objects.create_account(username=username, first_name=first_name,
                                                             last_name=last_name,
                                                             password=raw_password)  # creating a teacher object from RegisterTeacher class to store the data
            teacher.subject = subject
            teacher.classes_taught = classes_taught
            teacher.contact_number = contact_number
            teacher.teacher_id = teacher_id
            teacher.email = email  # store the extra attributes
            teacher.save()
            msg = 'User created successfully.'
            success = True

            return redirect("login")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm_teacher()

    return render(request, "accounts/register_teacher.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url='/login/')
def profile(request):
    student_object = RegisterStudent.objects.filter(username=request.user).exists()
    teacher_object = RegisterTeacher.objects.filter(username=request.user).exists()
    if student_object:  # if user is student returns True
        student_object = RegisterStudent.objects.get(username=request.user)  # get that particular user
        data = dict(
            username=request.user,
            first_name=student_object.first_name,
            last_name=student_object.last_name,
            standard=student_object.standard,
            section=student_object.section,
            stream=student_object.stream,
            roll_no=student_object.roll_no,
            student_id=student_object.student_id,
            email=student_object.email  # making a context
        )
        return render(request, 'accounts/profile_student.html', data)  # sending the context to the template
    elif teacher_object:  # if user is teacher return True
        teacher_object = RegisterTeacher.objects.get(username=request.user)
        data = dict(
            username=request.user,
            first_name=teacher_object.first_name,
            last_name=teacher_object.last_name,
            subject=teacher_object.subject,
            classes_taught=teacher_object.classes_taught,
            contact_number=teacher_object.contact_number,
            teacher_id=teacher_object.teacher_id,  # making a context
            email=teacher_object.email
        )
        return render(request, 'accounts/profile_teacher.html', data)  # sending the context to the template
    else:
        return redirect('login')  # if no user then return back to login


def index(request):
    return render(request, 'home/index.html')  # home page


@login_required(login_url="login")
def logout(request):
    auth_logout(request)  # logout
    return redirect('login')
