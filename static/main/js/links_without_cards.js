// document.addEventListener("DOMContentLoaded", () => {
const saveFormObject = new SaveForm('form_nocard', document.querySelector('.link-nocard__form'), 'createFormObject')

// Подсветка кнопки в header
Array.from(document.querySelectorAll('.menu_item')).forEach(element => element.classList.remove('active'));
document.querySelector('[data-menu="nocard"]').classList.add('active')

document.addEventListener('DOMContentLoaded', () => {
    saveFormObject.checkAsideForm()
    favoriteBlockCheck()
    refreshFavorite()
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

document.querySelector('form').addEventListener('change', (event) => {
    if (event.target.parentNode.classList.contains('favorite__item')) {
        changeFavoriteFilter(event.target)
    }
    saveFormObject.saveForm()
    favoriteBlockCheck()
    createFormObject()
    reloadRefresh()
    refreshFavorite()


})
function checkDeposit(price, qty) {
    const deposit = document.querySelector("#id_user_limit-nocard").value
    let diferencia = qty * price - deposit

    if (diferencia <= 0) {
        return 'red'
    }
    else if (diferencia > 0 && diferencia <= 300) {
        return 'yellow'
    }
    else {
        return 'green'
    }
}

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
                                        <p>${element.first.base}<span>${element.first.base}</span></p>
                                        <span>&nbsp;-&nbsp;</span>
                                        <p>${element.best.base.abbr} <span>${element.best.base.crypto_name}</span></p>
                                    </div>
                                    <span >${element.first.price}</span>
                                    <a href="${exchangeInfo.generateConvertLink(element.best.base.abbr, element.first.base)}" target="_blank" class="btn btn_purple btn_nocard">Купить</a>
                                </div>
                                </div>

                                <div class="token-links__second-step">
                                    <div class="token-links__wrapper">
                                        <p class="token-links__item-title">${element.best.exchange_info.exchange_name}</p>
                                        <div class="token-links__item-content">
                                            <div class="token-links__token-pair">
                                                <p>${element.best.base.abbr}<span>${element.best.base.crypto_name}</span></p>
                                                <span>&nbsp;-&nbsp;</span>
                                                <p>${element.best.quote.abbr} <span>${element.best.quote.crypto_name}</span></p>
                                            </div>
                                            <span>${element.best.price}</span>
                                            <a href="https://www.bestchange.ru/click.php?id=${element.best.exchange_info.exchange_id}" target="_blank" class="btn btn_purple btn_nocard">Обмен</a>
                                        </div>
                                        <div class="token-links__arrow close"></div>
                                    </div>
                                    <div class="token-links__info hidden">
                                        <div class="token-links__info-wrapper">
                                            <p>Мин. лимиты <span>${element.best.lim_min}</span></p>
                                            <p>Резервы <span>${element.best.available}</span></p>
                                            <p>Отзывы <span>${element.best.positive_reviews}/${element.best.negative_reviews}</span></p>
                                            <p>Рейтинг <span>${element.best.exchange_info.info_star}</span></p>
                                            <p>Доп. проверка<span>${checkValue(element.best.exchange_info.info_verification)}</span></p>
                                            <p>Юр. регистрация<span>${checkValue(element.best.exchange_info.info_registration)}</span></p>
                                        </div>
                                    </div>
                                </div>

                                <div class="token-links__third-step">
                                    <p class="token-links__item-title">${element.exchange}</p>
                                    <div class="token-links__item-content">
                                        <div class="token-links__token-pair">
                                            <p>${element.best.quote.abbr}<span>${element.best.quote.crypto_name}</span></p>
                                            <span>&nbsp;-&nbsp;</span>
                                            <p>${element.second.quote} <span>${element.second.quote}</span></p>
                                        </div>
                                        <span class = "${checkDeposit(element.second.price, element.second.qty)}">${element.second.price}</span>
                                        <a href="${exchangeInfo.generateConvertLink(element.best.quote.abbr, element.second.quote)}" target="_blank" class="btn btn_purple btn_nocard btn_nocard_sell">Продать</a>
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

                    //************* temp Favorite *****************
                    let favoriteFlag = 0;
                    function changeFavoriteBtn() {
                        if (favoriteFlag == 1) {
                            return `<svg class="link-content__favorite_add link-content__favorite_delete" data-favorite="delete" version="1.0" xmlns="http://www.w3.org/2000/svg"
                            width="1280.000000pt" height="1216.000000pt" viewBox="0 0 1280.000000 1216.000000"
                            preserveAspectRatio="xMidYMid meet">
                           <g transform="translate(0.000000,1216.000000) scale(0.100000,-0.100000)"
                           fill="#FFF200" stroke="none">
                           <path d="M5890 10598 c-332 -755 -736 -1674 -898 -2043 -161 -368 -295 -671
                           -297 -673 -2 -2 -308 -25 -682 -52 -373 -27 -1054 -76 -1513 -109 -459 -34
                           -1087 -79 -1395 -101 -308 -22 -585 -43 -615 -46 l-54 -6 49 -47 c28 -25 336
                           -300 684 -611 349 -311 806 -718 1016 -905 1267 -1130 1560 -1391 1572 -1400
                           17 -13 74 228 -542 -2265 -256 -1036 -464 -1887 -463 -1890 2 -4 869 499 1928
                           1117 1058 618 1931 1122 1940 1120 8 -2 398 -242 865 -532 468 -291 1165 -724
                           1550 -963 385 -239 811 -504 947 -588 135 -85 249 -154 253 -154 4 0 4 17 0
                           38 -6 34 -411 1897 -776 3568 -87 402 -159 738 -159 747 0 13 649 563 2997
                           2542 258 217 261 220 230 227 -18 4 -1011 104 -2207 223 -1196 119 -2184 220
                           -2196 225 -15 6 -62 111 -199 446 -98 242 -412 1013 -697 1714 -285 701 -564
                           1388 -620 1525 -56 138 -104 253 -108 258 -3 4 -278 -610 -610 -1365z"/>
                           </g>
                           </svg>
                           `
                        }
                        else if (favoriteFlag == 0) {
                            return `<svg class="link-content__favorite_add" data-favorite="add" version="1.0" xmlns="http://www.w3.org/2000/svg"
                            width="1280.000000pt" height="1216.000000pt" viewBox="0 0 1280.000000 1216.000000"
                            preserveAspectRatio="xMidYMid meet">
                           <g transform="translate(0.000000,1216.000000) scale(0.100000,-0.100000)"
                           fill="none" stroke="#fff">
                           <path d="M5890 10598 c-332 -755 -736 -1674 -898 -2043 -161 -368 -295 -671
                           -297 -673 -2 -2 -308 -25 -682 -52 -373 -27 -1054 -76 -1513 -109 -459 -34
                           -1087 -79 -1395 -101 -308 -22 -585 -43 -615 -46 l-54 -6 49 -47 c28 -25 336
                           -300 684 -611 349 -311 806 -718 1016 -905 1267 -1130 1560 -1391 1572 -1400
                           17 -13 74 228 -542 -2265 -256 -1036 -464 -1887 -463 -1890 2 -4 869 499 1928
                           1117 1058 618 1931 1122 1940 1120 8 -2 398 -242 865 -532 468 -291 1165 -724
                           1550 -963 385 -239 811 -504 947 -588 135 -85 249 -154 253 -154 4 0 4 17 0
                           38 -6 34 -411 1897 -776 3568 -87 402 -159 738 -159 747 0 13 649 563 2997
                           2542 258 217 261 220 230 227 -18 4 -1011 104 -2207 223 -1196 119 -2184 220
                           -2196 225 -15 6 -62 111 -199 446 -98 242 -412 1013 -697 1714 -285 701 -564
                           1388 -620 1525 -56 138 -104 253 -108 258 -3 4 -278 -610 -610 -1365z"/>
                           </g>
                           </svg>
                        `
                        }
                    }

                    if (document.querySelector('.sidebar__favorite_nocard input').checked) {
                        // console.log('favorite_1');
                        // if (!document.querySelector('.favorite__item')) {
                        //     continue
                        // }
                        filterArr = Array.from(document.querySelectorAll('.favorite__item:has(input:checked)'))
                        // debugger
                        if (
                            (filterArr.find((element) => { return element.dataset.firstcoin == item['0'].best.quote.abbr })) && (filterArr.find((element) => { return element.dataset.secondcoin == item['0'].best.base.abbr }))
                        ) {
                            favoriteFlag = 1
                        } else {
                            continue
                        }
                    }
                    else {
                        if (localStorage.getItem('nocard_favorite')) {
                            const favoriteArr = JSON.parse(localStorage.getItem('nocard_favorite'))

                            if (favoriteArr.find((itemFavorite) => {
                                return ((itemFavorite.firstCoin == item['0'].best.quote.abbr) && (itemFavorite.secondCoin == item['0'].best.base.abbr))
                            })) {
                                favoriteFlag = 1
                            }
                        }
                    }

                    //*************************************************
                    let titleSection = document.createElement('div')
                    titleSection.classList.add('token-links_group')
                    // titleSection.dataset.firstcoin = item['0'].best.quote.abbr
                    // titleSection.dataset.secondcoin = item['0'].best.base.abbr
                    titleSection.innerHTML = `
                    <div class="token-links_group-title" data-firstcoin="${item['0'].best.quote.abbr}" data-secondcoin = "${item['0'].best.base.abbr}">${item['0'].first.base} - <span>${item['0'].best.base.abbr} </span> - <span> ${item['0'].best.quote.abbr}</span> - ${item['0'].second.quote}
                    ${changeFavoriteBtn()}
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
                        if ((Number(limitFilterValue) >= element.best.lim_min)) {
                            let row = document.createElement('div')
                            row.classList.add('token-links__item')
                            row.innerHTML = `
                                <div class="token-links__row">
                                <div class="token-links__first-step">
                                     <p class="token-links__item-title">${element.exchange}</p>
                                    <div class="token-links__item-content">
                                        <div class="token-links__token-pair">
                                            <p>${element.first.base}<span>${element.first.base}</span></p>
                                            <span>&nbsp;-&nbsp;</span>
                                            <p>${element.best.base.abbr} <span>${element.best.base.crypto_name}</span></p>
                                        </div>
                                        <div class = "token-links__price">
                                            <span class= "${checkDeposit(element.first.price, element.first.qty)}">${element.first.price}</span>
                                            <p>${element.first.price_full}</p>
                                        </div>
                                        <a href="${exchangeInfo.createConvertLink(element.exchange, element.first.base, element.best.base.abbr)}" target="_blank" class="btn btn_purple btn_nocard">Купить</a>
                                    </div>
                                    </div>

                                    <div class="token-links__second-step">
                                        <div class="token-links__wrapper">
                                            <p class="token-links__item-title">${element.best.exchange_info.exchange_name}</p>
                                            <div class="token-links__item-content">
                                                <div class="token-links__token-pair">
                                                    <p>${element.best.base.abbr}<span>${element.best.base.crypto_name}</span></p>
                                                    <span>&nbsp;-&nbsp;</span>
                                                    <p>${element.best.quote.abbr} <span>${element.best.quote.crypto_name}</span></p>
                                                </div>
                                                <div class = "token-links__price">
                                                <span>${element.best.price}</span>
                                                    <p>${element.best.price_full}</p>
                                                </div>
                                                
                                                <a href="https://www.bestchange.ru/click.php?id=${element.best.exchange_info.exchange_id}" target="_blank" class="btn btn_purple btn_nocard">Обмен</a>
                                            </div>
                                            <div class="token-links__arrow close"></div>
                                        </div>
                                        <div class="token-links__info hidden">
                                            <div class="token-links__info-wrapper">
                                                <p>Мин. лимиты <span>${element.best.lim_min}</span></p>
                                                <p>Резервы <span>${element.best.available}</span></p>
                                                <p>Отзывы <span>${element.best.positive_reviews}/${element.best.negative_reviews}</span></p>
                                                <p>Рейтинг <span>${element.best.exchange_info.info_star}</span></p>
                                                <p>Доп. проверка<span>${checkValue(element.best.exchange_info.info_verification)}</span></p>
                                                <p>Юр. регистрация<span>${checkValue(element.best.exchange_info.info_registration)}</span></p>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="token-links__third-step">
                                        <p class="token-links__item-title">${element.exchange}</p>
                                        <div class="token-links__item-content">
                                            <div class="token-links__token-pair">
                                                <p>${element.best.quote.abbr}<span>${element.best.quote.crypto_name}</span></p>
                                                <span>&nbsp;-&nbsp;</span>
                                                <p>${element.second.quote} <span>${element.second.quote}</span></p>
                                            </div>
                                        <div class = "token-links__price">
                                            <span class="${checkDeposit(element.second.price, element.second.qty)}">${element.second.price}</span>
                                            <p>${element.second.price_full}</p> 

                                        </div>
                                            <a href="${exchangeInfo.createConvertLink(element.exchange, element.second.quote, element.best.quote.abbr)}" target="_blank" class="btn btn_purple btn_nocard btn_nocard_sell">Продать</a>
                                        </div>
                                    </div>
                                    <div class="token-links__percent">${element.spread}%</div>
                                    <div class="token-links__profit">
                                ${((Number(deposit) + (element.spread * Number(deposit)) / 100) - Number(deposit)).toFixed(1)} $
                                    
                                    </div>
                                </div>
                            `
                            pairRows.push(row)
                        }
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
//             `<input id="checkbox-token-pair-${item[0].ad_give_second.abbr}${item[0].best.quote.abbr}-nocard" name="token-pair" type="checkbox">
//         <label for="checkbox-token-pair-${item[0].ad_give_second.abbr}${item[0].best.quote.abbr}-nocard">${item['0'].first.base} - ${item[0].ad_give_second.abbr} - ${item[0].best.quote.abbr} - ${item[0].ad_get_second}</label>
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
    console.log(event.target);
    if (event.target.classList.contains('token-links__arrow')) {
        toggleInfo(event.target)
    }
    else if (event.target.dataset.favorite == 'add') {
        addToFavorite(event.target)
    }
    else if (event.target.parentNode.parentNode.dataset.favorite == 'add') {
        addToFavorite(event.target.parentNode.parentNode)
    }
    else if (event.target.dataset.favorite == 'delete') {
        deleteFavoriteItem(event.target)
    }
    else if (event.target.parentNode.dataset.favorite == 'delete') {
        deleteFavoriteItem(event.target.parentNode)
    }
    else if (event.target.parentNode.parentNode.dataset.favorite == 'delete') {
        deleteFavoriteItem(event.target.parentNode.parentNode)
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
        else if (event.target.classList.contains('favorite__del-btn')) {
            deleteFavoriteItem(event.target)
        }
        else {
            element.hide()
        }
    })
})

