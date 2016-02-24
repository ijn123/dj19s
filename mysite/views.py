from django.http import HttpResponse


def home(request):
    return HttpResponse('<h2>Hi from Django</h2>')
