(function () {
    'use strict';
    window.CalculationMortgage = {};
    var self = window.CalculationMortgage;

    self.init = function () {
        var calcCol = $('.calc-col');
        var cost = calcCol.attr('data-cost');
        if (cost !== undefined) {
            $('#amount').val(Utils.getNumberFormat(cost, 2));
            $('#rate').val(Utils.getNumberFormat(calcCol.attr('data-rate'), 2));
            $('#year').val('30');

            $('.calculate').click();
        }
    };

    self.clickOnMortgageCost = function (elem) {
        var cost = $(elem).parents('.estate-item').find('.estate-common-cost').text();
        if (cost === undefined || cost === '')
            cost = $('.estate-cost').text();
        location.href = '/calculator/' + cost.replace('руб.', '').replace(/[^0-9+\-Ee.]/g, '');
    };

    self.checkMaxValue = function (field, maxValue) {
        var fieldInput = $(field);
        var value = fieldInput.val();
        if (parseInt(value) > maxValue) {
            fieldInput.val(maxValue)
        }
    };

    self.calculateMortgage = function () {
        var amount = $('#amount').val().replace(/[^0-9+\-Ee.]/g, '');
        var rate = $('#rate').val().replace(/[^0-9+\-Ee.]/g, '');
        var year = $('#year').val().replace(/[^0-9+\-Ee.]/g, '');
        var result;

        if (amount !== '' && rate !== '' && year !== '') {
            if ($('#annuity').attr('checked')) {
                result = calculateAnnuity(amount, rate, year);
            } else {
                result = calculateDifferentiate(amount, rate, year);
            }

            $('.result-calculate').css('display', 'block');
            var monthPay = $('#month-pay');
            monthPay.html(result.monthPay + ' руб.');
            var totalCost = $('#total-cost');
            totalCost.html(result.total + ' руб.');
        }
    };

    function calculateAnnuity(amount, rate, year) {
        var month = year * 12;
        rate = rate / 1200.0;
        var annuityCoef = (rate * Math.pow(1 + rate, month)) / (Math.pow(1 + rate, month) - 1);
        var monthPay = amount * annuityCoef;
        var total = monthPay * month;
        return {
            total: Utils.getNumberFormat(total.toString(), 2),
            monthPay: Utils.getNumberFormat(monthPay.toString(), 2)
        };
    }

    function calculateDifferentiate(amount, rate, year) {
        var mp;
        var arr = [];
        var month = year * 12;
        var mp_real = amount / (year * 12.0);
        while (month !== 0) {
            mp = mp_real + (amount * rate / 1200);
            arr.push(mp);
            amount -= mp_real;
            month = month - 1;
        }

        return {
            total: Utils.getNumberFormat(arr.reduce(function (sum, current) {
                return sum + current
            }, 0).toString(), 2),
            monthPay: 'от ' + Utils.getNumberFormat(arr[0].toString(), 2) + ' до '
            + Utils.getNumberFormat(arr[arr.length - 1].toString(), 2)
        };
    }
})();