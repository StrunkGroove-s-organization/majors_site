// Подсветка кнопки в header
Array.from(document.querySelectorAll('.menu_item')).forEach(element => element.classList.remove('active'));
document.querySelector('[data-menu="calc"]').classList.add('active')

const form = document.querySelector('.calc-p2p__form')
const deposit = form.querySelector('input[data-input="p2p_deposit"]')

form.addEventListener('change', () => {
    console.log('change');
    calcProfit('p2p2')
    calcProfit('p2p3')
})

function calcCommission(calcType) {
    let commission = 0;
    if (calcType == 'p2p2') {
        Array.from(form.querySelectorAll('input[data-input="p2p2_commission"]')).forEach((item) => {
            commission = commission + Number(item.value)
        })
    }
    else if (calcType == 'p2p3') {
        Array.from(form.querySelectorAll('input[data-input="p2p3_commission"]')).forEach((item) => {
            commission = commission + Number(item.value)
        })
    }
    return commission
}

function calcProfit(section) {
    const buyPrice = Number(form.querySelector(`input[data-input="${section}_price_buy"]`).value)
    const sellPrice = Number(form.querySelector(`input[data-input="${section}_price_sell"]`).value)
    const spread = form.querySelector(`input[data-input="${section}_spred"]`)
    const profit = form.querySelector(`input[data-input="${section}_profit"]`)

    const comission = calcCommission(section)
    let changePrice = 0

    if (form.querySelector(`input[data-input="${section}_price_change"]`)) {
        changePrice = Number(form.querySelector(`input[data-input="${section}_price_change"]`).value)
    } else {
        changePrice = 1;
    }
    let spredValue = (sellPrice / (buyPrice * changePrice) - 1) * 100 - comission
    if (isNaN(spredValue) || !isFinite(spredValue)) {
        spredValue = 0
    }
    spread.value = spredValue.toFixed(5)
    profit.value = (Number(deposit.value) * Number(spread.value) / 100).toFixed(5)
}

calcProfit('p2p2')
calcProfit('p2p3')