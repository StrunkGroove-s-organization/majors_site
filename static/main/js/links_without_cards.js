// document.addEventListener("DOMContentLoaded", () => {
const saveFormObject = new SaveForm('form_nocard', document.querySelector('.link-nocard__form'), 'createFormObject')

// Подсветка кнопки в header
Array.from(document.querySelectorAll('.menu_item')).forEach(element => element.classList.remove('active'));
document.querySelector('[data-menu="nocard"]').classList.add('active')

document.addEventListener('DOMContentLoaded', () => {
    saveFormObject.checkAsideForm()
}, { once: true })

//sidebar
const pageSection = 'all';
let selectInput = [];

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
                this.btn.querySelector('.select-title').innerHTML = `Выберите фильтр`
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

const menuTokenRadio = new SidebarRadioList('.sidebar__select_token', 'all');
const menuMarketRadio = new SidebarRadioList('.sidebar__title_market', 'all');
// let menuTokenPairChekbox;

const menuArray = [
    menuMarketRadio,
    menuTokenRadio,
]
function refreshSidebarTitle() {
    menuArray.forEach(element => {
        element.changeTitle()
    })
}
refreshSidebarTitle()


//Отправка формы и генерация карточек

// let form = new FormData(document.querySelector('form'))
const table = document.querySelector('.token-links')
const refreshCheckbox = document.querySelector('.sidebar__refresh_nocard input');

document.querySelector('form').addEventListener('submit', (event) => {
    event.preventDefault()
})
let refreshInterval
function reloadRefresh() {
    clearInterval(refreshInterval);
    if (refreshCheckbox.checked) {
        refreshInterval = setInterval(() => createFormObject(), 30000) //интервал обновления
    }
}

document.querySelector('form').addEventListener('change', () => {
    saveFormObject.saveForm()
    createFormObject()
    reloadRefresh()

})
function createFormObject() {
    let formObject = {
        // token: [],
        // market:
    }
    // Array.from(document.querySelectorAll('.sidebar__select_token input')).forEach(input => {
    //     if (input.checked) {
    //         formObject.token.push(input.value)
    //     }
    // })
    // Array.from(document.querySelectorAll('.sidebar__title_market input')).forEach(input => {
    //     if (input.checked) {
    //         formObject.market.push(input.value)
    //     }
    // })
    formObject.token = document.querySelector('.sidebar__select_token input:checked').value
    formObject.market = document.querySelector('.sidebar__title_market input:checked').value
    sendData(formObject)
}

