$(function() {

    var time = $('#time p');
    var power = $('#power p');
    var toogle_one = $('#toggle-one');


    //////////////// Communication with BACK-END every second /////////////////
    var id = setInterval(function () {
        console.log('jestem wywoływana co sekundę');
        $.ajax({
            url: 'http://127.0.0.1:8000/store/cache',
            type: 'GET',
            dataType: 'json'
         }).done(function (result) {
            time.text(result.TTL);
            power.text(result.Power);

            if (result.TTL > 0) {
                $(function() {
                    toogle_one.bootstrapToggle('on');
                });
                $.ajax({
                    url: 'http://127.0.0.1:8000/microwave/status/1',
                    type: 'PUT',
                    data: {
                    "On": true,
                    "TTL": result.TTL, //add +10s (but how?)
                    "Power": result.Power
                    }
                 }).done()
            }else {
                 $(function() {
                    toogle_one.bootstrapToggle('off');
                })
            }
        });
        }, 1000
    );


    /////////////// T+ (timer +10s) event //////////////////////
    $("button#Tplus").on("click", function () {

        var actual_time = time.text();
        var actual_power = power.text();

        if (parseInt(actual_time) === 99) {
            alert('This is maximal time');

        }else if (parseInt(actual_time) >= 90 && parseInt(actual_time) <= 99 ){
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": 99,
                    "Power": actual_power
                }
            }).done(function (result) {
                console.log('Put completed')
            }).fail(function () {
                alert('Something went wrong');
            })

        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": parseInt(actual_time) +10,
                    "Power": actual_power
                }
            }).done(function (result) {
                console.log('Put completed');
            }).fail(function () {
                alert('Something went wrong');
            })
        }
    });

     /////////////// T- (timer -10s) event //////////////////////
    $("button#T-").on("click", function (){

        var actual_time = time.text();
        var actual_power = power.text();

        if (parseInt(actual_time) === 0){
            alert('Time can\'t be negative');

        }else if (parseInt(actual_time) >=1 && parseInt(actual_time) <=9) {
             $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                        "On": true,
                        "TTL": 0,
                        "Power": actual_power
                    }
            }).done(function () {
                console.log('Put completed');
            }).fail(function () {
                alert('Something went wrong');
            })

        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                        "On": true,
                        "TTL": parseInt(actual_time) - 10,
                        "Power": actual_power
                    }
            }).done(function () {
                console.log('Put completed');
            }).fail(function () {
                alert('Something went wrong');
            })
        }
    });

     /////////////// P+ (power +100W) event //////////////////////
	$("button#Pplus").on("click", function () {

        var actual_time = time.text();
        var actual_power = power.text();

        if (parseInt(actual_power) === 1000){
            alert('Max power is 1kW')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": actual_time,
                    "Power": parseInt(actual_power)+100
                }
            }).done(function () {
                console.log('PUT completed');
            }).fail(function () {
                alert('Something went wrong');
            })
        }
    });

     /////////////// P- (timer -100W) event //////////////////////
	$("button#P-").on("click", function () {

        var actual_time = time.text();
        var actual_power = power.text();

        if (parseInt(actual_power) === 100){
            alert('Power can\'t be lower')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": actual_time,
                    "Power": parseInt(actual_power)-100
                }
            }).done(function () {
                console.log('PUT completed');
            }).fail(function () {
                alert('Something went wrong');
            })
        }
    });

	 /////////////// C (stop microwave) event //////////////////////
    $("button#C").on("click", function () {

        var actual_time = time.text();

        if (parseInt(actual_time) ===0){
            alert('Microwave already stopped')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": false,
                    "TTL": 0,
                    "Power": 100
                }
            }).done(function () {
                alert('Microwave Stopped');
            }).fail(function () {
                alert('Something went wrong');
            })
        }
    });


});