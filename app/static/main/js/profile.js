
document.addEventListener("DOMContentLoaded", () => {
    const rateGroup = document.querySelector('.premium__rate-select')
    const description = document.querySelector('.premium__description span')

    changeDescription(rateGroup.querySelector('input:checked'))

    rateGroup.addEventListener('change', (event) => {
        changeDescription(event.target)
    })

    function changeDescription(element) {
        if (element == document.querySelector('#radio-test-subscription')) {
            description.innerHTML = ''
            description.insertAdjacentText("afterbegin", '10$ - доступ на 2 дня')
        }
        else if (element == document.querySelector('#radio-profi-subscription')) {
            description.innerHTML = ''
            description.insertAdjacentText("afterbegin", '28$ - доступ на 1 месяц')
        }
        else if (element == document.querySelector('#radio-infinity-subscription')) {
            description.innerHTML = ''
            description.insertAdjacentText("afterbegin", '500$ - доступ без ограничений')
        }
        // else if (element == document.querySelector('#radio-1000_infinity_500-subscription')) {
        //     description.innerHTML = ''
        //     description.insertAdjacentText("afterbegin", 'unset')
        // }
    }
})


const form = document.querySelector('.premium form');
const criptoBtn = document.querySelector("[data-pay='cripto']");
const fiatBtn = document.querySelector("[data-pay='fiat']");
const payBlock = document.querySelector('.pay-block');

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