function sendData(formData) {
    // console.log(formData);
    const limitFilterValue = document.querySelector('#id_user_limit-nocard').value
    let pairCounter = 0; //Счетчик сгенерированных пар
    // let rowCounter = 0; //Счетчик строк в разделе
    let pairRows = []

    // const formData = {}
    // formData.limit = document.querySelector('#id_user_limit-nocard').value
    // console.log(JSON.stringify(formData));
    return fetch('/api/v1/links_without_cards_3/',
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-CSRFToken': document.querySelector('input[name = "csrfmiddlewaretoken"]').value },
            body: JSON.stringify(formData),
        }).then((response) => {
            // console.log(response);
            return response.json()
        }).then((dataObj) => {
            if (dataObj.detail) {
                checkDetail(dataObj.detail)
            }
            else {
                const data = dataObj.data
                table.innerHTML = ''

                // if (dataObj.favourite.length != 0) {
                if (0) {
                    let titleSection = document.createElement('div')
                    titleSection.classList.add('token-links_group')
                    titleSection.innerHTML = `
                <div class="token-links_group-title">Избранное</div>
                `
                    table.insertAdjacentElement("beforeend", titleSection)
                    dataObj.favourite.forEach((element) => {
                        let row = document.createElement('div')
                        row.classList.add('token-links__item')
                        row.innerHTML = `
                            <div class="token-links__row">
                            <div class="token-links__first-step">
                                 <p class="token-links__item-title">${element.exchange}</p>
                                <div class="token-links__item-content">
                                    <div class="token-links__token-pair">
                                        <p>${element.ad_give_first}<span>${element.ad_give_first}</span></p>
                                        <span>&nbsp;-&nbsp;</span>
                                        <p>${element.ad_give_second.abbr} <span>${element.ad_give_second.crypto_name}</span></p>
                                    </div>
                                    <span>${element.ad_price_first}</span>
                                    <a href="${exchangeInfo.generateConvertLink(element.ad_give_second.abbr, element.ad_give_first)}" target="_blank" class="btn btn_purple btn_nocard">Купить</a>
                                </div>
                                </div>

                                <div class="token-links__second-step">
                                    <div class="token-links__wrapper">
                                        <p class="token-links__item-title">${element.exchange_info.exchange_name}</p>
                                        <div class="token-links__item-content">
                                            <div class="token-links__token-pair">
                                                <p>${element.ad_give_second.abbr}<span>${element.ad_give_second.crypto_name}</span></p>
                                                <span>&nbsp;-&nbsp;</span>
                                                <p>${element.ad_get_first.abbr} <span>${element.ad_get_first.crypto_name}</span></p>
                                            </div>
                                            <span>${element.best_price}</span>
                                            <a href="https://www.bestchange.ru/click.php?id=${element.exchange_info.exchange_id}" target="_blank" class="btn btn_purple btn_nocard">Обмен</a>
                                        </div>
                                        <div class="token-links__arrow close"></div>
                                    </div>
                                    <div class="token-links__info hidden">
                                        <div class="token-links__info-wrapper">
                                            <p>Мин. лимиты <span>${element.lim_min}</span></p>
                                            <p>Резервы <span>${element.available}</span></p>
                                            <p>Отзывы <span>${element.positive_reviews}/${element.negative_reviews}</span></p>
                                            <p>Рейтинг <span>${element.exchange_info.info_star}</span></p>
                                            <p>Доп. проверка<span>${checkValue(element.exchange_info.info_verification)}</span></p>
                                            <p>Юр. регистрация<span>${checkValue(element.exchange_info.info_registration)}</span></p>
                                        </div>
                                    </div>
                                </div>

                                <div class="token-links__third-step">
                                    <p class="token-links__item-title">${element.exchange}</p>
                                    <div class="token-links__item-content">
                                        <div class="token-links__token-pair">
                                            <p>${element.ad_get_first.abbr}<span>${element.ad_get_first.crypto_name}</span></p>
                                            <span>&nbsp;-&nbsp;</span>
                                            <p>${element.ad_get_second} <span>${element.ad_get_second}</span></p>
                                        </div>
                                        <span>${element.ad_price_second}</span>
                                        <a href="${exchangeInfo.generateConvertLink(element.ad_get_first.abbr, element.ad_get_second)}" target="_blank" class="btn btn_purple btn_nocard btn_nocard_sell">Продать</a>
                                    </div>
                                </div>
                                <div class="token-links__percent">${element.spread_with_fee}%</div>
                                <div class="token-links__profit">
                            ${((Number(deposit) + (element.spread_with_fee * Number(deposit)) / 100) - Number(deposit)).toFixed(1)} $
                                
                                </div>
                            </div>
                            <a class='link-content__favorite_del' data-hash = "${element.hash}">Удалить из избранного</a>
                        `
                        table.insertAdjacentElement("beforeend", row)
                    })
                }


                for (const key in data) {
                    const item = data[key]
                    let titleSection = document.createElement('div')
                    titleSection.classList.add('token-links_group')
                    titleSection.innerHTML = `
                    <div class="token-links_group-title">${item['0'].ad_give_first} - ${item['0'].ad_give_second.abbr} - ${item['0'].ad_get_first.abbr} - ${item['0'].ad_get_second}
                    <a class='link-content__favorite_add'>В избранное</a>
                    </div>
                    `
                    for (const key in item) {
                        const element = item[key]
                        const deposit = document.querySelector('#id_user_limit-nocard').value
                        function checkValue(value) {
                            if (value == true) {
                                return "Да"
                            } else {
                                return "Нет"
                            }
                        }

                        if ((limitFilterValue >= element.lim_min)) {
                            // console.log('imitFilterValue' + limitFilterValue);
                            // console.log('element.lim_min' + element.lim_min);
                            // rowCounter++
                            let row = document.createElement('div')
                            row.classList.add('token-links__item')
                            row.innerHTML = `
                                <div class="token-links__row">
                                <div class="token-links__first-step">
                                     <p class="token-links__item-title">${element.exchange}</p>
                                    <div class="token-links__item-content">
                                        <div class="token-links__token-pair">
                                            <p>${element.ad_give_first}<span>${element.ad_give_first}</span></p>
                                            <span>&nbsp;-&nbsp;</span>
                                            <p>${element.ad_give_second.abbr} <span>${element.ad_give_second.crypto_name}</span></p>
                                        </div>
                                        <div class = "token-links__price">
                                            <span>${element.ad_price_first}</span>
                                            <p>${element.full_price_first}</p>
                                        </div>
                                        <a href="${exchangeInfo.createConvertLink(element.exchange, element.ad_give_first, element.ad_give_second.abbr)}" target="_blank" class="btn btn_purple btn_nocard">Купить</a>
                                    </div>
                                    </div>

                                    <div class="token-links__second-step">
                                        <div class="token-links__wrapper">
                                            <p class="token-links__item-title">${element.exchange_info.exchange_name}</p>
                                            <div class="token-links__item-content">
                                                <div class="token-links__token-pair">
                                                    <p>${element.ad_give_second.abbr}<span>${element.ad_give_second.crypto_name}</span></p>
                                                    <span>&nbsp;-&nbsp;</span>
                                                    <p>${element.ad_get_first.abbr} <span>${element.ad_get_first.crypto_name}</span></p>
                                                </div>
                                                <div class = "token-links__price">
                                                    <span>${element.best_price}</span>
                                                    <p>${element.best_full_price}</p>
                                                </div>
                                                
                                                <a href="https://www.bestchange.ru/click.php?id=${element.exchange_info.exchange_id}" target="_blank" class="btn btn_purple btn_nocard">Обмен</a>
                                            </div>
                                            <div class="token-links__arrow close"></div>
                                        </div>
                                        <div class="token-links__info hidden">
                                            <div class="token-links__info-wrapper">
                                                <p>Мин. лимиты <span>${element.lim_min}</span></p>
                                                <p>Резервы <span>${element.available}</span></p>
                                                <p>Отзывы <span>${element.positive_reviews}/${element.negative_reviews}</span></p>
                                                <p>Рейтинг <span>${element.exchange_info.info_star}</span></p>
                                                <p>Доп. проверка<span>${checkValue(element.exchange_info.info_verification)}</span></p>
                                                <p>Юр. регистрация<span>${checkValue(element.exchange_info.info_registration)}</span></p>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="token-links__third-step">
                                        <p class="token-links__item-title">${element.exchange}</p>
                                        <div class="token-links__item-content">
                                            <div class="token-links__token-pair">
                                                <p>${element.ad_get_first.abbr}<span>${element.ad_get_first.crypto_name}</span></p>
                                                <span>&nbsp;-&nbsp;</span>
                                                <p>${element.ad_get_second} <span>${element.ad_get_second}</span></p>
                                            </div>
                                        <div class = "token-links__price">
                                            <span>${element.ad_price_second}</span>
                                            <p>${element.full_price_second}</p> 

                                        </div>
                                            <a href="${exchangeInfo.createConvertLink(element.exchange, element.ad_get_second, element.ad_get_first.abbr)}" target="_blank" class="btn btn_purple btn_nocard btn_nocard_sell">Продать</a>
                                        </div>
                                    </div>
                                    <div class="token-links__percent">${element.spread_with_fee}%</div>
                                    <div class="token-links__profit">
                                ${((Number(deposit) + (element.spread_with_fee * Number(deposit)) / 100) - Number(deposit)).toFixed(1)} $
                                    
                                    </div>
                                </div>
                                

                            `
                            pairRows.push(row)
                        }
                        // table.insertAdjacentElement("beforeend", row)
                    }

                    if (pairRows.length != 0) {
                        console.log('createRow');
                        table.insertAdjacentElement("beforeend", titleSection)
                        pairRows.forEach(element => {
                            table.insertAdjacentElement("beforeend", element)
                        })
                        pairCounter++
                    }
                    pairRows = [];
                };

                if (pairCounter == 0) {
                    console.log('pairCounter == 0');
                    renderError({ error: 'Не найдено ни одного выгодного предложения. Попробуйте изменить значения фильтров' })
                }
            }
        }).catch(error => {
            console.error(error);
        });
}
// sendData();
// createFormObject();
function checkDetail(detail) {
    if (modalNoPay.modalShowFlag == 0)
        if (detail == 'Authentication credentials were not provided.') {
            setTimeout(() => { modalNoPay.createModal(false) }, 2000)
        }
        else if (detail == 'You do not have permission to perform this action.') {
            setTimeout(() => { modalNoPay.createModal(true) }, 2000)
        }
}
function renderError(errorData) {
    document.querySelector('.token-links').innerHTML = '';
    let tableRow = document.createElement('div');
    tableRow.classList.add('link-content__item-block');
    tableRow.style.marginTop = '50px';
    tableRow.innerHTML = `
            <div class="link-content__item link-content__item_error">
                <p>${errorData.error}</p>
            </div>
                `
    document.querySelector('.token-links').insertAdjacentElement('beforeend', tableRow)
}

