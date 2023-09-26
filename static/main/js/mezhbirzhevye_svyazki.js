// document.addEventListener("DOMContentLoaded", () => {

// Подсветка кнопки в header
Array.from(document.querySelectorAll('.menu_item')).forEach(element => element.classList.remove('active'));
document.querySelector('[data-menu="crossmarket"]').classList.add('active')

// sidebar
// document.addEventListener('DOMContentLoaded', () => {
//    checkAsideForm()
// }, { once: true })

let pageSection

class SidebarList {
    constructor(listClass, forPage) {
        this.btn = document.querySelector(listClass);
        this.forPage = forPage;
        this.listBlock = this.btn.querySelector('.sidebar__select-list');
        if (forPage == 'p2p2') {
            this.listWrapper = this.listBlock.querySelector('.sidebar__list-wrapper.p2p2');
        } else if (forPage == 'p2p3') {
            this.listWrapper = this.listBlock.querySelector('.sidebar__list-wrapper.p2p3');
        }
        if (forPage == 'p2p2' || forPage == 'p2p3') {
            this.arrayElements = Array.from(this.listWrapper.querySelectorAll(`label`));
        } else {
            this.arrayElements = Array.from(this.listBlock.querySelectorAll(`label`));
        }
    }

    hide() {
        this.btn.classList.add('hidden')
        this.listBlock.classList.add('hidden')
    }
    toggle() {
        this.listBlock.classList.toggle('hidden')
        this.btn.classList.toggle('hidden')
    }
    changeActiveList() {
        if (this.forPage != 'all') {
            if (this.forPage == pageSection) {
                this.listWrapper.classList.add('show')
            }
            else {
                this.listWrapper.classList.remove('show')
            }
        }
    }
}

class SidebarRadioList extends SidebarList {
    changeTitle() {
        if (this.forPage == pageSection || this.forPage == 'all') {
            const copyElement = this.arrayElements.find(element => {
                // debugger
                return this.listBlock.querySelector(`#${element.getAttribute('for')}`).checked
            }).cloneNode(true)
            this.btn.querySelector('.select-title').innerHTML = '';
            this.btn.querySelector('.select-title').insertAdjacentElement('afterbegin', copyElement);
            this.hide()
        }
    }
}

class SidebarCheckboxList extends SidebarList {
    changeTitle() {
        if (this.forPage == pageSection || this.forPage == 'all') {
            let listArr = this.arrayElements.filter((element) => {
                return this.listBlock.querySelector(`#${element.getAttribute('for')}`).checked;
            });
            if (listArr.length == 0) {
                this.btn.querySelector('.select-title').innerHTML = `Фильтр отключен`
            }
            else if (listArr.length == 1) {
                this.btn.querySelector('.select-title').innerHTML = `${listArr[0].textContent}`
            }
            else {
                this.btn.querySelector('.select-title').innerHTML = `${listArr[0].textContent} <span class="select-counter">+${listArr.length - 1}</span>`
            };
        }
    }
}


document.querySelector('.sidebar').addEventListener('click', (event) => {
    menuArray.forEach(element => {

        if (event.target == element.btn || (event.target.parentNode == element.btn && event.target != element.listBlock)) {
            if (element.forPage == 'all' || element.forPage == pageSection) {
                element.toggle()
            }
        }
        else if (event.target == element.listBlock || event.target.parentNode == element.listBlock || event.target == element.listWrapper || event.target.parentNode == element.listWrapper) {
            if (element.forPage == 'all' || element.forPage == pageSection) {
                element.changeTitle()
            }
        }
        else {
            element.hide()
        }
    })
})

function refreshSidebarTitle() {
    menuArray.forEach(element => {
        element.changeTitle()
    })
}
let refreshInterval;
const asideForm = document.querySelector('.sidebar__form')

// function checkAsideForm() {
//     if (localStorage.getItem('form_spreadtable')) {
//         loadForm()
//     }
//     else {
//         saveForm()
//     }
// }
// function saveForm() {
//     let checkedInputs = {}
//     asideForm.querySelectorAll('input').forEach((element) => {
//         if ((element.type == 'checkbox' || element.type == 'radio') && element.checked == true) {
//             checkedInputs[element.id] = element.value
//         } else if (element.type == 'number') {
//             checkedInputs[element.id] = element.value
//         }
//     })


