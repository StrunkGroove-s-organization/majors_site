
const form = document.querySelector('.premium form');
const criptoBtn = document.querySelector("[data-pay='cripto']");
const fiatBtn = document.querySelector("[data-pay='fiat']");
const payBlock = document.querySelector('.pay-block');
const profilePageBtn = document.querySelector('[data-page = "profile"]')
const referalPageBtn = document.querySelector('[data-page = "referal"]')

document.addEventListener("DOMContentLoaded", () => {
    const rateGroup = document.querySelector('.premium__rate-select')
    const description = document.querySelector('.premium__description span')

    changeDescription(rateGroup.querySelector('input:checked'))

    form.addEventListener('change', (event) => {
        // changeDescription(event.target)
        changeDescription(rateGroup.querySelector('input:checked'))

    })

    function changeDescription(element) {
        const criptoType = document.querySelector('.premium__period-select input:checked').value
        let infoText = ''
        description.innerHTML = ''

        if (element == document.querySelector('#radio-test-subscription')) {
            switch (criptoType) {
                case 'USDT_TRX':
                    infoText = '10$ - доступ на 2 дня'
                    break;
                case 'USDT_BSC':
                    infoText = '3$ - доступ на 2 дня'
                    break;
                case 'BNB':
                    infoText = '10$ - доступ на 2 дня'
                    break;

                default:
                    infoText = 'Error'
                    break;
            }
        }
        else if (element == document.querySelector('#radio-profi-subscription')) {
            switch (criptoType) {
                case 'USDT_TRX':
                    infoText = '28$ - доступ на 1 месяц'
                    break;
                case 'USDT_BSC':
                    infoText = '28$ - доступ на 1 месяц'
                    break;
                case 'BNB':
                    infoText = '28$ - доступ на 1 месяц'
                    break;

                default:
                    infoText = 'Error'
                    break;
            }
        }
        else if (element == document.querySelector('#radio-infinity-subscription')) {
            switch (criptoType) {
                case 'USDT_TRX':
                    infoText = '500$ - доступ без ограничений'
                    break;
                case 'USDT_BSC':
                    infoText = '500$ - доступ без ограничений'
                    break;
                case 'BNB':
                    infoText = '500$ - доступ без ограничений'
                    break;
                default:
                    infoText = 'Error'
                    break;
            }
        }
        description.insertAdjacentText("afterbegin", infoText)

        // else if (element == document.querySelector('#radio-1000_infinity_500-subscription')) {
        //     description.innerHTML = ''
        //     description.insertAdjacentText("afterbegin", 'unset')
        // }
    }
})




criptoBtn.addEventListener('click', () => {
    sendForm('cripto')
})

// fiatBtn.addEventListener('click', () => {
//     sendForm('fiat')
// })

function sendForm(paySelect) {
    let url
    if (paySelect == 'cripto') {
        url = '/payment_crypto/'
    } else if (paySelect == 'fiat') {
        url = '/payment_fiat/'
    }

    payBlock.innerHTML = `
                    <div class="container">
                        <div class="pay-block__wrapper">
                    <div class="pay-block__qr">
                        <img src="/static/main/img/preloader.gif" alt="">
                    </div>
                    <p>Сумма оплаты</p>
                    <div class="pay-block__summ"></div>
                    <p>Кошелек</p>
                    <div class="pay-block__hash"></div>
                    <a href="" class="pay-block__link inactive">
                        Oплатить с помощью
                    </a>
                </div>
            </div>
                    `

    return fetch(url,
        {
            method: "POST",
            body: new FormData(form),
        }).then((response) => {
            return response.json();
        }).then((responseData) => {
            payBlock.innerHTML = `
                    <div class="container">
                        <div class="pay-block__wrapper">
                    <div class="pay-block__qr">
                        <img src="${responseData.image}" alt="">
                    </div>
                    <p>Сумма оплаты</p>
                    <div class="pay-block__summ">${responseData.sum}</div>
                    <p>Кошелек</p>
                    <div class="pay-block__hash">${responseData.wallet_hash}</div>
                    <a href="${responseData.pay_url}" target="_blank" class="pay-block__link">
                        Оплатить с помощью сервиса Plisio
                    </a>
                </div>
            </div>
                    `

            document.querySelector('.pay-block__summ').addEventListener('click', () => {
                copySumm()
            })
            document.querySelector('.pay-block__hash').addEventListener('click', () => {
                copyWallet()
            })

        }).catch(() => {
            payBlock.innerHTML = `
        <div class="container">
            <div class="pay-block__wrapper">
        <div class="pay-block__qr_error">
           При запросе на сервис оплаты произошла ошибка. Попробуйте повторить запрос.
        </div>
        <p>Сумма оплаты</p>
        <div class="pay-block__summ"></div>
        <p>Кошелек</p>
        <div class="pay-block__hash"></div>
        <a href="" class="pay-block__link inactive">
            Oплатить с помощью
        </a>
    </div>
</div>
        `
        })
}

function copySumm() {
    navigator.clipboard.writeText(document.querySelector('.pay-block__summ').textContent)
        .then(() => {
            // console.log('Text copied to clipboard');
        })
        .catch(err => {
            console.error('Error in copying text: ', err);
        });
    showCopyMessage()
}

function copyWallet() {
    navigator.clipboard.writeText(document.querySelector('.pay-block__hash').textContent)
        .then(() => {
            // console.log('Text copied to clipboard');
        })
        .catch(err => {
            console.error('Error in copying text: ', err);
        });
    showCopyMessage()
}

function showCopyMessage() {
    const $body = document.querySelector('body')
    const copyMessage = document.createElement('div');
    copyMessage.classList.add('copy-message')
    copyMessage.textContent = 'Скопировано в буфер'
    $body.insertAdjacentElement("afterbegin", copyMessage);
    setTimeout(() => {
        $body.removeChild(copyMessage)
    }, 1000);
}


profilePageBtn.addEventListener('click', () => {
    referalPageBtn.classList.remove('active')
    document.querySelector('.page_referal').classList.remove('active')
    profilePageBtn.classList.add('active')
    document.querySelector('.page_profile').classList.add('active')
})

referalPageBtn.addEventListener('click', () => {
    referalPageBtn.classList.add('active')
    document.querySelector('.page_referal').classList.add('active')
    profilePageBtn.classList.remove('active')
    document.querySelector('.page_profile').classList.remove('active')
})

const linkBtn = document.querySelector('.referal__info-value_link')
const referalLink = String(linkBtn.textContent).replaceAll(' ', '')

linkBtn.addEventListener('click', () => {
    window.navigator.clipboard.writeText(referalLink)
    showCopyMessage()
})