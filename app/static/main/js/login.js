//бургер-меню
const burgerBtn = document.querySelector('.burger__btn')
const burgerMenu = document.querySelector('.header__menu-block')
burgerBtn.addEventListener('click', () => {
   burgerBtn.classList.toggle('active')
   burgerMenu.classList.toggle('active')
})


//кнопки в баннерах
if (document.querySelector('.rate__btn-block')) {
   if (document.querySelector('[data-link = "noauth"]')) {
      const rateLinkArr = document.querySelectorAll('[data-link = "noauth"]')

      rateLinkArr.forEach(element => {
         element.addEventListener('click', openRegBlock)
      })
   }
}

if (document.querySelector('.main-screen')) {
   if (document.querySelector('[data-screen = "noauth"]')) {
      const mainScreenLink = document.querySelector('[data-screen = "noauth"]')
      mainScreenLink.addEventListener('click', openRegBlock)
   }
}
if (document.querySelector('.screener')) {
   if (document.querySelector('[data-screener = "noauth"]')) {
      const mainScreenerLink = document.querySelector('[data-screener = "noauth"]')
      mainScreenerLink.addEventListener('click', openRegBlock)
   }
}

function changeLinks() {
   if (document.querySelector('.rate__btn-block')) {
      const rateBtnBlockArr = document.querySelectorAll('.rate__btn-block')
      const rateLinkArr = document.querySelectorAll('[data-link = "noauth"]')
      rateLinkArr.forEach(element => {
         element.removeEventListener('click', openRegBlock)
      })
      rateBtnBlockArr.forEach(element => {
         element.innerHTML = '<a href="/profile/#premium" class="btn btn_white btn_rates">Оформить подписку</a>'
      })
   }

   if (document.querySelector('.main-screen')) {
      const mainScreenBtnBlock = document.querySelector('.main-screen__btn-block')
      const mainScreenLink = document.querySelector('[data-screen = "noauth"]')
      mainScreenLink.removeEventListener('click', openRegBlock)

      mainScreenBtnBlock.innerHTML = '<a href="/profile/#premium" class="btn btn_orange btn_main-screen">Попробовать от 5$</a>'
   }

   if (document.querySelector('.screener')) {
      const mainScreenerBtnBlock = document.querySelector('.screener__btn-block')
      const mainScreenerLink = document.querySelector('[data-screener = "noauth"]')
      mainScreenerLink.removeEventListener('click', openRegBlock)

      mainScreenerBtnBlock.innerHTML = '<a href="/profile/#premium" class="screener__btn btn btn_white">Начать</a>'
   }

}


//модальное окно  регистрация/логин
const modal = document.querySelector('.modal');
const closeBtn = document.querySelector('.modal__close');
const loginBtn = document.querySelector('.btn[data-link="login"]');
const regBtn = document.querySelector('.btn[data-link="reg"]');
const loginBlock = document.querySelector('.modal__login');
const regBlock = document.querySelector('.modal__registration');
const resetBlock = document.querySelector('.modal__reset');
const resetBtn = document.querySelector('.modal__reset-pass');
const messageBlock = document.querySelector('.modal__message');


if (loginBtn) {
   loginBtn.addEventListener('click', openLoginBlock)
}

if (regBtn) {
   regBtn.addEventListener('click', openRegBlock)
}
function openLoginBlock() {
   openModal(loginBlock);
   burgerBtn.classList.remove('active')
   burgerMenu.classList.remove('active')
   loginBtn.removeEventListener('click', openLoginBlock)

}
function openRegBlock() {
   openModal(regBlock);
   burgerBtn.classList.remove('active')
   burgerMenu.classList.remove('active')
   regBtn.removeEventListener('click', openRegBlock)
}

function openModal(select) {
   modal.classList.add('active');
   changeModalSection(select)
   closeBtn.addEventListener('click', closeModal);
   loginForm.addEventListener('submit', loginSend);
   regForm.addEventListener('submit', regisrationSend);
   emailResetForm.addEventListener('submit', resetPass);
   emailResetBackBtn.addEventListener('click', backToLogin);

}

