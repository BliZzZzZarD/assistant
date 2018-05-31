(function () {
    'use strict';
    window.LayoutCommerce = {};
    var self = window.LayoutCommerce;
    self.top_menu_height = 0;
    self.Urls = {
        commerces: "/get_commerces/",
        city: "/get_cities/",
        district: "/get_districts",
        street: "/get_streets/",
        constructionCommerce: "/get_commerce_constructions",
        appointment: "/get_appointments",
        commerceGeo: "/get_commerce_geo/"
    };

    var estateHref = '/estate/commerces';

    function initViewEstate() {
        Layout.initColRowEstateView();

        //инициализация отображения по нажатию кнопки отображения
        var thEstate = $('.estate-th');
        var listEstate = $('.estate-list');

        thEstate.on('click', function () {
            if (!thEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 0);
                self.getCommerceEstate();
            }
        });

        listEstate.on('click', function () {
            if (!listEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 1);
                self.getCommerceEstate();
            }
        });
    }

    function initFilterEstate() {
        Layout.initSelect();
        //загрузка городов
        getCity();
        //загрузка типа конструкции
        getConstructionEstate();
        //загрузка типа конструкции
        getAppointment();
        //загрузка недвижимости
        self.getCommerceEstate();

        $("#city-select").on('change', function () {
            var cityValue = this.value;
            if (cityValue !== "") {
                getDistrict(cityValue);
                getStreet(cityValue);
            } else {
                Layout.cleanOptions($("#street-select"), true);
                Layout.cleanOptions($("#district-select"), true);
            }
        });

        $("#district-select").on('change', function () {
            var districtValue = this.value;
            var cityValue = $("#city-select").val();
            if (districtValue !== "") {
                Layout.cleanOptions($("#street-select"), false);
                getStreet(cityValue, districtValue);
            } else {
                Layout.cleanOptions($("#street-select"), false);
                getStreet(cityValue);
            }
        });

        //инициализация отображения активных значений фильтра
        setFilterInputValue();
    }

    function setFilterInputValue() {
        Layout.setFilterInput($('#cost-from'), $.cookie('costCommerceMin'), false);
        Layout.setFilterInput($('#cost-to'), $.cookie('costCommerceMax'), false);
        Layout.setFilterInput($('#area-from'), $.cookie('areaCommerceMin'), false);
        Layout.setFilterInput($('#area-to'), $.cookie('areaCommerceMax'), false);
    }

    function initSortEstate() {
        Layout.initSortSelect();

        $('#sort-estate-select').on('change', function () {
            Utils.setCookie('orderField', this.value);
            self.getCommerceEstate();
        });
    }

    function getCity() {
        $.get(self.Urls.city, function (result) {
            if (result) {
                var citySelect = $("#city-select");
                citySelect.html(citySelect.html() + result);
                citySelect.selectpicker('refresh');
                if ($.cookie('cityCommerce') !== undefined)
                    Layout.setFilterSelect(citySelect, $.cookie('cityCommerce'));
                if (citySelect.val() !== "")
                    citySelect.trigger('change');
            }
        });
    }

    function getDistrict(cityValue) {
        $.get(self.Urls.district, {cityValue: cityValue}, function (result) {
            if (result) {
                var districtSelect = $("#district-select");
                districtSelect.html(districtSelect.html() + result);

                if (districtSelect.children().length > 1) {
                    districtSelect.prop('disabled', false);
                    districtSelect.selectpicker('refresh');
                    if ($.cookie('districtCommerce') !== undefined)
                        Layout.setFilterSelect(districtSelect, $.cookie('districtCommerce'));
                    if (districtSelect.val() !== "")
                        districtSelect.trigger('change');
                }
            }
        });
    }

    function getStreet(cityValue, districtValue) {
        var params = {
            cityValue: cityValue,
            districtValue: districtValue !== undefined ? districtValue : null
        };

        $.get(self.Urls.street, params, function (result) {
            if (result) {
                var streetSelect = $("#street-select");
                streetSelect.html(streetSelect.html() + result);
                if (streetSelect.children().length > 1) {
                    streetSelect.prop('disabled', false);
                    streetSelect.selectpicker('refresh');
                    if ($.cookie('streetCommerce') !== undefined)
                        Layout.setFilterSelect(streetSelect, $.cookie('streetCommerce'));
                }
            }

        });
    }

    function getConstructionEstate() {
        $.get(self.Urls.constructionCommerce, function (result) {
            if (result) {
                var construction = $("#construction-select");
                construction.html(construction.html() + result);
                construction.selectpicker('refresh');
                if ($.cookie('constructionCommerce') !== undefined)
                    Layout.setFilterSelect(construction, $.cookie('construction').split(','));
            }
        });
    }

    function getAppointment() {
        $.get(self.Urls.appointment, function (result) {
            if (result) {
                var construction = $("#appointment-select");
                construction.html(construction.html() + result);
                construction.selectpicker('refresh');
                if ($.cookie('appointment') !== undefined)
                    Layout.setFilterSelect(construction, $.cookie('appointment').split(','));
            }
        });
    }

    //инициализация карты
    function initMapSet() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAE1_4eb436QOPwVKX-TpQDP6YpA9d0vY4&v=3.exp&' +
            'callback=LayoutCommerce.initialize';
        document.body.appendChild(script);

        var scriptCluster = document.createElement('script');
        scriptCluster.type = 'text/javascript';
        scriptCluster.src =
            'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js';
        document.body.appendChild(scriptCluster);
    }

    self.findEstate = function () {

        Utils.setCookie('cityCommerce', $('#city-select').val());
        Utils.setCookie('districtCommerce', $('#district-select').val());
        Utils.setCookie('streetCommerce', $('#street-select').val());
        Utils.setCookie('costCommerceMin', $('#cost-from').val());
        Utils.setCookie('costCommerceMax', $('#cost-to').val());
        Utils.setCookie('areaCommerceMin', $('#area-from').val());
        Utils.setCookie('areaCommerceMax', $('#area-to').val());
        Utils.setCookie('appointment', $('#appointment-select').val().toString());
        Utils.setCookie('constructionCommerce', $('#construction-select').val().toString());

        self.getCommerceEstate();
    };

    self.getCommerceEstate = function (page) {
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
            orderField: $.cookie('orderField'),
            colRowView: $.cookie('colRowView'),
            city: $.cookie('cityCommerce'),
            district: $.cookie('districtCommerce'),
            street: $.cookie('streetCommerce'),
            costMin: $.cookie('costCommerceMin'),
            costMax: $.cookie('costCommerceMax'),
            areaMin: $.cookie('areaCommerceMin'),
            areaMax: $.cookie('areaCommerceMax'),
            appointment: $.cookie('appointment'),
            construction: $.cookie('constructionCommerce')
        };

        blockUI();

        $.get(self.Urls.commerces, params).done(function (result) {
            if (result) {
                $("#estates").html(result);
                var pagination = $('.pagination-div');
                if (pagination.length !== 0) {
                    var pageEstate = pagination[0].dataset.currentPage;
                    Utils.setCookie('page', pageEstate);
                    Utils.setLocation(result, 'commerce', estateHref + '?page=' + pageEstate);
                } else {
                    Utils.setLocation(result, 'commerce', estateHref);
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
        citySelect.trigger('change');

        var constructionSelect = $("#construction-select");
        Layout.setFilterSelect(constructionSelect, '');

        var appointmentSelect = $("#appointment-select");
        Layout.setFilterSelect(appointmentSelect, '');

        setFilterInputValue();
        self.getCommerceEstate();
    };

    self.removeAllCookie = function () {
        Utils.removeCookie('cityCommerce');
        Utils.removeCookie('districtCommerce');
        Utils.removeCookie('streetCommerce');
        Utils.removeCookie('costCommerceMin');
        Utils.removeCookie('costCommerceMax');
        Utils.removeCookie('areaCommerceMin');
        Utils.removeCookie('areaCommerceMax');
        Utils.removeCookie('appointment');
        Utils.removeCookie('constructionCommerce');
    };

    self.showCommerceByAppointment = function (appointment) {
        self.removeAllCookie();
        Utils.setCookie('appointment', appointment);
        location.href = "/estate/commerces/";
    };

    self.showCommerces = function () {
        self.removeAllCookie();
        location.href = "/estate/commerces/";
    };

    self.initialize = function () {
        var geolocation;
        var mapOptions = {
            zoom: 11,
            center: {lat: 51.662, lng: 39.202}
        };

        var map = new google.maps.Map(document.getElementById('map-category-estate-canvas'), mapOptions);
        $.ajax({
            url: self.Urls.commerceGeo
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
                        address: value.address_show,
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
                            content: Layout.getContentForInfoWindow(this.objects, this.address)
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
