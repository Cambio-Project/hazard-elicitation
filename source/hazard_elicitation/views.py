from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


async def ui(request: HttpRequest) -> HttpResponse:
    return render(request, 'html/ui.html')
