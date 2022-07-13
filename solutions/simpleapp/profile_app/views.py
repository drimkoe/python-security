from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required

class ProfileView(LoginRequiredMixin,View):

    def get(self, request):
        #user = request.user
        #if not user.is_authenticated:
        #    return HttpResponse(status=401)
        return render(request,'profile.html')
