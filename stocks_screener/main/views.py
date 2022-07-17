from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def get_symbol(request):
    if request.GET:
        data = {
            'symbol': request.session['symbol'][0],
            'interval': request.session['symbol'][1]
        }
        return JsonResponse(data)


def stock_view(request):
    if request.GET:
        timeframe = request.GET['timeframe']
        symbol = request.GET['symbol']
        request.session['symbol'] = [symbol, timeframe]
        return HttpResponse('ok')


def index(request):
    if 'symbol' not in request.session:
        request.session['symbol'] = ['AAPL', 'D']

    context = {
        'timeframe': request.session['symbol'][1],
        'symbol': request.session['symbol'][0]
    }
    return render(request, 'main/index.html', context)


def auth(request):
    pass