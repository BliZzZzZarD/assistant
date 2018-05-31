(function () {
    'use strict';
    window.LayoutApartment = {};
    var self = window.LayoutApartment;
    self.top_menu_height = 0;
    self.Urls = {
        apartments: "/get_apartments/",
        city: "/get_cities/",
        district: "/get_districts",
        street: "/get_streets/",
        construction: "/get_constructions",
        apartmentGeo: "/get_apartment_geo/"
    };

    var estateHref = '/estate/apartments';

    function initViewEstate() {
        Layout.initColRowEstateView();

        //инициализация отображения по нажатию кнопки отображения
        var thEstate = $('.estate-th');
        var listEstate = $('.estate-list');

        thEstate.on('click', function () {
            if (!thEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 0);
                self.getApartmentEstate();
            }
        });

        listEstate.on('click', function () {
            if (!listEstate.hasClass('active')) {
                Utils.setCookie('colRowView', 1);
                self.getApartmentEstate();
            }
        });
    }

    function initFilterEstate() {
        Layout.initSelect();
        //загрузка городов
        getCity();
        //загрузка типа конструкции
        getConstructionEstate();
        //загрузка недвижимости
        self.getApartmentEstate();

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
        setFilterRadioButtonActive();
        setFilterInputValue();
    }

    function setFilterRadioButtonActive() {
        var btnRoomList = $('.switch-room').children();
        if ($.cookie('isRoom') !== undefined)
            btnRoomList[0].classList.add('active');
        else if ($.cookie('isFiveRoom') !== undefined)
            btnRoomList[btnRoomList.length - 1].classList.add('active');
        else if ($.cookie('countRoom') !== undefined)
            btnRoomList[$.cookie('countRoom')].classList.add('active');
        else {
            btnRoomList.removeClass('active');
        }
    }

    function setFilterInputValue() {
        Layout.setFilterInput($('#cost-from'), $.cookie('costMin'), false);
        Layout.setFilterInput($('#cost-to'), $.cookie('costMax'), false);
        Layout.setFilterInput($('#area-from'), $.cookie('areaMin'), false);
        Layout.setFilterInput($('#area-to'), $.cookie('areaMax'), false);
    }

    function initSortEstate() {
        Layout.initSortSelect();

        $('#sort-estate-select').on('change', function () {
            Utils.setCookie('orderField', this.value);
            self.getApartmentEstate();
        });
    }

    function getCity() {
        $.get(self.Urls.city, function (result) {
            if (result) {
                var citySelect = $("#city-select");
                citySelect.html(citySelect.html() + result);
                citySelect.selectpicker('refresh');
                if ($.cookie('city') !== undefined)
                    Layout.setFilterSelect(citySelect, $.cookie('city'));
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
                    if ($.cookie('district') !== undefined)
                        Layout.setFilterSelect(districtSelect, $.cookie('district'));
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
                    if ($.cookie('street') !== undefined)
                        Layout.setFilterSelect(streetSelect, $.cookie('street'));
                }
            }

        });
    }

    function getConstructionEstate() {
        $.get(self.Urls.construction, function (result) {
            if (result) {
                var construction = $("#construction-select");
                construction.html(construction.html() + result);
                construction.selectpicker('refresh');
                if ($.cookie('construction') !== undefined)
                    Layout.setFilterSelect(construction, $.cookie('construction').split(','));
            }
        });
    }

    //инициализация карты
    function initMapSet() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAE1_4eb436QOPwVKX-TpQDP6YpA9d0vY4&v=3.exp&' +
            'callback=LayoutApartment.initialize';
        document.body.appendChild(script);

        var scriptCluster = document.createElement('script');
        scriptCluster.type = 'text/javascript';
        scriptCluster.src =
            'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js';
        document.body.appendChild(scriptCluster);
    }

    self.findEstate = function () {
        var grpButRoom = $('.switch-room');
        if (grpButRoom.children().hasClass('active')) {
            var btnRoomList = grpButRoom.children();
            if (btnRoomList[0].classList.contains('active')) {
                Utils.setCookie('isRoom', 1);
                Utils.removeCookie('countRoom');
                Utils.removeCookie('isFiveRoom');
            } else if (btnRoomList[btnRoomList.length - 1].classList.contains('active')) {
                Utils.removeCookie('isRoom');
                Utils.removeCookie('countRoom');
                Utils.setCookie('isFiveRoom', 1);
            } else {
                Utils.removeCookie('isRoom');
                Utils.setCookie('countRoom', btnRoomList.filter(function (index, item) {
                    return item.classList.contains('active');
                }).children('input')[0].dataset.type);
                $.removeCookie('isFiveRoom');
            }
        } else {
            Utils.removeCookie('isRoom');
            Utils.removeCookie('countRoom');
            Utils.removeCookie('isFiveRoom');
        }

        Utils.setCookie('city', $('#city-select').val());
        Utils.setCookie('district', $('#district-select').val());
        Utils.setCookie('street', $('#street-select').val());
        Utils.setCookie('costMin', $('#cost-from').val());
        Utils.setCookie('costMax', $('#cost-to').val());
        Utils.setCookie('areaMin', $('#area-from').val());
        Utils.setCookie('areaMax', $('#area-to').val());
        Utils.setCookie('construction', $('#construction-select').val().toString());

        self.getApartmentEstate();
    };

    self.getApartmentEstate = function (page) {
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
            isRoom: $.cookie('isRoom'),
            countRoom: $.cookie('countRoom'),
            isFiveRoom: $.cookie('isFiveRoom'),
            city: $.cookie('city'),
            district: $.cookie('district'),
            street: $.cookie('street'),
            costMin: $.cookie('costMin'),
            costMax: $.cookie('costMax'),
            areaMin: $.cookie('areaMin'),
            areaMax: $.cookie('areaMax'),
            construction: $.cookie('construction')
        };

        blockUI();

        $.get(self.Urls.apartments, params).done(function (result) {
            if (result) {
                $("#estates").html(result);
                var pagination = $('.pagination-div');
                if (pagination.length !== 0) {
                    var pageEstate = pagination[0].dataset.currentPage;
                    Utils.setCookie('page', pageEstate);
                    Utils.setLocation(result, 'apartment', estateHref + '?page=' + pageEstate);
                } else {
                    Utils.setLocation(result, 'apartment', estateHref);
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

        setFilterRadioButtonActive();
        setFilterInputValue();
        self.getApartmentEstate();
    };

    self.removeAllCookie = function () {
        Utils.removeCookie('isRoom');
        Utils.removeCookie('countRoom');
        Utils.removeCookie('isFiveRoom');
        Utils.removeCookie('city');
        Utils.removeCookie('district');
        Utils.removeCookie('street');
        Utils.removeCookie('costMin');
        Utils.removeCookie('costMax');
        Utils.removeCookie('areaMin');
        Utils.removeCookie('areaMax');
        Utils.removeCookie('construction');
    };

    self.showApartmentByRoom = function (isRoom, countRoom, isFiveRoom) {
        self.removeAllCookie();
        if (isRoom !== null) {
            Utils.setCookie('isRoom', 1);
        } else if (isFiveRoom !== null) {
            Utils.setCookie('isFiveRoom', 1);
        } else {
            Utils.setCookie('countRoom', countRoom);
        }

        location.href = "/estate/apartments/";
    };

    self.showApartments = function () {
        self.removeAllCookie();
        location.href = "/estate/apartments/";
    };

    self.initialize = function () {
        var geolocation;
        var mapOptions = {
            zoom: 11,
            center: {lat: 51.662, lng: 39.202}
        };

        var map = new google.maps.Map(document.getElementById('map-category-estate-canvas'), mapOptions);
        $.ajax({
            url: self.Urls.apartmentGeo
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