//     const localData = JSON.stringify(checkedInputs)
//     localStorage.setItem('form_spreadtable', localData)
// }
// function loadForm() {
//     const saveFormData = JSON.parse(localStorage.getItem('form_spreadtable'))
//     asideForm.querySelectorAll('input').forEach((element) => {
//         if (element.type == 'checkbox' || element.type == 'radio') {
//             element.checked = false;
//         } else if (element.type == 'number') {
//             element.value = ''
//         }
//     })

//     for (key in saveFormData) {
//         if (asideForm.querySelector(`#${[key]}`).type == 'checkbox' || asideForm.querySelector(`#${[key]}`).type == 'radio') {
//             asideForm.querySelector(`#${[key]}`).checked = true
//         } else if (asideForm.querySelector(`#${[key]}`).type == 'number') {
//             asideForm.querySelector(`#${[key]}`).value = saveFormData[key];
//         }

//     }
//     refreshSidebarTitle()
//     reloadRefresh()
// }


const menuMarketBuyChekbox = new SidebarCheckboxList('.sidebar__title_market-buy', 'all');
const menuMarketSellChekbox = new SidebarCheckboxList('.sidebar__title_market-sell', 'all');
// const menuTokenRadio2 = new SidebarRadioList('.sidebar__select_token', 'p2p2');
// const menuTokenRadio3 = new SidebarRadioList('.sidebar__select_token', 'p2p3');
// const menuTradeRadio = new SidebarRadioList('.sidebar__select_trade', 'all');

const menuArray = [
    menuMarketBuyChekbox,
    menuMarketSellChekbox
    //     menuPaymentChekbox,
    //     menuMarketChekbox,
    //     menuTokenRadio2,
    //     menuTokenRadio3,
    //     menuTradeRadio
]


// Переключение p2p2/p2p3
// const navLinkArr = document.querySelectorAll('.nav-link');
// const p2p2Btn = document.querySelector('[data-page="p2plinks_2"]')
// const p2p3Btn = document.querySelector('[data-page="p2plinks_3"]')
const formNode = document.querySelector(".link-cross-market__form")
// const onlyUsdtCheckbox = document.querySelector('#id_only_stable_coin+label')
let lastFormData = {};
// let lastLimitData = {};

// changeSectionMark(p2p2Btn)
// refreshSidebarTitle()
// changePageSection('p2p2')

// p2p2Btn.addEventListener('click', () => {
//     document.querySelector('.link-content').classList.remove('link-content_p2p3')
//     changeSectionMark(p2p2Btn);
//     changePageSection('p2p2');
// })
// p2p3Btn.addEventListener('click', () => {
//     document.querySelector('.link-content').classList.add('link-content_p2p3')
//     changeSectionMark(p2p3Btn);
//     changePageSection('p2p3');
// })

// function changeSectionMark(btn) {
//     for (let index = 0; index < navLinkArr.length; index++) {
//         navLinkArr[index].classList.remove('active')
//     }
//     btn.classList.add('active')
// }

// function changePageSection(section) {
//     pageSection = section;
//     generateTitleBlock()
//     onlyUsdtCheckboxHide()

//     menuArray.forEach(element => {
//         element.changeActiveList();
//         element.changeTitle();
//     })
//     sendData(formNode);
// }

// function generateTitleBlock() {
//     if (pageSection == 'p2p2') {
//         document.querySelector('.link-content__title-block').innerHTML = ' <div class="link-content__title link-content__title_buy">Покупка</div><div class="link-content__title link-content__title_sell">Продажа</div><div class="link-content__title link-content__title_spred">Спред, %</div><div class="link-content__title link-content__title_profit">Прибыль, ₽</div>'
//     } else if (pageSection == 'p2p3') {
//         document.querySelector('.link-content__title-block').innerHTML = ' <div class="link-content__title link-content__title_buy">Покупка</div><div class="link-content__title link-content__title_change">Обмен</div><div class="link-content__title link-content__title_sell">Продажа</div><div class="link-content__title link-content__title_spred">Спред, %</div><div class="link-content__title link-content__title_profit">Прибыль, ₽</div>'
//     }
// }
// function onlyUsdtCheckboxHide() {
//     if (pageSection == 'p2p2') {
//         onlyUsdtCheckbox.classList.add('hidden')
//     }
//     else if (pageSection == 'p2p3') {
//         onlyUsdtCheckbox.classList.remove('hidden')
//     }
// }

