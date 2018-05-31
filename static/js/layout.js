(function () {
    'use strict';
    window.Layout = {};
    var self = window.Layout;
    self.top_menu_height = 0;
    self.Urls = {
        configuration: "/configuration/"
    };

    //инициализация активной ссылки в nav-bar
    function initNavBarActive() {
        var url = document.location.toString();
        $("ul.nav.navbar-nav.navbar-right > li").each(function () {
            if (!$(this).find('a.nav-a')[0].href.endsWith('/')) $(this).find('a.nav-a')[0].href += '/';
        }).filter(function () {
            return url === $(this).find('a.nav-a')[0].href;
        }).addClass("active");
    }

    //инициализация nav-estate-catalog
    function initNavEstateCatalog() {
        var b = $(".nav-a").children('.caret');
        var menu = $(".dropdown-menu-container");
        if (window.innerWidth < 753) {
            b.hide();
            menu.addClass('hide');
        } else {
            b.show();
            menu.removeClass('hide');
        }
    }

    //изменение размеров окна браузера
    function initResize() {
        $(window).resize(function () {
            initNavEstateCatalog();
        });
    }

    //изменение переключения button type radio
    function initSwitchButton() {
        $('[data-toggle="switch-buttons"]').children().on('click', function (e) {
            e.preventDefault();
            var element = $(this);
            var parent = element.parent();
            var input = element.children();
            if (element.hasClass('active')) {
                element.removeClass('active');
            } else {
                parent.find('.active').removeClass('active');
                element.addClass('active')
            }
            input.prop('checked', element.hasClass('active'));
            input.trigger('change');
        });
    }

    //инициализация tab элементов
    function initEstateTab() {
        $("#estateTab").find("a").click(function (e) {
            e.preventDefault();
            $(this).tab('show');
        });
    }

    function initStickUp() {
        $('.templatemo-top-menu').stickUp({
            scrollHide: true
        });
    }

    function initScrollUp() {
        self.top_menu_height = $('.templatemo-top-menu').height();
        $('#btn-back-to-top').click(function (e) {
            e.preventDefault();
            var selector_top = $('#templatemo-top').offset().top - self.top_menu_height;
            $('html,body').animate({scrollTop: selector_top}, 'slow');
        });
    }

    //инициализация настроек
    function initConfig() {
        var phone = $('.phone'),
            email = $('#email').find('> p');

        $.ajax({
            url: self.Urls.configuration
        }).done(function (result) {
            if (result) {
                var config = jQuery.parseJSON(result.data)[0];
                if (config !== undefined) {
                    config = config.fields;
                    phone.html(phone.html() + " " + config.phone);
                    email.html(email.html() + " " + config.email);
                    if (config.isVk) {
                        $('li#vk > a').attr('href', config.vk);
                    } else {
                        $('li#vk').hide();
                    }

                    if (config.isFb) {
                        $('li#fb > a').attr('href', config.fb);
                    } else {
                        $('li#fb').hide();
                    }
                }
            }
        });
    }

    //инициализация select-bootstrap
    self.initSelect = function () {
        $('.selectpicker').selectpicker({
            size: 4
        });

        var switchSelect = $(".dependent-select");
        switchSelect.prop('disabled', true);
        switchSelect.selectpicker('refresh');
    };

    //инициализация типа сортировки
    self.initSortSelect = function () {
        var sortEstate = $('#sort-estate-select');
        var sortValue = $.cookie('orderField') !== undefined ? $.cookie('orderField') : 0;
        Layout.setFilterSelect(sortEstate, sortValue);
    };

    //установка значений фильтра для select
    self.setFilterSelect = function (selector, value) {
        if (value !== undefined) {
            selector.selectpicker('val', value);
        }
    };

    //очистка options для select-bootstrap
    self.cleanOptions = function (select, isDisableSelect) {
        select.html('<option value="">Не выбрано</option>');
        select.val(0);

        if (isDisableSelect) {
            select.prop('disabled', true);
            select.selectpicker('refresh');
        }

    };

    //установка значений фильтра для input
    self.setFilterInput = function (selector, value) {
        if (value !== undefined) {
            selector.val(Utils.getNumberFormat(value, 2));
        } else {
            selector.val('');
        }
    };

    //страница вперед/назад
    self.pageNextPrevious = function (page) {
        var typeEstate = $('.pagination-div')[0].dataset['estateType'];
        if (typeEstate === 'apartments') {
            LayoutApartment.getApartmentEstate(page);
        } else if (typeEstate === 'residences') {
            LayoutResidence.getResidenceEstate(page);
        } else if (typeEstate === 'commerces') {
            LayoutCommerce.getCommerceEstate(page);
        } else if (typeEstate === 'lands') {
            LayoutLand.getLandEstate(page);
        }
    };

    //поиск с главной страницы
    self.findEstate = function () {
        var typeEstate = $('#estate-type-select').val();
        var costFrom = $('#cost-from').val();
        var costTo = $('#cost-to').val();

        if (typeEstate === '0') {
            LayoutApartment.removeAllCookie();

            Utils.setCookie('costMin', costFrom);
            Utils.setCookie('costMax', costTo);

            location.href = "/estate/apartments/";
        } else if (typeEstate === '1') {
            LayoutResidence.removeAllCookie();

            Utils.setCookie('costResidenceMin', costFrom);
            Utils.setCookie('costResidenceMax', costTo);

            location.href = "/estate/residences/";
        } else if (typeEstate === '2') {
            LayoutCommerce.removeAllCookie();

            Utils.setCookie('costCommerceMin', costFrom);
            Utils.setCookie('costCommerceMax', costTo);

            location.href = "/estate/commerces/";
        } else if (typeEstate === '3') {
            LayoutLand.removeAllCookie();

            Utils.setCookie('costLandMin', costFrom);
            Utils.setCookie('costLandMax', costTo);

            location.href = "/estate/lands/";
        }
    };

    //поиск по адресной навигации
    self.findEstateByAddress = function (typeEstate, city, street) {
        if (typeEstate === 'apartments') {
            LayoutApartment.removeAllCookie();

            Utils.setCookie('city', city);
            Utils.setCookie('street', street);

            location.href = "/estate/apartments/";
        } else if (typeEstate === 'residences') {
            LayoutResidence.removeAllCookie();

            Utils.setCookie('cityResidence', city);
            Utils.setCookie('streetResidence', street);

            location.href = "/estate/residences/";
        } else if (typeEstate === 'commerces') {
            LayoutCommerce.removeAllCookie();

            Utils.setCookie('cityCommerce', city);
            Utils.setCookie('streetCommerce', street);

            location.href = "/estate/commerces/";
        } else if (typeEstate === 'lands') {
            LayoutLand.removeAllCookie();

            Utils.setCookie('cityLand', city);

            location.href = "/estate/lands/";
        }
    };

    self.findEstateByArticle = function (input, event) {
        if (event.keyCode === 13) {
            var article = input.value;
            if (article !== undefined && article !== '')
                location.href = '/estate/find_by_article/' + input.value;
        }
    };

    //обработка ошибки при возвращении данных о недвижимости
    self.setErrorInEstateBlock = function () {
        var errorBlock =
            "<div class=\"row margin-t-15 margin-b-20 margin-l-5\">\n" +
            "<p>При обработке данных произошла ошибка</p>\n</div>";
        $("#estates").html(errorBlock);
    };

    //содержимое информационного окна маркера карты
    self.getContentForInfoWindow = function (objects, address) {
        var result = "";
        if (address !== undefined)
            result = "<h6 class='caption-info-geo'>" + address + "</h6></br>";
        objects.forEach(function (value) {
            var url = "/estate/" + value.slug;
            result += "<a class='info-geo' href=" + url + ">" + value.caption + "</a></br>"
        });

        return result;
    };

    //инициализация активной кнопки вид "колонка/строка"
    self.initColRowEstateView = function () {
        var thEstate = $('.estate-th');
        var listEstate = $('.estate-list');

        //инициализация кнопок типа отображения
        var colRowView = $.cookie('colRowView');
        if (colRowView === "1") {
            thEstate.removeClass('active');
            listEstate.addClass('active');
        } else {
            thEstate.addClass('active');
            listEstate.removeClass('active');
        }
    };

    self.init = function () {
        initNavBarActive();
        initNavEstateCatalog();
        initResize();
        initSwitchButton();
        initEstateTab();
        initScrollUp();
        initConfig();
        initStickUp();
    };

})();

$(document).ready(function () {
    Layout.init();
    $(window).on('beforeunload', function () {
        Utils.removeCookie('page');
    });
});



