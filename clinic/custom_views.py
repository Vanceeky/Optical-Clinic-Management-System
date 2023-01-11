from django.shortcuts import render

def handler404(request, *args, **kwargs):
    response = render('templates/404.html', context = {})
    response.status_code = 404
    return response


def handler500(request, *args, **kwargs):
    response = render('templates/500.html', context={})
    response.status_code = 500
    return response