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
const menuBtn = document.querySelector('.calculator__arrow')
const calcMenu = document.querySelector('.calculator__menu')
const calcMenuTitle = document.querySelector('label[for = "calculator-profit_target"]')
let typeCalc = 'deposit'
calculateDay()

formCalc.addEventListener('change', () => {

   if (event.target.type == 'number') {
      calculateDay()
   }
   else if (event.target.type == 'range') {
      event.target.parentNode.querySelector('input[type="number"]').value = event.target.value
      calculateDay()
   }
})

formCalc.addEventListener('pointermove', (event) => {
   if (event.target.type == 'range') {
      event.target.parentNode.querySelector('input[type="number"]').value = event.target.value
      calculateDay()
   }
})

formCalc.addEventListener('click', (event) => {
   if (event.target == menuBtn) {
      checkMenu()
   }
   else if (event.target == document.querySelector('span[data-calc="deposit" ]') || event.target == document.querySelector('span[data-calc="profit"]')) {
      changeCalcType(event.target)
   }
   else {
      menuBtn.classList.remove('active')
      calcMenu.classList.remove('active')
   }
})

function checkMenu() {
   menuBtn.classList.toggle('active')
   calcMenu.classList.toggle('active')

}
function changeCalcType(element) {
   console.log(element.dataset.calc);
   typeCalc = element.dataset.calc
   calcMenuTitle.textContent = element.textContent
   menuBtn.classList.remove('active')
   calcMenu.classList.remove('active')
   calculateDay()
}


function calculateDay() {
   const totalProfit = document.querySelector('#calculator-profit_total')
   const depositProfit = document.querySelector('#calculator-profit_deposit').value
   const rangeProfit = document.querySelector('#calculator-profit_range').value
   const spredProfit = document.querySelector('#calculator-profit_spred').value
   const targetProfit = document.querySelector('#calculator-profit_target').value

   if (typeCalc == 'deposit') {
      totalProfit.value = Math.ceil(Math.log(targetProfit / depositProfit) / Math.log(spredProfit / 100 * rangeProfit + 1))
   }
   else if (typeCalc == 'profit') {
      totalProfit.value = Math.ceil(Math.log((targetProfit * 100 / (spredProfit * rangeProfit)) / depositProfit) / Math.log(spredProfit / 100 * rangeProfit + 1))
   }
}

//Animations foryou
const foryouItems = Array.from(document.querySelectorAll('.foryou__item'))
document.addEventListener("scroll", anumationForyouItems)

function anumationForyouItems() {
   foryouItems.forEach((element, count) => {
      if (element.getBoundingClientRect().y < window.outerHeight * 0.7) {
         element.classList.remove('hide')
         foryouItems.splice(count, 1)
      }
      if (foryouItems.length == 0) {
         document.removeEventListener("scroll", anumationForyouItems)
      }
   })
}

