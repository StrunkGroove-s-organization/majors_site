
// Переключение buy/sell
let pageSection = 'buy'
const navLinkArr = document.querySelectorAll('.nav-link');
const buyBtn = document.querySelector('[data-page="buy"]')
const sellBtn = document.querySelector('[data-page="sell"]')
changeSectionMark(buyBtn)

buyBtn.addEventListener('click', () => {
   changeSectionMark(buyBtn);
   changePageSection('buy')
})
sellBtn.addEventListener('click', () => {
   changeSectionMark(sellBtn);
   changePageSection('sell');
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
   reloadRefresh();
}

//Отправка запроса
const asideForm = document.querySelector('.sidebar form');
const refreshCheckbox = document.querySelector('#checkbox-refresh');
let table = document.querySelector('.table-content');
let refreshInterval;

asideForm.addEventListener('submit', () => {
   event.preventDefault()
})
document.addEventListener('DOMContentLoaded', () => {
   checkForm()
   postForm()
}, { once: true })

asideForm.addEventListener('change', () => {
   postForm();
   reloadRefresh();
   saveForm()
});

function postForm() {
   let data = new FormData(asideForm)
   url = 'ads/';

   if (pageSection == 'buy') {
      data.append('pageSection', 'Buy')
   } else if (pageSection == 'sell') {
      data.append('pageSection', 'Sell')
   }


   return fetch(url,
      {
         method: "POST",
         body: data
      }).then((response) => {
         return response.text()
      }).then((dataTable) => {
         table.innerHTML = dataTable;
         generateLinks();
      }).catch(error => {
         console.error(error);
      });
}

function reloadRefresh() {
   clearInterval(refreshInterval);
   if (refreshCheckbox.checked) {
      refreshInterval = setInterval(postForm, 5000) //интервал обновления
   }
}
function checkForm() {
   if (localStorage.getItem('form_price')) {
      loadForm()
   }
   else {
      saveForm()
   }
}
function saveForm() {
   let checkedInputs = {}
   asideForm.querySelectorAll('input:checked').forEach((element) => {
      checkedInputs[element.id] = element.value
   })
   const localData = JSON.stringify(checkedInputs)
   localStorage.setItem('form_price', localData)
}
function loadForm() {
   const saveFormData = JSON.parse(localStorage.getItem('form_price'))
   asideForm.querySelectorAll('input:checked').forEach((element) => {
      element.checked = false
   })
   for (key in saveFormData) {
      asideForm.querySelector(`#${[key]}`).checked = true
   }
   refreshTitleCheckbox()
   changeTitleRadio(btnToken);
   changeTitleRadio(btnFiat);
}


//Формы sidebar
const btnPay = document.querySelector('.sidebar__title_pay');
const btnMarket = document.querySelector('.sidebar__title_market');
const btnToken = document.querySelector('.sidebar__select_token');
const btnFiat = document.querySelector('.sidebar__select_fiat');

const listPay = btnPay.querySelector('.sidebar__select-list');
const listMarket = btnMarket.querySelector('.sidebar__select-list');
const listToken = btnToken.querySelector('.sidebar__radio-list');
const listFiat = btnFiat.querySelector('.sidebar__radio-list');

const arrChekbox = document.querySelectorAll('.sidebar__select-list input[type="checkbox"]');
const arrLebelChekbox = document.querySelectorAll('.sidebar__select-list input[type="checkbox"]+label');
const arrInputRadioToken = btnToken.querySelectorAll('.sidebar__radio-list input[type="radio"]');
const arrInputRadioFiat = btnFiat.querySelectorAll('.sidebar__radio-list input[type="radio"]');

changeTitleRadio(btnToken);
// changeTitleRadio(btnFiat);

document.addEventListener('click', (event) => {
   let target = event.target;
   if (target === btnPay || target.closest(`.${btnPay.className.split(' ',)[0]}`)) {
      openList(btnPay, listPay);
   }
   else if (target === btnMarket || target.closest(`.${btnMarket.className.split(' ',)[0]}`)) {
      openList(btnMarket, listMarket);
   }
   else if (target === btnToken || target.closest(`.${btnToken.className.split(' ',)[0]}`) && !target.closest('.sidebar__radio-list')) {
      openList(btnToken, listToken);
   }
   else if (target === btnFiat || target.closest(`.${btnFiat.className.split(' ',)[0]}`) && !target.closest('.sidebar__radio-list')) {
      openList(btnFiat, listFiat);
   }
   else if (Array.from(arrChekbox).find(node => node.isEqualNode(target)) || Array.from(arrLebelChekbox).find(node => node.isEqualNode(target)) || target.tagName == 'LABEL') {
   }

   else if (Array.from(arrInputRadioToken).find(node => node.isEqualNode(target))) {
      changeTitleRadio(btnToken);
   }
   else if (Array.from(arrInputRadioFiat).find(node => node.isEqualNode(target))) {
      changeTitleRadio(btnFiat);
   }

   else {
      closeList();
   }
})

function openList(btn, list) {
   if (!btn.classList.contains('hidden')) {
      closeList();
   }
   else {
      closeList();
      btn.classList.remove('hidden');
      list.classList.remove('hidden');
   }
}
function closeList() {
   btnPay.classList.add('hidden');
   listPay.classList.add('hidden');
   btnMarket.classList.add('hidden');
   listMarket.classList.add('hidden');
   btnToken.classList.add('hidden');
   listToken.classList.add('hidden');
   btnFiat.classList.add('hidden');
   listFiat.classList.add('hidden');
   refreshTitleCheckbox()

}
function changeTitleRadio(section) {
   baseElement = section.querySelector('.select-title');
   element = section.querySelector('input:checked + label')
   let bufferElement = element.cloneNode(true);
   bufferElement.removeAttribute('for')
   baseElement.innerHTML = '';
   baseElement.insertAdjacentElement('afterbegin', bufferElement);
   closeList()
}
function refreshTitleCheckbox() {
   const checkboxItemsList = [
      { btn: btnPay, list: listPay },
      { btn: btnMarket, list: listMarket },
   ]
   checkboxItemsList.forEach(element => {
      let listArr = element.list.querySelectorAll('input:checked + label');
      let listCounter = listArr.length
      if (listCounter == 0) {
         element.btn.querySelector('.select-title').innerHTML = ``;
         element.btn.querySelector('.select-placeholder').classList.remove('hidden')
      }
      else if (listCounter == 1) {
         element.btn.querySelector('.select-title').innerHTML = `${listArr[0].textContent}`
         element.btn.querySelector('.select-placeholder').classList.add('hidden')

      }
      else {
         element.btn.querySelector('.select-title').innerHTML = `${listArr[0].textContent} <span class="select-counter">+${listCounter - 1}</span>`
         element.btn.querySelector('.select-placeholder').classList.add('hidden')
      }
   });
}

// Генерация ссылок и присвоение иконок

let paymentData = {}
fetch("/static/main/js/payout_links.json")
   .then(response => {
      return response.json()
   }).then(data => {
      paymentData = data;
      console.log(paymentData);
   })

function generateLinks() {
   const priceBlocksArr = document.querySelectorAll('.table-item');
   const paymentsBlockArr = document.querySelectorAll('.payment__item')
   const exchangeInfo = {
      binance: {
         img: '/static/main/img/exchange/binance.png',
         generateLink(trade, token, fiat) {
            if (trade == 'buy') {
               return `${paymentData.Binance.baseUrl}all-payments/` + `${token.trim()}?fiat=` + `${fiat.trim()}`
            } else {
               return `${paymentData.Binance.baseUrl}sell/` + `${token.trim()}?fiat=` + `${fiat.trim()}&payment=` + `all-payments`
            }
         }
      },
      huobi: {
         img: '/static/main/img/exchange/huobi.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Huobi.baseUrl}` + `${trade}-` + `${token.trim()}-` + `${fiat.trim()}`
         }

      },
      bybit: {
         img: '/static/main/img/exchange/bybit.png',
         generateLink(trade, token, fiat) {
            if (trade == 'buy') {
               return `${paymentData.ByBit.baseUrl}1&token=` + `${token.trim()}&fiat=` + `${fiat.trim()}&paymentMethod=`
            } else {
               return `${paymentData.ByBit.baseUrl}0&token=` + `${token.trim()}&fiat=` + `${fiat.trim()}&paymentMethod=`
            }
         }
      },
      okx: {
         img: '/static/main/img/exchange/okx.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Okx.baseUrl}` + `${fiat.trim()}/` + `${trade}-` + `${token.trim()}`
         }
      },
      bitget: {
         img: '/static/main/img/exchange/bitget.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.BitGet.baseUrl}` + `${trade}/` + `${token.trim()}?fiatName=` + `${fiat.trim()}`
         }
      },
      garantex: {
         img: '/static/main/img/exchange/garantex.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Garantex.baseUrl}` + `${token.trim().toLowerCase()}` + `${fiat.trim().toLowerCase()}`
         }
      },
      bitpapa: {
         img: '/static/main/img/exchange/bitpapa.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Bitpapa.baseUrl}` + `${trade}`
         }
      },
      beribit: {
         img: '/static/main/img/exchange/beribit.svg',
         generateLink(trade, token, fiat) {
            return `${paymentData.Beribit.baseUrl}` + `${token.trim()}_` + `${fiat.trim()}`
         }
      },
      'hodl hodl': {
         img: '/static/main/img/exchange/hodl.png',
         generateLink(trade, token, fiat) {
            return `${paymentData["Hodl Hodl"].baseUrl}` + `${trade}?filters%5Bcurrency_code%5D=` + `${fiat.trim()}&pagination%5Boffset%5D=0`
         }
      },
      mexc: {
         img: '/static/main/img/exchange/mexc.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Mexc.baseUrl}`
         }
      },
      kucoin: {
         img: '/static/main/img/exchange/kucoin.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Kucoin.baseUrl}` + `${trade}/` + `${token.trim()}-` + `${fiat.trim()}`
         }
      },
      'gate.io': {
         buy: 'https://www.gate.io/ru/c2c/market',
         sell: 'https://www.gate.io/ru/c2c/market',
         img: '/static/main/img/exchange/gateio.png',
         generateLink(trade, token, fiat) {
            return `${paymentData["Gate.io"].baseUrl}`
         }
      },
      totalcoin: {
         img: '/static/main/img/exchange/totalcoin.png',
         generateLink(trade, token, fiat) {
            return `${paymentData.Totalcoin.baseUrl}` + `${trade}/` + `${token.trim().toLowerCase()}/` + `${fiat.trim().toLowerCase()}`
         }
      }
   }

   const selectToken = document.querySelector('.sidebar__select_token .select-title label').textContent;
   const selectFiat = document.querySelector('.sidebar__select_fiat .select-title label').textContent;
   const selectedPayments = Array.from(document.querySelectorAll('.sidebar__title_pay .sidebar__select-list input:checked + label'), (element) => { return element.textContent })
   console.log('payments:', selectedPayments);
   Array.from(priceBlocksArr).forEach((element) => {
      let exchange = element.querySelector('.btn_favorite').textContent.toLowerCase();
      element.querySelector('.table-item__favorite a').setAttribute('href', exchangeInfo[exchange].generateLink(pageSection, selectToken, selectFiat))
      element.querySelector('.table-item__favorite img').setAttribute('src', exchangeInfo[exchange].img);

      //длинные имена

      // if (element.querySelector('.table-item__name').textContent.length > 20) {
      //    element.querySelector('.table-item__name').style.fontSize = '11px'
      //    element.querySelector('.table-item__name').style.letterSpacing = '-1px'
      // }
   })
   Array.from(paymentsBlockArr).forEach((element) => {
      let paymentName = element.querySelector('.payments__name').textContent;
      element.querySelector('.payment__img').setAttribute('src', paymentImg.setSrc(paymentName));
   })
}
