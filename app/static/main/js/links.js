const exchangeInfo = {
   binance: {
      img: '/static/main/img/exchange/binance.png',
      baseUrl: "https://p2p.binance.com/",

      generateLink(trade, token, fiat) {
         if (trade == 'buy') {
            return `${this.baseUrl}ru/trade/all-payments/` + `${token.trim()}?fiat=` + `${fiat.trim()}`
         } else {
            return `${this.baseUrl}ru/trade/sell/` + `${token.trim()}?fiat=` + `${fiat.trim()}&payment=` + `all-payments`
         }
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/advertiserDetail?advertiserNo=${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         // return `https://www.binance.com/ru/convert/${firstToken}/${secondToken}`
         return `https://www.binance.com/ru/trade/${secondToken}_${firstToken}?theme=dark&type=spot`
      }
   },
   huobi: {
      img: '/static/main/img/exchange/huobi.png',
      baseUrl: "https://www.huobi.com/",
      generateLink(trade, token, fiat) {
         return `${this.baseUrl}en-us/fiat-crypto/trade/` + `${trade}-` + `${token.trim()}-` + `${fiat.trim()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru-ru/fiat-crypto/trader/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru-ru/trade/${secondToken.toLowerCase()}_${firstToken.toLowerCase()}?type=spot`
      }
   },
   bybit: {
      img: '/static/main/img/exchange/bybit.png',
      baseUrl: "https://www.bybit.com/",

      generateLink(trade, token, fiat) {
         if (trade == 'buy') {
            return `${this.baseUrl}fiat/trade/otc/?actionType=1&token=` + `${token.trim()}&fiat=` + `${fiat.trim()}&paymentMethod=`
         } else {
            return `${this.baseUrl}fiat/trade/otc/?actionType=0&token=` + `${token.trim()}&fiat=` + `${fiat.trim()}&paymentMethod=`
         }
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}fiat/trade/otc/profile/${id}/${token}/${fiat}/item`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru-RU/trade/spot/${secondToken}/${firstToken}`
      }
   },
   okx: {
      img: '/static/main/img/exchange/okx.png',
      baseUrl: "https://www.okx.cab/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru/p2p-markets/` + `${fiat.trim()}/` + `${trade}-` + `${token.trim()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/p2p/ads-merchant?publicUserId=${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru/trade-spot/${secondToken}-${firstToken}`
      }
   },
   bitget: {
      img: '/static/main/img/exchange/bitget.png',
      baseUrl: "https://www.bitget.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru/p2p-trade/` + `${trade}/` + `${token.trim()}?fiatName=` + `${fiat.trim()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/p2p-trade/user/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru/spot/${secondToken}${firstToken}?type=spot`
      }
   },
   garantex: {
      img: '/static/main/img/exchange/garantex.png',
      baseUrl: "https://garantex.org/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}trading/` + `${token.trim().toLowerCase()}` + `${fiat.trim().toLowerCase()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return this.generateLink(buy_sell, token, fiat)
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}trading/` + `${firstToken.trim().toLowerCase()}` + `${secondToken.trim().toLowerCase()}`
      }
   },
   bitpapa: {
      img: '/static/main/img/exchange/bitpapa.png',
      baseUrl: "https://bitpapa.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}` + `${trade}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/user/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru`
      }
   },
   beribit: {
      img: '/static/main/img/exchange/beribit.svg',
      baseUrl: "https://beribit.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}exchange/spots/` + `${token.trim()}_` + `${fiat.trim()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/user/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}exchange/spots/${firstToken}_${secondToken}`
      }
   },
   'hodl hodl': {
      img: '/static/main/img/exchange/hodl.png',
      baseUrl: "https://hodlhodl.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}offers/` + `${trade}?filters%5Bcurrency_code%5D=` + `${fiat.trim()}&pagination%5Boffset%5D=0`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}offers/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}`

      }
   },
   mexc: {
      img: '/static/main/img/exchange/mexc.png',
      baseUrl: "https://otc.mexc.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru-RU`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru-RU/merchant?id=${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru-RU/exchange/${firstToken}_${secondToken}?_from=header`
      }
   },
   kucoin: {
      img: '/static/main/img/exchange/kucoin.png',
      baseUrl: "https://www.kucoin.com/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru/otc/` + `${trade}/` + `${token.trim()}-` + `${fiat.trim()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return this.generateLink(buy_sell, token, fiat)
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru/trade/${secondToken}-${firstToken}`
      }
   },
   'gateio': {
      img: '/static/main/img/exchange/gateio.png',
      baseUrl: "https://www.gate.io/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru/c2c/market`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return `${this.baseUrl}ru/c2c/user/${id}`
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru/trade/${secondToken}_${firstToken}`
      }
   },
   totalcoin: {
      img: '/static/main/img/exchange/totalcoin.png',
      baseUrl: "https://totalcoin.io/",

      generateLink(trade, token, fiat) {
         return `${this.baseUrl}ru/offers/` + `${trade}/` + `${token.trim().toLowerCase()}/` + `${fiat.trim().toLowerCase()}`
      },
      generateExchangeLink(id, buy_sell, token, fiat) {
         return this.generateLink(buy_sell, token, fiat)
      },
      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}ru`
      }
   },
   pancake: {
      img: '/static/main/img/exchange/pancake.png',
      baseUrl: 'https://pancakeswap.finance/',

      generateConvertLink(firstToken, secondToken) {
         return `${this.baseUrl}/swap`
      }
   },
   unname: {
      img: '/static/main/img/payments/unname.png'
   },

   setSrc(name) {
      if ((this[name.toLowerCase()])) {
         return this[name.toLowerCase()].img
      }
      else {
         return this.unname.img
      }
   },

   createLink(exchange, id, buy_sell, token, fiat) {
      if (id !== '#') {
         return this[exchange.toLowerCase()].generateExchangeLink(id, buy_sell.toLowerCase(), token, fiat)
      }
      else {
         return this[exchange.toLowerCase()].generateLink(buy_sell.toLowerCase(), token, fiat)
      }
   },
   createConvertLink(exchange, quoteToken, baseToken) {
      return this[exchange.toLowerCase()].generateConvertLink(quoteToken, baseToken)
   }
}



