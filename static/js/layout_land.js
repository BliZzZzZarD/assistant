(function () {
    'use strict';
    window.LayoutLand = {};
    var self = window.LayoutLand;
    self.top_menu_height = 0;
    self.Urls = {
        lands: "/get_lands/",
        city: "/get_cities/",
        appointment: "/get_land_appointment",
        landGeo: "/get_land_geo/"
    };

    var estateHref = '/estate/lands';

    function initViewEstate() {
        Layout.initColRowEstateView();

        //инициализация отображения по нажатию кнопки отображения
        var thEstate = $('.estate-th');
        var listEstate = $('.estate-list');

        thEstate.on('click', function () {
            if (!thEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 0);
                self.getLandEstate();
            }
        });

        listEstate.on('click', function () {
            if (!listEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 1);
                self.getLandEstate();
            }
        });
    }

    function initFilterEstate() {
        Layout.initSelect();
        //загрузка населенных пунктов
        getCity();
        //загрузка типов назначений земельных участков
        getAppointmentLand();
        //загрузка недвижимости
        self.getLandEstate();

        setFilterInputValue();
    }

    function setFilterInputValue() {
        Layout.setFilterInput($('#cost-from'), $.cookie('costLandMin'), false);
        Layout.setFilterInput($('#cost-to'), $.cookie('costLandMax'), false);
        Layout.setFilterInput($('#area-from'), $.cookie('areaLandMin'), false);
        Layout.setFilterInput($('#area-to'), $.cookie('areaLandMax'), false);
    }

    function initSortEstate() {
        Layout.initSortSelect();

        $('#sort-estate-select').on('change', function () {
            Utils.setCookie('orderLandField', this.value);
            self.getLandEstate();
        });
    }

    function getCity() {
        $.get(self.Urls.city, function (result) {
            if (result) {
                var citySelect = $("#city-select");
                citySelect.html(citySelect.html() + result);
                citySelect.selectpicker('refresh');
                if ($.cookie('cityLand') !== undefined)
                    Layout.setFilterSelect(citySelect, $.cookie('cityLand'));
            }
        });
    }

    function getAppointmentLand() {
        $.get(self.Urls.appointment, function (result) {
            if (result) {
                var appointment = $("#appointment-select");
                appointment.html(appointment.html() + result);
                appointment.selectpicker('refresh');
                if ($.cookie('appointmentLand') !== undefined)
                    Layout.setFilterSelect(appointment, $.cookie('appointmentLand').split(','));
            }
        });
    }

    //инициализация карты
    function initMapSet() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAE1_4eb436QOPwVKX-TpQDP6YpA9d0vY4&v=3.exp&' +
            'callback=LayoutLand.initialize';
        document.body.appendChild(script);

        var scriptCluster = document.createElement('script');
        scriptCluster.type = 'text/javascript';
        scriptCluster.src = 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js';
        document.body.appendChild(scriptCluster);
    }

    self.findEstate = function () {
        Utils.setCookie('cityLand', $('#city-select').val());
        Utils.setCookie('costLandMin', $('#cost-from').val());
        Utils.setCookie('costLandMax', $('#cost-to').val());
        Utils.setCookie('areaLandMin', $('#area-from').val());
        Utils.setCookie('areaLandMax', $('#area-to').val());
        Utils.setCookie('appointmentLand', $('#appointment-select').val().toString());

        self.getLandEstate();
    };

    self.getLandEstate = function (page) {
        if (page !== undefined) {
            Utils.setCookie('page', page);
        } else {
            if ($.cookie('page') !== undefined) {
                page = $.cookie('page');
            } else {
                page = Utils.getUrlParams('page');
                if (page === undefined) {
                    page = 1;
                }
            }
        }

        var params = {
            page: page,
            orderField: $.cookie('orderLandField'),
            colRowView: $.cookie('colRowView'),
            city: $.cookie('cityLand'),
            costMin: $.cookie('costLandMin'),
            costMax: $.cookie('costLandMax'),
            areaMin: $.cookie('areaLandMin'),
            areaMax: $.cookie('areaLandMax'),
            appointmentLand: $.cookie('appointmentLand')
        };

        blockUI();

        $.get(self.Urls.lands, params).done(function (result) {
            if (result) {
                $("#estates").html(result);
                var pagination = $('.pagination-div');
                if (pagination.length !== 0) {
                    var pageEstate = pagination[0].dataset.currentPage;
                    Utils.setCookie('page', pageEstate);
                    Utils.setLocation(result, 'land', estateHref + '?page=' + pageEstate);
                } else {
                    Utils.setLocation(result, 'land', estateHref);
                }
            } else {
                Layout.setErrorInEstateBlock();
            }
            unblockUI();
        }).fail(function () {
            Layout.setErrorInEstateBlock();
            unblockUI();
        });
    };

    self.trashFilter = function () {
        self.removeAllCookie();

        var citySelect = $("#city-select");
        Layout.setFilterSelect(citySelect, '');

        var appointmentLand = $("#appointment-select");
        Layout.setFilterSelect(appointmentLand, '');

        setFilterInputValue();
        self.getLandEstate();
    };

    self.removeAllCookie = function () {
        Utils.removeCookie('cityLand');
        Utils.removeCookie('costLandMin');
        Utils.removeCookie('costLandMax');
        Utils.removeCookie('areaLandMin');
        Utils.removeCookie('areaLandMax');
        Utils.removeCookie('appointmentLand');
    };

    self.showLandByAppointment = function (appointmentLand) {
        self.removeAllCookie();
        Utils.setCookie('appointmentLand', appointmentLand);
        location.href = "/estate/lands/";
    };

    self.showLands = function () {
        self.removeAllCookie();
        location.href = "/estate/lands/";
    };

    self.initialize = function () {
        var geolocation;
        var mapOptions = {
            zoom: 11,
            center: {lat: 51.662, lng: 39.202}
        };

        var map = new google.maps.Map(document.getElementById('map-category-estate-canvas'), mapOptions);
        $.ajax({
            url: self.Urls.landGeo
        }).done(function (result) {
            if (result) {
                var geoList = result.data.result;
                var gPoints = geoList.map(function (value) {
                    geolocation = value.geo.split(',');
                    return new google.maps.Marker({
                        position: {
                            lat: parseFloat(geolocation[0]),
                            lng: parseFloat(geolocation[1])
                        },
                        map: map,
                        label: {
                            fontWeight: 'bold',
                            fontSize: 'small',
                            text: value.count.toString()
                        },
                        objects: value.objects,
                        icon: {
                            url: "/static/images/estates/flag.png",
                            scaledSize: new google.maps.Size(40, 40)
                        }
                    });
                });

                gPoints.forEach(function (value) {
                    google.maps.event.addListener(value, 'click', function () {
                        var infowindow = new google.maps.InfoWindow({
                            content: Layout.getContentForInfoWindow(this.objects)
                        });
                        infowindow.open(map, this);
                    });
                });

                var markerCluster = new MarkerClusterer(map, gPoints,
                    {
                        imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
                    });
            }
        });
    };

    self.init = function () {
        initViewEstate();
        initFilterEstate();
        initSortEstate();
        initMapSet();
    };
})();