// function refreshMenu(data) {
//     const menuLinksList = document.querySelector('.sidebar__title_token-pair .sidebar__select-list')
//     menuLinksList.innerHTML = ''

//     for (const key in data) {
//         // debugger
//         const item = data[key]
//         menuLinksList.insertAdjacentHTML("beforeend",
//             `<input id="checkbox-token-pair-${item[0].ad_give_second.abbr}${item[0].ad_get_first.abbr}-nocard" name="token-pair" type="checkbox">
//         <label for="checkbox-token-pair-${item[0].ad_give_second.abbr}${item[0].ad_get_first.abbr}-nocard">${item['0'].ad_give_first} - ${item[0].ad_give_second.abbr} - ${item[0].ad_get_first.abbr} - ${item[0].ad_get_second}</label>
//         `)
//     }
//     menuTokenPairChekbox = new SidebarCheckboxList('.sidebar__title_token-pair', 'all');
//     if (selectInput.length != 0) {
//         Array.from(menuTokenPairChekbox.listBlock.querySelectorAll('input')).forEach((element) => {
//             if (selectInput.find((item) => {
//                 return item == element.id
//             })) {
//                 element.checked = true;
//             }
//         })
//     }
//     menuTokenPairChekbox.changeTitle()
// }


// открытие-закрытие окна info
document.addEventListener('click', checkClick)

