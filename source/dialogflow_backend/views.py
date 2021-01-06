from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


async def bot(request: HttpRequest) -> HttpResponse:
    return render(request, 'html/bot.html')
