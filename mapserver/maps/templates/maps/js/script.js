function initMap() {

    alert("Hello");

    var myLatLng = [{
        lat: -26.363,
        lng: 132.044
    }, {
        lat: -27.363,
        lng: 131.044
    }];
    arrayLength = myLatLng.length;

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {
             lat: -27.363,
            lng: 131.044
        }
    });

    var markers = [];
    for (var i = 0; i < arrayLength; i++)
        markers.push(new google.maps.Marker({
            position: myLatLng[i],
            map: map,
            title: 'Hello World!'
        }));
} 