checkForm()
formNode.addEventListener('change', () => {
    // saveForm()
    checkForm()
    reloadRefresh()

});

const refreshCheckbox = document.querySelector('#checkbox-refresh');

function checkForm() {
    const formData = new FormData(formNode);
    let formValues = {}

    for (const key of formData.keys()) {
        formValues[key] = formData.getAll(key)
    }

    if (JSON.stringify(formValues) == JSON.stringify(lastFormData)) {
        // console.log('no change');
        return
    }
    lastFormData = {};
    Object.assign(lastFormData, formValues)
    refreshSidebarTitle();
    sendData(formNode);
}

function reloadRefresh() {
    clearInterval(refreshInterval);
    if (refreshCheckbox.checked) {
        refreshInterval = setInterval(() => sendData(formNode), 5000) //интервал обновления
    }
}
// sendData('')
function sendData(dataPost) {
    let jsonForm = {
        // csrfmiddlewaretoken: dataPost.querySelector('input[name = "csrfmiddlewaretoken"]').value
    }

    let url = '/api/v1/mezhbirzhevye-svyazki/'
    // if (pageSection == 'p2p2') {
    //     url = '/api/p2plinks_2/'
    // } else if (pageSection == 'p2p3') {
    //     url = '/api/p2plinks_3/'
    // }
    dataPost.querySelectorAll('input').forEach((element) => {
        if (element.type == "checkbox") {
            // if (element.getAttribute('name') == 'only_stable_coin') {
            //     jsonForm[element.getAttribute('name')] = element.checked;
            //     return;
            // }
            if (element.id == 'checkbox-refresh') {
                return
            }
            if (element.checked) {
                if (!jsonForm.hasOwnProperty(element.getAttribute('name'))) {
                    jsonForm[element.getAttribute('name')] = []
                }
                jsonForm[element.getAttribute('name')].push(element.value)
            }
        }
        else if (element.type == "radio" && element.checked) {
            jsonForm[element.getAttribute('name')].push(element.value)
        }
        else if (element.type == 'hidden') {
            return
        }

        else {
            if (element.name == 'deposit') {
                return
            }
            jsonForm[element.getAttribute('name')] = element.value
        }
    })


    return fetch(url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-CSRFToken': document.querySelector('input[name = "csrfmiddlewaretoken"]').value },
            body: JSON.stringify(jsonForm),
        }).then((response) => {
            return response.json()
        }).then((responseData) => {
            if (responseData.error) {
                renderError(responseData)
            }
            else {
                renderData(responseData)
            }
        });
}

