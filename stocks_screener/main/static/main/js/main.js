function ajax_get(){
    var symbol
    var interval
    $.ajax({
        type: 'GET',
        url: 'get_symbol/',
        data: {},
        dataType: 'json',
        cache: false,
        success: function(data){
            get_json = JSON.parse(JSON.stringify(data))
            console.log(get_json)
            symbol = get_json.symbol
            console.log(symbol)
            interval = get_json.interval
            $.ajax({
                type: 'GET',
                url: 'screener/get_stock_params/',
                data: {
                    'symbol': symbol,
                    'interval': interval
                },
                dataType: 'json',
                cache: false,
                success: function(data){
                    if (data != 'fail'){
                        var stocks_json = JSON.parse(JSON.stringify(data));
                        stocks_json = stocks_json.stock;
                         var screener;
                         var capitalization;
                         var ema10_intersection_up;
                         var ema10_intersection_down;
                         var macd;
                         var ema10_up;
                         var ema10_down;
                         var rsi_up;
                         var rsi_down;
                         var snp500_ema10;
                         if (stocks_json.screener == 'america'){
                            screener = 'Америка'
                         };
                         if (stocks_json.screener == 'russia'){
                            screener = 'Россия'
                         };
                         if (stocks_json.ema10_intersection_up == true){
                            ema10_intersection_up = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            ema10_intersection_up = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.ema10_intersection_down == true){
                            ema10_intersection_down = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            ema10_intersection_down = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.macd == true){
                            macd = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            macd = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.ema10_up == true){
                            ema10_up = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            ema10_up = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.ema10_down == true){
                            ema10_down = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            ema10_down = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.rsi_up == true){
                            rsi_up = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            rsi_up = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.rsi_down == true){
                            rsi_down = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            rsi_down = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         if (stocks_json.snp500_ema10 == true){
                            snp500_ema10 = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                         }else{
                            snp500_ema10 = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                         };
                         const html = `
                              <span class='data_symbol'>Тикер: ${stocks_json.symbol}</span><br>
                              <span class='data_screener'>Страна: ${screener}</span><br>
                              <span class='data_capitalization'>Капитализация: ${stocks_json.capitalization}</span><br>
                              <span class='data_rating'>Smart Score: ${stocks_json.rating}</span><br>
                              <span class='data_ema10_intersection_up'>EMA10 Пересечение<img src="/static/screener/img/up.png">: ${ema10_intersection_up}</span><br>
                              <span class='data_ema10_intersection_down'>EMA10 Пересечение<img src='/static/screener/img/down.png'>: ${ema10_intersection_down}</span><br>
                              <span class='data_macd'>MACD Пересечение: ${macd}</span><br>
                              <span class='data_ema10_up'>EMA10 <img src="/static/screener/img/up.png">: ${ema10_up}</span><br>
                              <span class='data_ema10_down'>EMA10 <img src="/static/screener/img/down.png">: ${ema10_down}</span><br>
                              <span class='data_rsi_up'>RSI <img src="/static/screener/img/up.png">: ${rsi_up}</span><br>
                              <span class='data_rsi_down'>RSI <img src="/static/screener/img/down.png">: ${rsi_down}</span><br>
                              <span class='data_snp500_ema10'>SPX: ${snp500_ema10}</span><br>`;
                         div = document.createElement('div');
                         div.className = 'stocks_list'
                         div.innerHTML = html;
                         document.querySelector('.stock_params').append(div);
                    }
                }
            })
        }
    })
}
ajax_get()