var  div = document.createElement('div');
$('#select_country_btn').click(function(){
    div.remove()
})

$('#select_country_btn').click(function(){
    var x = 0
    div = document.createElement('div');
    for(x = 0; x < 10; x++){
        if ($("#macd").prop('checked')){
            var macd = 'macd';
        } else {
            var macd = 'no';
        };
        $.ajax({    
            type: 'GET',
            url: 'selection_country/',
            data: {
                'x': x,
                'select_country': $('#country_selection').val(),
                'ema10_selection': $('#ema10_selection').val(),
                'ema10_intersection_selection': $('#ema10_intersection_selection').val(),
                'rsi_selection': $('#rsi_selection').val(),
                'macd': macd
            },    

            dataType: 'json',

            cache: false,

            success: function(data){
                if (data != 'fail'){
                    var stocks_json = JSON.parse(JSON.stringify(data));
                    stocks_json = stocks_json.stock;
                    const html = `<div id="stocks_list">
                        Название тикера: <button value='${stocks_json.exchange}'>${stocks_json.symbol}</button>
                        Биржа торговли: ${stocks_json.exchange}
                        Страна тикера: ${stocks_json.screener}<br>
                        EMA10 Пересечение Вверх: ${stocks_json.ema10_intersection_up}
                        EMA10 Пересечение Вниз: ${stocks_json.ema10_intersection_down}
                        MACD Пересечение: ${stocks_json.macd}
                        EMA10 Вверх: ${stocks_json.ema10_up}
                        EMA10 Вниз: ${stocks_json.ema10_down}
                        RSI Вверх: ${stocks_json.rsi_up}
                        RSI Вниз: ${stocks_json.rsi_down}<br>
                        </div>`;
                    div.insertAdjacentHTML('beforeend', html);
                    document.querySelector('#stocks_list').append(div);
                }    
            }
        });
    };
});    

$('#stock').click(function(){
    console.log('нажата')
    const html = `<div id="tradingview_5cce6"></div>
          <div class="tradingview-widget-copyright"><a href="https://ru.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">График AAPL</span></a> от TradingView</div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {
          "autosize": true,
          "symbol": "NASDAQ:AAPL",
          "interval": "D",
          "timezone": "Etc/UTC",
          "theme": "light",
          "style": "1",
          "locale": "ru",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "allow_symbol_change": true,
          "container_id": "tradingview_5cce6"
        }
          );
          </script>`
    $('.tradingview-widget-container').innerHTML(html)      
})


