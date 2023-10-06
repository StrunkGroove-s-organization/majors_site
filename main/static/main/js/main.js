// $(document).ready(function () {
//   //   $(".slider").slick();
// });

// $(function() {

// })

// new Swiper(".productivity-block__swiper-container");

const mySwiper = new Swiper(".productivity-block__swiper-container", {
  slidesPerView: 2,
  spaceBetween: 30,
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

const mySwiper2 = new Swiper(".blog-block__swiper-container", {
  slidesPerView: 2,
  spaceBetween: 30,
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
