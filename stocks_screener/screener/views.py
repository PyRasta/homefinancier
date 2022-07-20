from time import sleep
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tv
from tradingview_ta import *


def get_ema10(handler):
    analysis = handler.get_analysis()
    ema10 = analysis.indicators['EMA10']
    value_open = analysis.indicators['open']
    value_close = analysis.indicators['close']
    dict_ema10 = {"ema10": ema10, 'value_open': value_open, 'value_close': value_close}
    return dict_ema10


def snp500_ema10_up(interval):
    handler = TA_Handler(
        symbol='SPX',
        exchange='SP',
        screener='cfd',
        interval=interval
    )
    analysis = handler.get_analysis()
    ema10 = analysis.indicators['EMA10']
    value_open = analysis.indicators['open']
    value_close = analysis.indicators['close']
    dict_ema10 = {"ema10": ema10, 'value_open': value_open, 'value_close': value_close}
    if dict_ema10['value_open'] > dict_ema10['ema10'] and dict_ema10['value_close'] > dict_ema10['ema10']:
        return True


def snp500_ema10_down(interval):
    handler = TA_Handler(
        symbol='SPX',
        exchange='SP',
        screener='cfd',
        interval=interval
    )
    analysis = handler.get_analysis()
    ema10 = analysis.indicators['EMA10']
    value_open = analysis.indicators['open']
    value_close = analysis.indicators['close']
    dict_ema10 = {"ema10": ema10, 'value_open': value_open, 'value_close': value_close}
    if dict_ema10['value_open'] < dict_ema10['ema10'] and dict_ema10['value_close'] < dict_ema10['ema10']:
        return True


def intersection_up_ema10(dict_ema10):
    if dict_ema10['value_open'] < dict_ema10['ema10'] and dict_ema10['value_close'] > dict_ema10['ema10']:
        return True


def intersection_down_ema10(dict_ema10):
    if dict_ema10['value_open'] > dict_ema10['ema10'] and dict_ema10['value_close'] < dict_ema10['ema10']:
        return True


def ema10_up(dict_ema10):
    if dict_ema10['value_open'] > dict_ema10['ema10'] and dict_ema10['value_close'] > dict_ema10['ema10']:
        return True


def ema10_down(dict_ema10):
    if dict_ema10['value_open'] < dict_ema10['ema10'] and dict_ema10['value_close'] < dict_ema10['ema10']:
        return True


def intersection_macd(handler):
    analysis = handler.get_analysis()
    macd_macd = analysis.indicators['MACD.macd']
    macd_signal = analysis.indicators['MACD.signal']
    if round(float(macd_macd), 2) == round(float(macd_signal), 2):
        return True