function closeModal() {
   closeBtn.removeEventListener('click', closeModal);
   modal.classList.remove('active');
   setTimeout(() => {
      loginBlock.classList.remove('active');
      regBlock.classList.remove('active');
      messageBlock.classList.remove('active');

      loginForm.removeEventListener('submit', loginSend);
      regForm.removeEventListener('submit', regisrationSend);
      emailResetForm.removeEventListener('submit', resetPass);
      emailResetBackBtn.removeEventListener('click', backToLogin);

      loginBtn.addEventListener('click', openLoginBlock)
      regBtn.addEventListener('click', openRegBlock)
   }, 200)
}
function changeModalSection(section) {
   loginBlock.classList.remove('active');
   regBlock.classList.remove('active');
   resetBlock.classList.remove('active');
   section.classList.add('active');
   loginForm.reset();
   regForm.reset();
   emailResetForm.reset();
   loginBlock.removeEventListener('click', selectBlock);
   regBlock.removeEventListener('click', selectBlock);
   resetBtn.removeEventListener('click', selectBlock);
   if (section != resetBlock) {
      section.querySelector('.modal__select-block').addEventListener('click', selectBlock);
   }
   if (section == loginBlock) {
      resetBtn.addEventListener('click', selectBlock);
   }
}

function selectBlock(event) {
   if ((event.target.dataset.btn == "login") || (event.target.parentNode.dataset == "login")) {
      changeModalSection(loginBlock)
   } else if ((event.target.dataset.btn == "registration") || (event.target.parentNode.dataset == "registration")) {
      changeModalSection(regBlock)
   } else if ((event.target.dataset.btn == "reset") || (event.target.parentNode.dataset == "reset")) {
      changeModalSection(resetBlock)
   }
}



// Отправка формы регистрации

const regForm = document.querySelector('.modal__registration form');
const regErrList = document.querySelector('.modal__registration .error-list');

// regForm.addEventListener('submit', regisrationSend);

function regisrationSend(event) {
   event.preventDefault()
   url = '/registration/';
   return fetch(url,
      {
         method: "POST",
         headers: { "X-CSRFToken": `${document.querySelector('input[name = "csrfmiddlewaretoken"]').value}` },
         body: new FormData(regForm),
      }).then((response) => {
         if (response.status == 400) {
            return response.json()
         }
         else {
            return response.text()
         }
      }).then((data) => {
         console.log(typeof (data));
         if (typeof (data) == 'object') {
            regErrList.innerHTML = ''
            for (const key in data) {
               if (Object.hasOwnProperty.call(data, key)) {
                  const element = data[key];
                  console.log(element);

                  element.forEach(item => {
                     let err = document.createElement('p');
                     err.innerHTML = item;
                     regErrList.insertAdjacentElement("beforeend", err)
                  });
               }
            }
         } else if (typeof (data) == 'string') {
            changeHeader(data)
            changeLinks()
            if (document.querySelector('[data-page="spreadtable"]')) {
               refreshToken(data);
            }
         }
      }).catch(error => {
         console.error('error', error.message);
      });
}

// Отправка формы логина

const loginForm = document.querySelector('.modal__login form');
const loginErrList = document.querySelector('.modal__login .error-list');

// loginForm.addEventListener('submit', loginSend);

function loginSend(event) {
   event.preventDefault()
   url = '/login/';
   return fetch(url,
      {
         method: "POST",
         body: new FormData(loginForm),
      }).then((response) => {
         if (response.status == 400) {
            return response.json()
         }
         else {
            return response.text()
         }
      }).then((data) => {
         if (typeof (data) == 'object') {
            loginErrList.innerHTML = ''
            for (const key in data) {
               if (Object.hasOwnProperty.call(data, key)) {
                  const element = data[key];
                  console.log(element);

                  element.forEach(item => {
                     let err = document.createElement('p');
                     err.innerHTML = item;
                     loginErrList.insertAdjacentElement("beforeend", err)
                  });
               }
            }
         } else if (typeof (data) == 'string') {
            changeHeader(data)
            changeLinks()
            if (document.querySelector('input[name="csrfmiddlewaretoken"]')) {
               refreshToken(data);
            }
         }
      }).catch(error => {
         console.log('error: ' + error);
      });
}
function changeHeader(newPage) {
   let parser = new DOMParser();
   let newHeaderBtnBlock = parser.parseFromString(newPage, "text/html").querySelector('.header__btn-block');
   document.querySelector('.header__menu-block').removeChild(document.querySelector('.header__btn-block'))
   document.querySelector('.header__menu-block').insertAdjacentElement("beforeend", newHeaderBtnBlock)
   closeModal()
}


