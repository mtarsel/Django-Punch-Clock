from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404



@login_required(login_url= '/manage_login/')
def manage(request):
	c ={}
	c.update(csrf(request))
	username = password = ''
	
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
				return render_to_response('management/manage.html',{'state':state, 'username': username})
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Incorrect Username or Password."
			#raise Http404
			return render_to_response('404.html', {'state':state, 'username':username})
		
	return render_to_response('management/manage.html',{'state':state, 'username': username})