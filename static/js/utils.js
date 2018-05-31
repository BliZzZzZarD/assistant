String.prototype.replaceAll = function (search, replace) {
    return this.split(search).join(replace);
};

(function () {
    'use strict';
    window.Utils = {};
    var self = window.Utils;

    self.setLocation = function (object, title, curLoc) {
        try {
            history.pushState(object, title, curLoc);
        } catch (e) {
            location.hash = '#' + curLoc;
        }
    };

    self.getUrlParams = function (name) {
        var params = {};
        window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
            params[key] = value;
        });
        return params[name];
    };

    self.setCookie = function (name, value) {
        if (value !== "" && value !== null && value !== undefined) {
            $.cookie(name, value.toString().replaceAll(' ', ''), {path:'/'});
        } else {
            $.removeCookie(name, {path:'/'});
        }
    };

    self.removeCookie = function (name)  {
        $.removeCookie(name, {path:'/'});
    };

    self.formatValueInput = function (field, dec) {
        var fieldInput = $(field);
        var value = fieldInput.val();
        if (value !== '') {
            fieldInput.val(self.getNumberFormat(value, dec));
        }
    };

    self.getNumberFormat = function (value, dec) {
        value = value.replace('-', '');
        var arrayVal = value.split('.');
        arrayVal[0] = arrayVal[0].replace(/[^0-9+\-Ee.]/g, '');
        if (arrayVal[0].length > 3) {
            arrayVal[0] = arrayVal[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, ' ');
        }
        if (arrayVal[1] !== undefined && arrayVal[1] !== '') {
            arrayVal[1] = arrayVal[1].length > dec ? arrayVal[1].substring(0, dec) : arrayVal[1];
            value = arrayVal.join('.');
        } else if (arrayVal[0] === '') {
            value = 0;
        } else {
            value = arrayVal[0];
        }

        return value;
    };
})();