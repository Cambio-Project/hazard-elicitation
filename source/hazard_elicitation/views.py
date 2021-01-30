from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from util.tracing import add_trace


@add_trace(True)
async def ui(request: HttpRequest) -> HttpResponse:
    return render(request, 'html/ui.html')
