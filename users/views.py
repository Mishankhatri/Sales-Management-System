from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register(request):
    "user registration view."
    if request.method == 'POST':
        r_form = UserRegisterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if r_form.is_valid() and p_form.is_valid():
            r_form.save()
            p_form.save()
            username = r_form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for { username }.')
            return redirect('login')
    else:
        r_form = UserRegisterForm()
        p_form = ProfileUpdateForm()
    context = {
        'r_form': r_form,
        'p_form': p_form
    }
    return render(request, 'users/register.html', context)

@login_required
def update_profile(request):
    "update user's profile view."
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')   
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/update_profile.html',context)


@login_required
def dashboard(request):
    "dashboard view"
    return render(request, 'users/dashboard.html')
