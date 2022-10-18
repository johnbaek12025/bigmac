from django.http import HttpResponse
from django.shortcuts import render

class registerUser:
    def get(self, req):
        return HttpResponse('this is a user reg form')
