from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.

def homepage(request):
	return render(request,'home.html')

def register(request):

	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if password1==password2:
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Please Choose another Username')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.error(request, 'An account has been already registered with this email!')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username, password=password1, email=email)
				user.save();
				messages.success(request,'Horray!User has been created')
				return redirect('login')
		else:
			messages.error(request, 'Oops! The passwords did not match')
			return redirect('register')
		return redirect('/')
		
	else:
		return render(request, 'register.html')



def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password1']

		user = auth.authenticate(username = username, password = password)

		if user is not None:
			auth.login(request,user)
			return redirect('/')

		else:
			messages.info(request,'invalid credentials')
			return redirect('login')

	else:
		return render(request, 'login.html')



def logout(request):
	auth.logout(request)
	return redirect('/')


@login_required
def profile(request):
	if request.method=='POST':
		uform = UserUpdateForm(request.POST,instance=request.user)
		pform = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

		if uform.is_valid() and pform.is_valid():
			uform.save()
			pform.save()
			return redirect('profile')
	else:
		uform = UserUpdateForm(instance=request.user)
		pform = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'uform':uform,
		'pform':pform
	}

	return render(request,'profile.html',context)
