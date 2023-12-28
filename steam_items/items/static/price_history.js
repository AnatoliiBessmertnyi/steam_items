window.addEventListener('load', function() {
    var itemId = document.querySelector('h1').dataset.itemId;
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Цена',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                fill: false
            }]
        },
        options: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: {
                            day: 'd/M/y H:mm'
                        }
                    }
                }
        }
    });

    $.getJSON("/price_history_json/" + itemId + "/")
    .done(function(data) {
        chart.data.labels = data.map(function(record) { return record.time; });
        chart.data.datasets[0].data = data.map(function(record) { return record.price; });
        chart.update();
    })
    .fail(function() {
        console.log("Ошибка при загрузке данных истории цен.");
    });
});
