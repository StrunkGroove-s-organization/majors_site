//слайдер
$(document).ready(function () {
   $('.company__list').slick({
      infinite: true,
      dots: false,
      arrows: false,
      slidesToShow: 5,
      autoplay: true,
      autoplaySpeed: 0,
      speed: 15000,
      swipe: false,
      touchMove: false,
      cssEase: 'linear',
      variableWidth: true,
      responsive: [
         {
            breakpoint: 1000,
            settings: {
               slidesToShow: 4,
            }
         },
         {
            breakpoint: 700,
            settings: {
               slidesToShow: 3,
            }
         },
         {
            breakpoint: 500,
            settings: {
               slidesToShow: 2,
            }
         },
      ]
   });

   $('.rates__slider').slick({
      arrows: true,
      slidesToShow: 3,
      prevArrow: '.rates__slider-btn_prev',
      nextArrow: '.rates__slider-btn_next',
      responsive: [
         {
            breakpoint: 1000,
            settings: {
               slidesToShow: 1,
               dots: true,

            }
         },
      ]
   })

   if (document.querySelector('[data-link = "noauth"]')) {
      const rateLinkArr = document.querySelectorAll('[data-link = "noauth"]')

      rateLinkArr.forEach(element => {
         element.addEventListener('click', openLoginBlock)
      })
   }
})







