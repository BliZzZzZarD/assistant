(function () {
    window.CallBackForm = {};
    var self = window.CallBackForm;

    var url = {
        mail: "/send_mail/",
        wait: "/send_wait_call/"
    };

    var csrftoken = $.cookie('csrftoken');

    var person = $("#callBackFormPerson");
    var email = $("#callBackFormEmail");
    var phone = $("#callBackFormPhone");
    var phoneWait = $("#callBackMiniFormPhone");
    var text = $("#callBackFormText");
    var error = $(".alertErrorString");

    function checkCallBackForm(params) {

        clearAlertError();

        var regPerson = /^[A-ZА-Я]+$/i,
            regEmail = /.+@.+\..+/i,
            regPhone = /^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$/,
            checker = {
                isValid: true,
                message: ""
            };

        if (!regPerson.test(params.person)) {
            checker.isValid = false;
            checker.message = "Имя должно содержать только буквенные символы;";
            person.addClass("alertErrorInput");
        }

        if (!regEmail.test(params.email)) {
            checker.isValid = false;
            checker.message += "Email должен быть вида example@example.exam;";
            email.addClass("alertErrorInput");
        }

        if (params.phone === "") {
            checker.isValid = false;
            checker.message += "Поле телефона не должно быть пустым;";
            phone.addClass("alertErrorInput");
        } else {
            if (!regPhone.test(params.phone)) {
                checker.isValid = false;
                checker.message += "Номер телефона должен содержать только цифровые символы, знак '-' и круглые скобки. " +
                    "Номер должен начинаться с цифры или + и заканчиваться цифрой;";
                phone.addClass("alertErrorInput");
            }
        }

        return checker;
    }

    self.sendMail = function () {
        var params = {
            person: person.val(),
            email: email.val(),
            phone: phone.val(),
            text: text.val()
        };

        var checker = checkCallBackForm(params);
        if (checker.isValid) {
            $.ajax({
                beforeSend: initBeforeAjax,
                type: "POST",
                url: url.mail,
                data: params
            }).done(function (result) {
                if (result === 'OK') {
                    alert('Письмо успешно отправлено');
                    clearAlertError();
                } else {
                    error.html(result);
                }
            });
        } else {
            error.html(checker.message.replace(/;/g, "<br>"));
        }
    };

    self.sendWaitMail = function () {
        var phoneClient = phoneWait.val();

        if (phoneClient !== undefined && phoneClient !== '') {
            var checker = checkWaitCall(phoneClient);
            if (checker.isValid) {
                var params = {
                    text: 'Клиент с номером ' + phoneClient + ' ожидает нашего звонка'
                };

                $.ajax({
                    beforeSend: initBeforeAjax,
                    type: "POST",
                    url: url.wait,
                    data: params
                }).done(function (result) {
                    if (result === 'OK') {
                        alert('Спасибо, мы обязательно Вам перезвоним.');
                        phoneWait.val('');
                    } else {
                        alert(result);
                    }
                });
            } else {
                alert(checker.message);
            }
        }
    };

    function checkWaitCall(phoneClient) {
        var regPhone = /^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$/,
            checker = {
                isValid: true,
                message: "Номер телефона должен содержать только цифровые символы, знак '-' и круглые скобки. " +
                "Номер должен начинаться с цифры или + и заканчиваться цифрой"
            };

        if (!regPhone.test(phoneClient))
            checker.isValid = false;

        return checker;
    }

    function clearAlertError() {
        error.html("");
        person.removeClass("alertErrorInput").val("");
        email.removeClass("alertErrorInput").val("");
        phone.removeClass("alertErrorInput").val("");
        text.val("");
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function initBeforeAjax(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
})();