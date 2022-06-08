from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    # if the request is "POST"
    if request.method == "POST":
        # then want to create a form with the data within the request.POST
        form = UserRegisterForm(request.POST)
        # if form data is valid
        if form.is_valid():
            # automatically hashes the password and saves user to db
            form.save()
            # form.cleaned_data is a dictionary containing data converted to python types
            username = form.cleaned_data.get('username')
            # flash message to indicate success in creating new account
            messages.success(request, f'Account created for {username}!')
            # redirect user to homepage name
            return redirect('blog-home')
    else:
        # else return a blank page
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'title': 'Register', 'form': form})

# # types of messages:
# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error
