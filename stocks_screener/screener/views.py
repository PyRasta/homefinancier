from django.shortcuts import render
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


def ema10_dowm(dict_ema10):
     if dict_ema10['value_open'] < dict_ema10['ema10'] and dict_ema10['value_close'] < dict_ema10['ema10']:
        return True


def intersection_macd(handler):
    analysis = handler.get_analysis()
    macd_macd = analysis.indicators['MACD.macd']
    macd_signal = analysis.indicators['MACD.signal']
    if round(float(macd_macd), 4) == round(float(macd_signal), 4):
        return True

def rsi_pattern_up(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 52 and rsi <= 53:
        return True

def rsi_pattern_down(handler):
    analysis = handler.get_analysis()
    rsi = analysis.indicators['RSI']
    if rsi > 48 and rsi <= 49:
        return True


def index(request):
    list_stocks = Tv.objects.using('list_stocks').filter(screener='america').filter(exchange='NASDAQ')

    interval = Interval.INTERVAL_1_DAY
    
    for stock in list_stocks:
        handler = TA_Handler(
            symbol=stock.symbol,
            exchange=stock.exchange,
            screener='america',
            interval=interval
        )
        try:
            dict_ema10 = get_ema10(handler)
            if rsi_pattern_up(handler) and intersection_macd(handler) and intersection_up_ema10(dict_ema10):
                print(f'RSI Патерн Вверх: {stock.symbol}')
            if rsi_pattern_down(handler) == True:
                print(f'RSI Патерн Вниз: {stock.symbol}')
        except:
            print('Потрачено')
        #try:
            #if intersection_macd(handler) == True:
               # print(f'Пересечение macd: {stock.symbol}')
        #except:
            #print('Потрачено')
        #try:
            #dict_ema10 = get_ema10(handler)
            #if intersection_up_ema10(dict_ema10) == True:
                #print(f'Пересечение вверх {stock.symbol}')
        #except:
           #print('Не получено')

    return render(request, 'screener/index.html')

