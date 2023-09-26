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

   //открытие окна регистрации при клике на "Оформить подписку"
   if (document.querySelector('[data-link = "noauth"]')) {
      const rateLinkArr = document.querySelectorAll('[data-link = "noauth"]')

      rateLinkArr.forEach(element => {
         element.addEventListener('click', openRegBlock)
      })
   }
})

// Калькулятор
const formCalc = document.querySelector('.calculator')
const range = formCalc.querySelector('.calculator__value-block input[type="range"]')
calculateDay()

formCalc.addEventListener('change', (event) => {
   if (event.target.type == 'number') {
      if (event.target.id != 'calculator-profit_target' && event.target.id != 'calculator-day-profit_target') {
         event.target.parentNode.querySelector('input[type="range"]').value = event.target.value
      }
      calculateDay()
   }
   else if (event.target.type == 'range') {
      event.target.parentNode.querySelector('input[type="number"]').value = event.target.value
   }
   calculateDay()
})

formCalc.addEventListener('pointerdown', () => {
   formCalc.addEventListener('pointermove', changeRange)
})
formCalc.addEventListener('pointerup', () => {
   formCalc.removeEventListener('pointermove', changeRange)
})

function changeRange(event) {
   if (event.target.type == 'range') {
      event.target.parentNode.querySelector('input[type="number"]').value = event.target.value
      calculateDay()
   } else {
      formCalc.removeEventListener('pointermove', changeRange)
   }
}

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
      if (totalProfit.value < 0) {
         totalProfit.value = 0
      }

      totalDayProfit.value = Math.ceil(Math.log((targetDayProfit * 100 / (spredDayProfit * rangeDayProfit)) / depositDayProfit) / Math.log(spredDayProfit / 100 * rangeDayProfit + 1))
      if (totalDayProfit.value < 0) {
         totalDayProfit.value = 0
      }
   }
}