function checkClick(event) {
    if (event.target.classList.contains('token-links__arrow')) {
        toggleInfo(event.target)
    }
}

function toggleInfo(element) {
    element.classList.toggle('close')
    element.parentElement.parentElement.querySelector('.token-links__info').classList.toggle('hidden')
}

document.querySelector('.sidebar').addEventListener('click', (event) => {
    // element = menuTokenPairChekbox
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

//Favorite
document.querySelector('.token-links').addEventListener('click', (event) => {
    if (event.target.classList.contains('link-content__favorite_add')) {
        addFavorite(event.target.parentElement)
    }
    else if (event.target.classList.contains('link-content__favorite_del')) {
        delFavorite(event.target.parentElement)
    }
})
function addFavorite(item) {
    let data = {

        // base_crypto: item.querySelector('.token-links__first-step .token-links__token-pair p:nth-child(1) span').textContent,
        // exchange: item.querySelector('.token-links__first-step .token-links__item-title').textContent,
        // best_change_exchange: item.querySelector('.token-links__second-step .token-links__token-pair').dataset.exchangeid,
        // id_best_change_give: item.querySelector('.token-links__third-step .token-links__token-pair').dataset.tokenid,
        // id_best_change_get: item.querySelector('.token-links__first-step .token-links__token-pair').dataset.tokenid
    }
    console.log(data);
    return fetch('/api/v1/favorite-without-3/',
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-CSRFToken': document.querySelector('input[name = "csrfmiddlewaretoken"]').value },
            body: JSON.stringify(data),
        }).then((response) => {
            console.log(response);
            // return response.json()
        }).then(() => {
            createFormObject()
        })
    // .then((dataObj) => {
    //     const data = dataObj.data
    //     table.innerHTML = ''

}

function delFavorite(item) {
    let data = {
        // base_crypto: item.querySelector('.token-links__first-step .token-links__token-pair p:nth-child(1) span').textContent,
        // exchange: item.querySelector('.token-links__first-step .token-links__item-title').textContent,
        // best_change_exchange: item.querySelector('.token-links__second-step .token-links__token-pair').dataset.exchangeid,
        // id_best_change_give: item.querySelector('.token-links__third-step .token-links__token-pair').dataset.tokenid,
        // id_best_change_get: item.querySelector('.token-links__first-step .token-links__token-pair').dataset.tokenid
    }
    return fetch('/api/v1/favorite-without-3/',
        {
            method: "DELETE",
            headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-CSRFToken': document.querySelector('input[name = "csrfmiddlewaretoken"]').value },
            body: JSON.stringify(data),
        }).then((response) => {
            console.log(response);
            // return response.json()
        }).then(() => {
            createFormObject()
        })
    // .then((dataObj) => {
    //     const data = dataObj.data
    //     table.innerHTML = ''
}
// })


//favorite


