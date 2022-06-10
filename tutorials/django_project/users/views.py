from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm

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
            messages.success(request, f'{username}, your account has been created! You can now login.')
            # redirect user to the login page
            return redirect('login')
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

@login_required
def profile(request):
    if request.method == 'POST':
        # the first argument gives the POST data, second argument is the instance 
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # the profile form has an extra input for the file that the user is trying to upload
        p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES, 
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            # save the 2 forms
            u_form.save()
            p_form.save()
            # flash message to indicate success in updating the profile
            messages.success(request, f'Your account has been updated!')
            # POST-GET-REDIRECT pattern: avoid confirmation for form resubmission
            return redirect('profile')
    else:
        # if no changes made, fill the form's fields with current profile data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)