//Favorite
// document.querySelector('.token-links').addEventListener('click', (event) => {
//     if (event.target.classList.contains('link-content__favorite_add')) {
//         addFavorite(event.target.parentElement)
//     }
//     else if (event.target.classList.contains('link-content__favorite_del')) {
//         delFavorite(event.target.parentElement)
//     }
// })
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
let favoriteNodeBlock = document.querySelector('.sidebar__favorite-block')

function addToFavorite(element) {
    let data
    if (localStorage.getItem('nocard_favorite')) {
        data = JSON.parse(localStorage.getItem('nocard_favorite'))
    } else {
        data = []
    }
    if (data.find((dataElement) => {
        return dataElement.secondCoin == element.parentNode.dataset.secondcoin && dataElement.firstCoin == element.parentNode.dataset.firstcoin
    }) == undefined) {
        data.push({
            firstCoin: element.parentNode.dataset.firstcoin,
            secondCoin: element.parentNode.dataset.secondcoin,
            isChecked: 'on'
        })
        localStorage.setItem('nocard_favorite', JSON.stringify(data))
        element.classList.add('link-content__favorite_delete')
        element.dataset.favorite = 'delete'
        refreshFavorite()
    }
}

function refreshFavorite() {
    if (localStorage.getItem('nocard_favorite')) {

        favoriteNodeBlock.innerHTML = ''
        // debugger
        let favoriteArr = JSON.parse(localStorage.getItem('nocard_favorite'))
        favoriteArr.forEach((element) => {
            // let checked = ''
            // if (element.isChecked == 'on') {
            //     checked = 'checked'
            // }
            let node = document.createElement('div')
            node.classList.add('favorite__item')
            node.dataset.secondcoin = element.secondCoin
            node.dataset.firstcoin = element.firstCoin
            node.innerHTML = `
        <label for="checkbox-favorite-${element.secondCoin}-${element.firstCoin}">USDT-${element.secondCoin}-${element.firstCoin}-USDT</label>
        <div class="favorite__del-btn" data-favorite="delete">
        <div></div>
        <div></div>
        </div>
        `
            let inputNode = document.createElement('input')
            inputNode.setAttribute('id', `checkbox-favorite-${element.secondCoin}-${element.firstCoin}`)
            inputNode.setAttribute('type', `checkbox`)
            inputNode.setAttribute('name', `favorite-item`)
            if (element.isChecked == 'on') {
                inputNode.checked = true;
            }
            node.insertAdjacentElement('afterbegin', inputNode)


            favoriteNodeBlock.insertAdjacentElement("beforeend", node)
        })
    }
}
function changeFavoriteFilter(input) {
    let value = ''
    if (input.checked) {
        value = 'on'
    } else {
        value = 'off'
    }
    let favoriteArr = JSON.parse(localStorage.getItem('nocard_favorite'))
    favoriteArr[favoriteArr.findIndex((element) => {
        return (element.secondCoin == input.parentNode.dataset.secondcoin) && (element.firstCoin == input.parentNode.dataset.firstcoin)
    })].isChecked = value
    localStorage.setItem('nocard_favorite', JSON.stringify(favoriteArr))
    createFormObject()
}

