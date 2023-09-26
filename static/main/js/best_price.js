// Переключение buy/sell
let pageSection = 'buy'
const navLinkArr = document.querySelectorAll('.nav-link');
const buyBtn = document.querySelector('[data-page="buy"]')
const sellBtn = document.querySelector('[data-page="sell"]')
changeSectionMark(buyBtn)
refreshAsideForm()

buyBtn.addEventListener('click', () => {
   changeSectionMark(buyBtn);
   changePageSection('buy')
})
sellBtn.addEventListener('click', () => {
   changeSectionMark(sellBtn);
   changePageSection('sell')
})

function changeSectionMark(btn) {
   for (let index = 0; index < navLinkArr.length; index++) {
      navLinkArr[index].classList.remove('active')
   }
   btn.classList.add('active')
}

function changePageSection(section) {
   pageSection = section;
   postForm();
   refreshAsideForm()
}

function refreshAsideForm() {
   const tokenBtn = document.querySelector('#token_btn_usdd')
   tokenBtn.parentElement.classList.remove('hide')
   if (pageSection == 'buy') {
      tokenBtn.parentElement.classList.add('hide')
   } else if (pageSection == 'sell') {
      tokenBtn.parentElement.classList.remove('hide')
   }
}


const filterBlock = document.querySelector('.sidebar__price-table')

document.addEventListener('DOMContentLoaded', postForm, { once: true })
filterBlock.addEventListener('change', () => {
   postForm();
});

function postForm() {
   let token = filterBlock.querySelector('input[name = "csrfmiddlewaretoken"]').value
   let data = {}
   data.token = filterBlock.querySelector('input:checked').value
   const table = document.querySelector('.price-table__content')

   if (pageSection == 'buy') {
      data.buy_sell = 'BUY'
   } else if (pageSection == 'sell') {
      data.buy_sell = 'SELL'
   }

   url = '/api/best_prices/';

   return fetch(url,
      {
         method: "POST",
         body: JSON.stringify(data),
         headers: {
            "X-CSRFToken": token,
            "Content-Type": "application/json",
         },
      }).then((response) => {
         return response.json()
      }).then((dataTable) => {
         table.innerHTML = '';
         dataTable.forEach((element) => {
            let tableRow = document.createElement('div')
            tableRow.classList.add('price-table__row')
            tableRow.innerHTML = `
            <div class="price-table__item price-table__item_market">
               <a target="_blank" href="${exchangeInfo.createLink(element.exchange, element.adv_no, element.buy_sell, element.token, element.fiat)}"><img src="${exchangeInfo.setSrc(element.exchange)}" alt=""></a>
               <p>${element.exchange}</p>
            </div>
            <div class="price-table__item price-table__item_payment">
               <img src="${paymentImg.setSrc(element.best_payment)}" alt="">
               <p>${element.best_payment}</p>
            </div>
            <div class="price-table__item price-table__item_buy">${element.price}</div>
            <div class="price-table__item price-table__item_limit">₽ ${element.lim_min} - ₽ ${element.lim_max}</div>
            <div class="price-table__item price-table__item_reserve">${element.available} ${element.token}</div>
            `
            table.insertAdjacentElement("beforeend", tableRow)
         })
      }).catch(error => {
         console.error(error);
      });
}
// function reloadRefresh() {
//    clearInterval(refreshInterval);
//    if (refreshCheckbox.checked) {
//       refreshInterval = setInterval(postForm, 5000) //интервал обновления
//    }
// }

// Генерация ссылок и присвоение иконок

let paymentData = {}
fetch("/static/main/js/payout_links.json")
   .then(response => {
      return response.json()
   }).then(data => {
      paymentData = data;
   })

