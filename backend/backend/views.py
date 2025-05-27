from http import HTTPStatus

from django.http.response import HttpResponse


def health(request):
    return HttpResponse("Healthy", status=HTTPStatus.OK)