function favoriteBlockCheck() {
    if (document.querySelector('#checkbox-favorite:checked')) {
        if (!document.querySelector('.sidebar__favorite-block').classList.contains('show')) {
            document.querySelector('.sidebar__favorite-block').classList.add('show')
        }
    } else {
        if (document.querySelector('.sidebar__favorite-block').classList.contains('show')) {
            document.querySelector('.sidebar__favorite-block').classList.remove('show')
        }
    }
}
function deleteFavoriteItem(input) {
    let favoriteArr = JSON.parse(localStorage.getItem('nocard_favorite'))

    let indexDelElement = favoriteArr.findIndex((element) => {
        return ((element.secondCoin == input.parentNode.dataset.secondcoin) && (element.firstCoin == input.parentNode.dataset.firstcoin))
    })
    console.log(indexDelElement);

    if (indexDelElement != -1) {
        favoriteArr.splice(indexDelElement, 1)
        localStorage.setItem('nocard_favorite', JSON.stringify(favoriteArr))
    }

    input.classList.remove('link-content__favorite_delete')
    input.dataset.favorite = 'add'
    if (document.querySelector('.sidebar__favorite_nocard input').checked) {
        createFormObject()
    }
    refreshFavorite()
    // document.querySelector('.sidebar__favorite-block').removeChild(input.parentNode)
}
refreshFavorite()