// Отправка формы восстановления пароля
const emailResetForm = document.querySelector('.modal__reset form');
const emailResetBackBtn = document.querySelector('.modal_back-reset');

// emailResetForm.addEventListener('submit', resetPass);

function resetPass(event) {
   event.preventDefault()
   url = '/password_reset_request/';
   return fetch(url,
      {
         method: "POST",
         body: new FormData(emailResetForm),
      }).then((response) => {
         return response.json()
      }).then((data) => {
         console.log(data);
         resetBlock.classList.remove('active')
         messageBlock.classList.add('active')
         messageBlock.textContent = data;
      }).catch(error => {
         console.log(error);
      });
}
function backToLogin() {
   changeModalSection(loginBlock)
}

/// Обновление токена формы при логине
function refreshToken(newPage) {
   const parser = new DOMParser();
   const token = parser.parseFromString(newPage, "text/html").querySelector('input[name="csrfmiddlewaretoken"]').value;
   // console.log(token);
   document.querySelector('input[name="csrfmiddlewaretoken"]').value = token;
   try {
      createFormObject()
   } catch (error) {
      try {
         sendData(document.querySelector('input[name="csrfmiddlewaretoken"]').parentNode);
      } catch (error) {
         console.log(error);
      }
   }
   try {
      postForm();
   } catch (error) {
      console.log(error);
   }
}


// Модальное окно при отсутствии логина/подписки

const modalNoPay = {
   modalNoPayElement: document.createElement('div'),
   modalShowFlag: 0,

   createModal(auth) {
      let onclickEvent = ''
      if (auth != true) {
         onclickEvent = 'onclick="modalNoPay.openRegModal(event)"'

      }
      this.modalNoPayElement.classList.add('modalNoPay')
      this.modalNoPayElement.innerHTML = `
   <section class="screener">
                <div class="container">
                   <div class="screener__content">
                        <div class = "close-modal">
                           <div></div>
                           <div></div>
                        </div>
                       <div class="screener__block">
                           <div class="screener__title">Начать пользоваться P2P скринером ARBITOOLS</div>
                           <div class="screener__subtitle">Экономьте время и повышайте свою эффективность вместе с ARBITOOLS. Начните использовать уже сегодня!
                           </div>
                           <div class="screener__btn-block">
                               <a href="/profile/#premium" ${onclickEvent} class="screener__btn btn btn_white">Начать</a>
                           </div>
                       </div>
                       <img src="/static/main/img/main/screener-new.png" alt="">
                   </div>
                </div>
            </section>
   `
      if (auth == false) {
         this.modalNoPayElement.querySelector('.screener__btn').addEventListener('click', this.openRegModal)
      }
      this.modalNoPayElement.querySelector('.close-modal').addEventListener('click', this.deleteModal)
      document.querySelector('body').insertAdjacentElement("afterbegin", this.modalNoPayElement)
      this.modalShowFlag = 1
   },

   deleteModal() {
      modalNoPay.modalNoPayElement.querySelector('.screener__btn').removeEventListener('click', modalNoPay.openRegModal)
      modalNoPay.modalNoPayElement.querySelector('.close-modal').removeEventListener('click', modalNoPay.deleteModal)
      document.querySelector('body').removeChild(modalNoPay.modalNoPayElement)
   },
   openRegModal(event) {
      event.preventDefault()
      this.deleteModal()
      openRegBlock()
   }
}
