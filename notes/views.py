from datetime import date
from django.shortcuts import redirect, render
# from django.contrib.auth import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import*
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
# Create your views here.



def custom_csrf_failure_view(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please try again.")


def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')


def user_login(request):
    error = ""
    
    if request.method == 'POST':
        u = request.POST.get('emailid')
        p = request.POST.get('pwd')

        print("Request Method: POST")
        print("Username:", u)

        # Validate the form
        if not u or not p:
            print("Form Validation Failed")
            error = 'Invalid username or password'
        else:
            user = authenticate(username=u, password=p)
            print("Authenticated User:", user)

            if user is not None:
                login(request, user)
                print("Login Successful")
                return redirect('profile')
            else:
                print("Authentication Failed")
                error = 'Invalid username or password'

    d = {'error': error}
    return render(request, 'user_login.html', d)


def login_admin(request):
    error = ""
    
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pwd')

        # Validate the form
        if not u or not p:
            error = 'yes'
        else:
            user = authenticate(username=u, password=p)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                error = 'yes'

    d = {'error': error}
    return render(request, 'login_admin.html', d)


def signup1(request):
    error = ""
    d = {'error': error}

    if request.method == "POST":
        print("CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
        print("POST Data:", request.POST)

        f = request.POST.get('firstname', '')
        l = request.POST.get('lastname', '')
        c = request.POST.get('contact', '')
        e = request.POST.get('emailid', '')
        p = request.POST.get('password', '')
        b = request.POST.get('branch', '')
        r = request.POST.get('role', '')

        try:
            user = User.objects.create_user(username=e, password=p, first_name=f, last_name=l)
            Signup.objects.create(user=user, contact=c, branch=b, role=r)
            error = "no"
            # Redirect to 'user_login' page upon successful signup
            return redirect('user_login')
        except Exception as e:
            print(e)
            error = "yes"

        d = {'error': error}

    return render(request, 'signup.html', d)


def admin_home(request):
    if not request.user.is_staff:
        return redirect(login_admin)
    P = Notes.objects.filter(status="pending").count()
    A = Notes.objects.filter(status="Accept").count()
    R = Notes.objects.filter(status="Reject").count()
    All = Notes.objects.all().count()
    d = {'P':P , 'A':A, "R":R, "All":All}
    return render(request,'admin_home.html',d)


def Logout(request):
    logout(request)
    return render(request,'index.html')


# def profile(request):
#     if not request.user.is_authenticated:
#         return redirect(user_login)
#     user = user.objects.get(id=request.user.id)
#     data = Signup.objects.get(user=user)
#     d = {'data' : data, 'user' : user}
#     return render(request,'profile.html',d)

def profile(request):
    user = request.user  # Use lowercase 'user'
    data = Signup.objects.get(user=user)  # Use lowercase 'user' here as well

    d = {'data': data, 'user': user}
    return render(request, 'profile.html', d)

# def change_password(request):
#     error=""
#     d={'error':error}

#     if request.method=="POST":
#         o=request.POST['old']
#         n=request.POST['new']
#         c=request.POST['confirm']
#         if c==n:
#             u = User.objects.get(username__exact=request.user.username)
#             u.set_password(n)
#             u.save()
#             error="no"
#         else:
#             error="yes"
#             d={'error':error}

#     return render(request, 'change_password.html',d)



# @login_required
# @csrf_protect
# def change_password(request):
#     if request.method == "POST":
#         # Use request.POST.get() to safely get form data
#         old_password = request.POST.get('old', '')
#         new_password = request.POST.get('new', '')
#         confirm_password = request.POST.get('confirm', '')

#         # Validate if the confirm password matches the new password
#         if new_password == confirm_password:
#             # Check if the old password is correct
#             if request.user.check_password(old_password):
#                 # Change the user's password
#                 request.user.set_password(new_password)
#                 request.user.save()
#                 messages.success(request, 'Password changed successfully.')
#                 return redirect('user_login.html')  # Change to your desired success view
#             else:
#                 messages.error(request, 'Incorrect old password.')
#         else:
#             messages.error(request, 'New password and confirm password do not match.')

#     # Render the form with potential error messages
#     return render(request, 'change_password.html')
@login_required
@csrf_protect
def change_password(request):
    error = ""  # Initialize error as an empty string

    if request.method == "POST":
        old_password = request.POST.get('old', '')
        new_password = request.POST.get('new', '')
        confirm_password = request.POST.get('confirm', '')

        if new_password == confirm_password:
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('user_login')
            else:
                error = "yes"  # Set the error variable
                messages.error(request, 'Incorrect old password.')
        else:
            error = "yes"  # Set the error variable
            messages.error(request, 'New password and confirm password do not match.')

    # Pass the 'error' variable to the template
    return render(request, 'change_password.html', {'error': error})

def edit_profile(request):
    user = request.user  # Use lowercase 'user'
    data = Signup.objects.get(user=user)  # Use lowercase 'user' here as well
    error=False
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        user.save()
        data.save()
        error=True

    d = {'data': data, 'user': user, 'error': error}
    return render(request, 'edit_profile.html', d)



# def upload_notes(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     error = ""
#     d = {'error': error}

#     if request.method == "POST":
#         print("CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
#         print("POST Data:", request.POST)

#         b = request.POST.get('branch', '')
#         s = request.POST.get('subject', '')
#         n = request.FILES.get('notesfile', '')
#         f = request.POST.get('filetype', '')
#         d = request.POST.get('description', '')
#         # u = User.objects.filter(username=request.username)
#         u = User.objects.get(username=request.user.username)

#         try:
#             Notes.objects.create(user=u, uploadingdate=date.today, branch=b, subject=s,
#                                  notesfile=n,filetype=f,description=d,status='pending')
#             error = "no"
#             # Redirect to 'user_login' page upon successful signup
#             return redirect('upload_notes')
#         except Exception as e:
#             print(e)
#             error = "yes"

#         d = {'error': error}

#     return render(request, 'upload_notes.html', d)


# def view_notes(request):
#     user = request.user  # Use lowercase 'user'
#     notes = Notes.objects.filter(user=user)  # Use lowercase 'user' here as well
    

#     d = {'notes': notes}
#     return render(request, 'view_notes.html', d)

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    d = {'error': error}

    if request.method == "POST":
        print("CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
        print("POST Data:", request.POST)

        b = request.POST.get('branch', '')
        s = request.POST.get('subject', '')
        n = request.FILES.get('notesfile', '')
        f = request.POST.get('filetype', '')
        d = request.POST.get('description', '')
        u = User.objects.get(username=request.user.username)

        try:
            # Convert date to string in isoformat
            uploading_date = date.today().isoformat()

            Notes.objects.create(
                user=u,
                uploadingdate=uploading_date,
                branch=b,
                subject=s,
                notesfile=n,
                filetype=f,
                description=d,
                status='pending'
            )
            error = "no"
            # Redirect to 'upload_notes' page upon successful upload
            return redirect('view_notes')
        except Exception as e:
            print(e)
            error = "yes"

        d = {'error': error}

    return render(request, 'upload_notes.html', d)

def view_notes(request):
    user = request.user
    notes = Notes.objects.filter(user=user)
    d = {'notes': notes}
    return render(request, 'view_notes.html', d)


def delete_notes(request, pid):
    # if not request.user.is_staff:
    #     return redirect('user_login')
    
    note = Notes.objects.get(id=pid)
    note.delete()
    
    return redirect('view_notes')

def view_users(request):
    users = Signup.objects.all()
    d = {'users': users}
    return render(request, 'view_users.html', d)


def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')



def pending_notes(request):
    notes = Notes.objects.filter(status="pending")
    d = {'notes': notes}
    return render(request, 'pending_notes.html', d)


# def assign_status(request, pid):
#     notes = Notes.objects.get(id=pid)
#     error = ""

#     if request.method == "POST":
#         s = request.POST.get('status', '')
#         try:
#             notes.status = s
#             notes.save() 
#             error = "no"
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             error = "yes"




def assign_status(request, pid):
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        s  = request.POST.get('status', '')
        try:
            notes.status = s
            notes.save() 
            error = "no"
        except Exception as e:
            print(f"An error occurred: {e}")
            error = "yes"

    d = {'notes': notes, 'error': error}
    return render(request, 'assign_status.html', d)



# def assign_status(request, pid):
#     notes = Notes.objects.get(id=pid)
#     error = ""
    
#     if request.method == "POST":
#         s = request.POST.get('status', '')
#         try:
#             notes.status = s
#             notes.save() 
#             error = "no"
#             # Redirect to the 'accepted' page
#             return redirect('accepted_notes') 
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             error = "yes"

#     d = {'notes': notes, 'error': error}
#     return render(request, 'assign_status.html', d)


def accepted_notes(request):
    
    notes = Notes.objects.filter(status="Accept")
    d = {'notes': notes}
    return render(request, 'accepted_notes.html', d)

def rejected_notes(request):
    notes = Notes.objects.filter(status="Reject")
    d = {'notes': notes}
    return render(request, 'rejected_notes.html', d)

def all_notes(request):
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'all_notes.html', d)

def delete_notes(request, pid):
    if not request.user.is_staff:
        return redirect('user_login')
    
    notes = Notes.objects.get(id=pid)
    notes.delete()
    
    return redirect('all_notes')

def view_all_notes(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    notes = Notes.objects.filter(status="Accept")
    d = {'notes': notes}
    return render(request, 'view_all_notes.html', d)
