$(document).ready(function () {
    // Swiper Client
    var partners = $('.swiper-slide').length;
    var slidesPerView;
    if (partners <= 5) {
        slidesPerView = partners;
    } else {
        slidesPerView = 5;
    }
    var swiper = new Swiper('.swiper-container', {
        speed:10000,
        autoplay: 1,
        slidesPerView: slidesPerView,
        spaceBetween: 50,
        loop: true,
        breakpoints: {
            1024: {
                slidesPerView: slidesPerView < 4 ? slidesPerView : 4,
                spaceBetween: 50
            },
            992: {
                slidesPerView: slidesPerView < 3 ? slidesPerView : 3,
                spaceBetween: 40
            },
            768: {
                slidesPerView: slidesPerView < 3 ? slidesPerView : 3,
                spaceBetween: 30
            },
            600: {
                slidesPerView: slidesPerView < 2 ? slidesPerView : 2,
                spaceBetween: 30
            },
            480: {
                slidesPerView: 1,
                spaceBetween: 0
            }
        }
    });

});