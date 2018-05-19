
$(function() {

    var time = $('#time p');
    var power = $('#power p');
    var toogle_one = $('#toggle-one');


    //////////////// Communication with BACK-END /////////////////
    var id = setInterval(function () {
        console.log('jestem wywoływana co sekundę');

        $.ajax({
            url: 'http://127.0.0.1:8000/microwave/status/1',
            type: 'GET',
            dataType: 'json'
         }).done(function (result) {
            time.text(result.TTL);
            power.text(result.Power);

            if (result.TTL > 0) {
                $(function() {
                    toogle_one.bootstrapToggle('on');
                })
            } else {
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

        if (parseInt(actual_time) === 1000){
            alert('Max power cant be lower')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'POST',
                data: {
                    "On": true,
                    "TTL": 44,
                    "Power": 600
                }
            }).done(function (result) {
                alert('PATCH	completed');
            }).fail(function () {
                alert("nie udało się");
            })
        }
    });

     /////////////// T- (timer -10s) event //////////////////////
    $("button#T-").on("click", function (){

        var actual_time = time.text();

        if (parseInt(actual_time) === 100 || parseInt(actual_time) === 0){
            alert('Max power cant be lower')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/microwave/event',
                type: 'PUT',
                dataType: "json",
                data: 'On=True&TTL=20&Power=500'
                // data: {
                //         "On": true,
                //         "TTL": 34,
                //         "Power": 600
                //     }
            }).done(function (result) {
                alert('PATCH	completed');
            }).fail(function () {
                alert('Something went wrong');
                alert(actual_power);
            })
        }
    });

     /////////////// P+ (power +100W) event //////////////////////
	$("button#Pplus").on("click", function () {

        var actual_power = power.text();

        if (parseInt(actual_power) === 1000){
            alert('Max power cant be lower')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": 44,
                    "Power": 700
                }
            }).done(function (result) {
                alert('PATCH	completed');
            }).fail(function () {
                alert("nie udało się");
            })
        }
    });

     /////////////// P- (timer -100W) event //////////////////////
	$("button#P-").on("click", function () {

        var actual_power = power.text();

        if (parseInt(actual_power) === 100 || parseInt(actual_power) === 0){
            alert('Max power cant be lower')
        }else {
            $.ajax({
                url: 'http://127.0.0.1:8000/store/',
                type: 'PUT',
                data: {
                    "On": true,
                    "TTL": 44,
                    "Power": 100
                }
            }).done(function (result) {
                alert('PATCH	completed');
            }).fail(function () {
                alert("nie udało się");
            })
        }
    });

	 /////////////// C (stop microwave) event //////////////////////
    $("button#C").on("click", function () {
        $.ajax({
            url: 'http://127.0.0.1:8000/store/',
            type: 'PUT',
                data: {
                    "On": false,
                    "TTL": 0,
                    "Power": 0
                }
        }).done(function (result) {
            alert('Microwave Stopped');
        }).fail(function () {
            alert('Something went wrong');
        })
    });


});