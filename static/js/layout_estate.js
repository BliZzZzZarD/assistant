(function () {
    'use strict';
    window.LayoutEstate = {};
    var self = window.LayoutEstate;

    function initGallery() {
        $( '#gallery' ).jGallery({ backgroundColor: '#f4faff', textColor: '#244971' });
    }

    //инициализация карты
    function initMapSet() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAE1_4eb436QOPwVKX-TpQDP6YpA9d0vY4&v=3.exp&' +
            'callback=LayoutEstate.initialize';
        document.body.appendChild(script);

        var scriptCluster = document.createElement('script');
        scriptCluster.type = 'text/javascript';
        scriptCluster.src =
            'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js';
        document.body.appendChild(scriptCluster);
    }

    self.initialize = function () {
        var geo = {};
        var mapOptions = {
            zoom: 17,
            center: geo
        };

        var geolocation = $('#map-estate-canvas').attr('data-geolocation');
        if (geolocation !== null && geolocation !== undefined && geolocation !== '') {
            geolocation = geolocation.split(',');
            geo.lat = parseFloat(geolocation[0]);
            geo.lng = parseFloat(geolocation[1]);
        }

        var map = new google.maps.Map(document.getElementById('map-estate-canvas'), mapOptions);
        var marker = new google.maps.Marker({
            position: geo,
            map: map,
            icon: {
                url: "/static/images/estates/flag2.png",
                scaledSize: new google.maps.Size(40, 40)
            }
        });
    };

    self.init = function () {
        initGallery();
        initMapSet();
    };
})();
