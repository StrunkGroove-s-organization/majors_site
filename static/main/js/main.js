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


// калькулятор
const formCalc = document.querySelector('.calculator')
const range = formCalc.querySelector('.calculator__value-block input[type="range"]')
calculateDay()

formCalc.addEventListener('change', (event) => {
  if (event.target.type == 'number') {
    calculateDay()
  }
})

formCalc.addEventListener('pointermove', (event) => {
  if (event.target.type == 'range') {
    event.target.parentNode.querySelector('input[type="number"]').value = event.target.value
    calculateDay()

  }
})

function calculateDay() {
  const totalProfit = document.querySelector('#calculator-profit_total')
  const depositProfit = document.querySelector('#calculator-profit_deposit').value
  const rangeProfit = document.querySelector('#calculator-profit_range').value
  const spredProfit = document.querySelector('#calculator-profit_spred').value
  const targetProfit = document.querySelector('#calculator-profit_target').value
  const totalDayProfit = document.querySelector('#calculator-day-profit_total')
  const depositDayProfit = document.querySelector('#calculator-day-profit_deposit').value
  const rangeDayProfit = document.querySelector('#calculator-day-profit_range').value
  const spredDayProfit = document.querySelector('#calculator-day-profit_spred').value
  const targetDayProfit = document.querySelector('#calculator-day-profit_target').value

  if (depositProfit != '' && rangeProfit != "" && spredProfit != "" && targetProfit != "") {
    totalProfit.value = Math.ceil(Math.log(targetProfit / depositProfit) / Math.log(spredProfit / 100 * rangeProfit + 1))
    totalDayProfit.value = Math.ceil(Math.log((targetDayProfit * 100 / (spredDayProfit * rangeDayProfit)) / depositDayProfit) / Math.log(spredDayProfit / 100 * rangeDayProfit + 1))
  }
}