def rsi_pattern_up(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 51 and rsi <= 54:
        return True


def rsi_pattern_down(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 46 and rsi <= 49:
        return True


def find_pattern_stocks(stock, interval):
    stock_patterns = {}
    handler = TA_Handler(
        symbol=stock.symbol,
        exchange=stock.exchange,
        screener=stock.screener,
        interval=interval
    )
    try:
        dict_ema10 = get_ema10(handler)
        if intersection_up_ema10(dict_ema10):
            stock_patterns['symbol'] = stock.symbol
            stock_patterns["exchange"] = stock.exchange
            stock_patterns["screener"] = stock.screener
            stock_patterns['rating'] = stock.rating
            stock_patterns['capitalization'] = f'{stock.capitalization}$'
            stock_patterns['ema10_intersection_up'] = True

        else:
            stock_patterns['symbol'] = stock.symbol
            stock_patterns["exchange"] = stock.exchange
            stock_patterns["screener"] = stock.screener
            stock_patterns['rating'] = stock.rating
            stock_patterns['capitalization'] = f'{stock.capitalization}$'
            stock_patterns['ema10_intersection_up'] = False

        if intersection_down_ema10(dict_ema10):
            stock_patterns['ema10_intersection_down'] = True
        else:
            stock_patterns['ema10_intersection_down'] = False

        if ema10_up(dict_ema10):
            stock_patterns['ema10_up'] = True
        else:
            stock_patterns['ema10_up'] = False

        if ema10_down(dict_ema10):
            stock_patterns['ema10_down'] = True
        else:
            stock_patterns['ema10_down'] = False

        if intersection_macd(handler):
            stock_patterns['macd'] = True
        else:
            stock_patterns['macd'] = False

        if rsi_pattern_up(handler) and intersection_up_ema10(dict_ema10) or rsi_pattern_up(handler) and ema10_up(
                dict_ema10):
            stock_patterns['rsi_up'] = True
        else:
            stock_patterns['rsi_up'] = False

        if rsi_pattern_down(handler) and intersection_down_ema10(dict_ema10) or rsi_pattern_down(
                handler) and ema10_down(dict_ema10):
            stock_patterns['rsi_down'] = True
        else:
            stock_patterns['rsi_down'] = False
        return stock_patterns
    except:
        return False


def filter_pattern(patterns, stock):
    flags = []
    for pattern in patterns.values():
        if stock:
            if pattern in stock.keys():
                if stock[pattern]:
                    flags.append(True)
                else:
                    flags.append(False)
        else:
            return False
    if False in flags:
        return False
    else:
        return True


def index(request):
    if 'symbol' in request.session:
        del request.session['symbol']
    return render(request, 'screener/screener.html')


def selection_country(request):
    if request.GET:
        if request.GET['smart_score'] == 'no':
            stock_queryset = \
            Tv.objects.using('list_stocks').order_by('-capitalization').filter(screener=request.GET['select_country'])[
                int(request.GET['x'])]
        else:
            stock_queryset = Tv.objects.using('list_stocks').order_by('-capitalization').filter(
                screener=request.GET['select_country']).filter(rating=int(request.GET['smart_score']))[
                int(request.GET['x'])]
        stocks = find_pattern_stocks(stock_queryset, request.GET['timeframe_selection'])
        if filter_pattern(request.GET, stocks):
            data = {
                "stock": stocks,
            }
            return JsonResponse(data)
        else:
            return HttpResponse('fail')


def get_stock_params(request):
    if request.GET:
        symbol = request.GET['symbol']
        interval = request.GET['interval']
        if interval == 'M':
            interval = '1M'
        elif interval == 'D':
            interval = '1d'
        elif interval == 'W':
            interval = '1W'
        elif interval == '240':
            interval = '4h'
        elif interval == '180':
            interval = '3h'
        elif interval == '120':
            interval = '2h'
        elif interval == '60':
            interval = '1h'
        elif interval == '30':
            interval = '30m'
        elif interval == '15':
            interval = '15m'
        elif interval == '5':
            interval = '5m'
        stock_queryset = Tv.objects.using('list_stocks').get(symbol=symbol)
        patterns = find_pattern_stocks(stock_queryset, interval)
        data = {
            'stock': patterns
        }
        return JsonResponse(data)
    else:
        return HttpResponse('fail')


def get_snp500(request):
    snp500_ema10 = ''
    if request.GET:
        interval = request.GET['interval']
        if interval == 'M':
            interval = '1M'
        elif interval == 'D':
            interval = '1d'
        elif interval == 'W':
            interval = '1W'
        elif interval == '240':
            interval = '4h'
        elif interval == '180':
            interval = '3h'
        elif interval == '120':
            interval = '2h'
        elif interval == '60':
            interval = '1h'
        elif interval == '30':
            interval = '30m'
        elif interval == '15':
            interval = '15m'
        elif interval == '5':
            interval = '5m'
        if snp500_ema10_up(interval):
            snp500_ema10 = True
        elif snp500_ema10_down(interval):
            snp500_ema10 = False
        else:
            snp500_ema10 = False
        data = {
            "snp500": snp500_ema10,
        }
        return JsonResponse(data)
