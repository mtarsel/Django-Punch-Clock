from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf


@login_required
def manage(request):
	c ={}
	c.update(csrf(request))
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Your username and/or password were incorrect."

	return render_to_response('management/manage.html',{'state':state, 'username': username})