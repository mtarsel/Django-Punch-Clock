from django.template import Context, loader
from punchclock.models import *
from management.models import *
#from django.http import HttpResponse
from django.shortcuts import render_to_response

def manage(request):
    user_list = UserAccountManagment.objects.all().order_by('-user_account')[:5]
    return render_to_response('management/manage.html', {'user_list': user_list})
