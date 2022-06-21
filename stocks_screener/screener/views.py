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
    if round(float(macd_macd), 3) == round(float(macd_signal), 3):
        return True

def rsi_pattern_up(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 51 and rsi <= 52:
        return True

def rsi_pattern_down(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 47 and rsi <= 49:
        return True


def find_pattern_stocks(stock):
    interval = Interval.INTERVAL_1_DAY
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
            stock_patterns['ema10_intersection_up'] = True

        else:
            stock_patterns['symbol'] = stock.symbol
            stock_patterns["exchange"] = stock.exchange
            stock_patterns["screener"] = stock.screener
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

        if rsi_pattern_up(handler) and intersection_up_ema10(dict_ema10):
            stock_patterns['rsi_up'] = True
        else:
            stock_patterns['rsi_up'] = False
            
        if rsi_pattern_down(handler) and intersection_down_ema10(dict_ema10):
            stock_patterns['rsi_down'] = True
        else:
            stock_patterns['rsi_down'] = False
        return stock_patterns        
    except:
        return False

def queryset_to_dict(queryset):
    output = {}
    output["symbol"] = queryset.symbol
    output["exchange"] = queryset.exchange
    output["screener"] = queryset.screener
    return output    


def filter_pattern(patterns, stock):
    flags = []
    for pattern in patterns.values():
        if stock != False:
            if pattern in stock.keys():
                if stock[pattern] == True:
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
    return render(request, 'screener/index.html')


def selection_country(request):
    if request.GET:
        stock_queryset = Tv.objects.using('list_stocks').filter(screener=request.GET['select_country'])[int(request.GET['x'])]
        stocks = find_pattern_stocks(stock_queryset)
        if filter_pattern(request.GET, stocks):
                data = {
                    "stock": stocks,
                }
                return JsonResponse(data)
        else:
            return HttpResponse('fail')           

