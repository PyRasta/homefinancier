var tr = document.createElement('tr');
function ajax_get(x, y){
    select_country_btn.setAttribute("disabled", "disabled");
    for(x = x; x < y; x++){
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
                'timeframe_selection': $('#timeframe_selection').val(),
                'macd': macd,
                'smart_score': $('#smart_score_selection').val(),
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
                    }
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
                    const html = `
                        <td><a href='/'  class='stock' value='${stocks_json.exchange}:${stocks_json.symbol}' target='blank'>${stocks_json.symbol}</a></td>
                        <td>${screener}</td>
                        <td>${stocks_json.capitalization}</td>
                        <td>${stocks_json.rating}</td>
                        <td>${ema10_intersection_up}</td>
                        <td>${ema10_intersection_down}</td>
                        <td>${macd}</td>
                        <td>${ema10_up}</td>
                        <td>${ema10_down}</td>
                        <td>${rsi_up}</td>
                        <td>${rsi_down}</td>`;
                    tr = document.createElement('tr');
                    tr.innerHTML = html;
                    document.querySelector('tbody').append(tr);
                }
            }
        });
    };
};

function ajax_snp500(){
    $.ajax({
            type: 'GET',
            url: 'get_snp500/',
            data: {
                'interval': $('#timeframe_selection').val()
            },

            dataType: 'json',

            cache: false,

            success: function(data){
                var snp500 = JSON.parse(JSON.stringify(data));
                snp500 = snp500.snp500
                if (snp500 == true){
                        snp500_ema10 = '<img src="/static/screener/img/green.png" width=30px height=30px>'
                    }else{
                        snp500_ema10 = '<img src="/static/screener/img/red.png" width=30px height=30px>'
                    };
                const snp500_html = `
                    SPX EMA10: ${snp500_ema10}
                `
                span = document.createElement('span');
                span.innerHTML = snp500_html;
                document.querySelector('.other_pattern').append(span);
            }
    })
}

ajax_snp500();
ajax_get(0, 10);

$(document).ajaxStop(function () {
    select_country_btn.removeAttribute('disabled');
})

$('#select_country_btn').click(function(){
    $('.other_pattern').empty();
    $("tbody").empty();
    const title_html = `
        <td>Тикер</td>
        <td>Страна</td>
        <td>Капитализация</td>
        <td>Smart Score</td>
        <td>EMA10 Пересечение<img src="/static/screener/img/up.png"></td>
        <td>EMA10 Пересечение<img src="/static/screener/img/down.png"></td>
        <td>MACD Пересечение</td>
        <td>EMA10 <img src="/static/screener/img/up.png"></td>
        <td>EMA10 <img src="/static/screener/img/down.png"></td>
        <td>RSI <img src="/static/screener/img/up.png"></td>
        <td>RSI <img src="/static/screener/img/down.png"></td>
    `
    tr = document.createElement('tr');
    tr.className = 'title_table'
    tr.innerHTML = title_html;
    document.querySelector('tbody').append(tr);
    var x = 0;
    var y = 21;
    ajax_get(x, y);
    $(document).ajaxStop(function () {
        if ($("tbody").children().length <= 8){
            y = y + 20
            x = y - 20
            ajax_get(x, y);
        } else {
            select_country_btn.removeAttribute('disabled');

        }
    });
});

$(document).on('click', '.stock', function(){
    symbol = $(this).text();
    timeframe_selection = $('#timeframe_selection').val();
    if (timeframe_selection == '1d'){
        timeframe_selection = 'D';
    };
    if (timeframe_selection == '1W'){
        timeframe_selection = 'W';
    };
    if (timeframe_selection == '1M'){
        timeframe_selection = 'M';
    };
    if (timeframe_selection == '2h'){
        timeframe_selection = '120';
    };
    if (timeframe_selection == '3h'){
        timeframe_selection = '180';
    };
    if (timeframe_selection == '4h'){
        timeframe_selection = '240';
    };
    if (timeframe_selection == '30m'){
        timeframe_selection = '30';
    };
    if (timeframe_selection == '15m'){
        timeframe_selection = '15';
    };
    if (timeframe_selection == '5m'){
        timeframe_selection = '5';
    };
    if (timeframe_selection == '1h'){
        timeframe_selection = '60';
    };
    $.ajax({
        type: "GET",
        url: "/stock_view/",
        data: {'timeframe': timeframe_selection, 'symbol': symbol},
        dataType: 'json',
        cache: false,
        success: function(data){
            console.log('ok')
        }
    });
});