function renderData(dataObject) {
    let pairCounter = 0; //Счетчик сгенерированных пар
    const summ = document.querySelector('input[id="id_user_deposit-crossmarket"]').value;
    // const summ = 10000;
    let data = dataObject
    let contentBlock = document.querySelector('.link-content__content-block')
    document.querySelector('.link-content__content-block').innerHTML = '';
    for (const key in data) {
        if (Object.hasOwnProperty.call(data, key)) {
            const element = data[key];
            let tableRow = document.createElement('div');
            tableRow.classList.add('link-content__item-block');
            tableRow.innerHTML = `
        <div class="link-content__item link-content__item_buy">
            <div class="card__top">Покупка</div>
            <div class="card__visible-info">
                  <div class="card__payments">
                     <img src="${exchangeInfo.setSrc(element.exchange_first)}" alt="">
                     <p>${element.exchange_first}</p>
                  </div>
                  <div class="card__token">${element.give_first} / ${element.give_second}</div>
                  <div class="card__price">${element.price_first}
                  </div>
                <a href="${exchangeInfo.createConvertLink(element.exchange_first, element.give_second, element.give_first)}" target="_blank" class="btn btn_purple btn_crossmarket">Открыть</a>
            </div>
        </div>

        <div class="link-content__item link-content__item_sell">
            <div class="card__top">Продажа</div>
         <div class="card__visible-info">
               <div class="card__payments">
               <img src="${exchangeInfo.setSrc(element.exchange_second)}" alt="">
               <p>${element.exchange_first}</p>
               </div>
               <div class="card__token">${element.get_first} / ${element.get_second}</div>
               <div class="card__price">${element.price_second}
               </div>
                <a href="${exchangeInfo.createConvertLink(element.exchange_second, element.get_first, element.get_second)}" target="_blank" class="btn btn_purple btn_crossmarket">Открыть</a>
         </div>
        </div>
        <div class="link-content__item link-content__item_spred">
            <div class="card__top">Спред,%</div>
            ${element.spread} %
        </div>
        <div class="link-content__item link-content__item_profit">
            <div class="card__top">Прибыль, $</div>

            ${((Number(summ) + (element.spread * Number(summ)) / 100) - Number(summ)).toFixed(1)} $
        </div>

        `
            contentBlock.insertAdjacentElement('beforeend', tableRow)
            pairCounter++;

            // if (pageSection == 'p2p3') {
            //     let changeBlock = document.createElement('div');
            //     changeBlock.classList.add('link-content__item')
            //     changeBlock.classList.add('link-content__item_change')
            //     changeBlock.innerHTML = `
            // <div class="card__top">Обмен</div>
            // <div class="card__change">
            //     <div class="card__change-tokens">
            //         <div class="card__spot">${element.spot}</div>
            //         <div class="card__token-usdt">
            //         ${element[1].token}
            //         <div class="card__arrow">
            //             <svg xmlns="http://www.w3.org/2000/svg" width="36" height="16" viewBox="0 0 36 16" fill="none">
            //                 <path d="M1 3.5C0.723858 3.5 0.5 3.72386 0.5 4C0.5 4.27614 0.723858 4.5 1 4.5V3.5ZM35.3536 4.35355C35.5488 4.15829 35.5488 3.84171 35.3536 3.64645L32.1716 0.464466C31.9763 0.269204 31.6597 0.269204 31.4645 0.464466C31.2692 0.659728 31.2692 0.976311 31.4645 1.17157L34.2929 4L31.4645 6.82843C31.2692 7.02369 31.2692 7.34027 31.4645 7.53553C31.6597 7.7308 31.9763 7.7308 32.1716 7.53553L35.3536 4.35355ZM1 4.5H35V3.5H1V4.5Z" fill="#191717"/>
            //                 <path d="M35 12.5C35.2761 12.5 35.5 12.2761 35.5 12C35.5 11.7239 35.2761 11.5 35 11.5L35 12.5ZM0.646446 11.6464C0.451183 11.8417 0.451183 12.1583 0.646446 12.3536L3.82843 15.5355C4.02369 15.7308 4.34027 15.7308 4.53553 15.5355C4.7308 15.3403 4.7308 15.0237 4.53553 14.8284L1.70711 12L4.53553 9.17157C4.7308 8.97631 4.7308 8.65973 4.53553 8.46446C4.34027 8.2692 4.02369 8.2692 3.82843 8.46446L0.646446 11.6464ZM35 11.5L1 11.5L1 12.5L35 12.5L35 11.5Z" fill="#191717"/>
            //             </svg>
            //         </div>
            //         ${element[2].token}
            //         </div>
            //     </div> 
            //     <div class="card-change-price"></div>  
            // </div>
            // `
            //     tableRow.querySelector('.link-content__item_buy').insertAdjacentElement("afterend", changeBlock)
            // }
        }
    };
    if (pairCounter == 0) {
        renderError({ error: 'Не найдено ни одного выгодного предложения. Попробуйте изменить лимиты' })
    }
}

function renderError(errorData) {
    document.querySelector('.link-content__content-block').innerHTML = '';
    let tableRow = document.createElement('div');
    tableRow.classList.add('link-content__item-block');
    tableRow.innerHTML = `
        <div class="link-content__item link-content__item_error">
            <p>${errorData.error}</p>
        </div>
            `
    document.querySelector('.link-content__content-block').insertAdjacentElement('beforeend', tableRow)
}

//Аккордеон

// const accirdeonBtn = document.querySelector('.input-section__hidden-btn')
// const accirdeonBlock = document.querySelector('.input-section__hidden-block')

// accirdeonBtn.addEventListener('click', () => {
//     accirdeonBlock.classList.toggle('hidden')
//     accirdeonBtn.classList.toggle('hidden')
// })

// })