const paymentImg = {
   Raiffeisenbank: {
      img: '/static/main/img/payments/raiffeisen.png'
   },
   Tinkoff: {
      img: '/static/main/img/payments/tinkoff.png'
   },
   Rosbank: {
      img: '/static/main/img/payments/rosselhoz.png'
   },
   РоссельхозБанк: {
      img: '/static/main/img/payments/rosselhoz.png'
   },
   'MTS-Bank': {
      img: '/static/main/img/payments/mts.png'
   },
   'Alfa Bank': {
      img: '/static/main/img/payments/alfa.png'
   },
   'Sber': {
      img: '/static/main/img/payments/sber.png'
   },
   'Gazprombank': {
      img: '/static/main/img/payments/gazprom.png'
   },
   'QIWI': {
      img: '/static/main/img/payments/qiwi.png'
   },
   'ЮMoney': {
      img: '/static/main/img/payments/umoney.png'
   },
   'Bank Transfer': {
      img: '/static/main/img/payments/transfer.png'
   },
   'Cash': {
      img: '/static/main/img/payments/cash.png'
   },
   'Post Bank': {
      img: '/static/main/img/payments/post.png'
   },
   'Home Credit Bank': {
      img: '/static/main/img/payments/homecredit.png'
   },
   'Home Credit Bank (Russia)': {
      img: '/static/main/img/payments/homecredit.png'
   },
   'SBP': {
      img: '/static/main/img/payments/sbp.png'
   },
   'VTB': {
      img: '/static/main/img/payments/vtb.png'
   },
   'Russia Standart Bank': {
      img: '/static/main/img/payments/russiastandart.png'
   },
   'Ak Bars Bank': {
      img: '/static/main/img/payments/AKBars.png'
   },
   'АкБарс Банк': {
      img: '/static/main/img/payments/AKBars.png'
   },
   'Перевод по номеру карты': {
      img: '/static/main/img/payments/card.png'
   },
   unname: {
      img: '/static/main/img/payments/unname.png'
   },

   setSrc(name) {
      if (this[name]) {
         return this[name].img
      }
      else {
         return this.unname.img
      }
   }
}