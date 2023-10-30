class SaveForm {
    constructor(localStorageItemName, formNode, sendFunctionName) {
        this.form = formNode;
        this.storageName = localStorageItemName;
        this.sendFunctionName = sendFunctionName;
    }
    checkAsideForm() {
        if (localStorage.getItem(this.storageName)) {
            this.loadForm()
        }
        else {
            this.saveForm()
        }
    }
    saveForm() {
        let checkedInputs = {}
        this.form.querySelectorAll('input').forEach((element) => {
            if (!element.parentNode.classList.contains('favorite__item')) {
                if ((element.type == 'checkbox' || element.type == 'radio') && element.checked == true) {
                    checkedInputs[element.id] = element.value
                } else if (element.type == 'number') {
                    checkedInputs[element.id] = element.value
                }
            }
        })

        const localData = JSON.stringify(checkedInputs)
        localStorage.setItem(this.storageName, localData)
    }
    loadForm() {
        //После вызова необходимо обновить заголовки формы и отправить запрос на обновление  списка
        const saveFormData = JSON.parse(localStorage.getItem(this.storageName))
        this.form.querySelectorAll('input').forEach((element) => {
            if (element.type == 'checkbox' || element.type == 'radio') {
                element.checked = false;
            } else if (element.type == 'number') {
                element.value = ''
            }
        })

        for (let key in saveFormData) {
            if (this.form.querySelector(`#${[key]}`).type == 'checkbox' || this.form.querySelector(`#${[key]}`).type == 'radio') {
                this.form.querySelector(`#${[key]}`).checked = true
            } else if (this.form.querySelector(`#${[key]}`).type == 'number') {
                this.form.querySelector(`#${[key]}`).value = saveFormData[key];
            }
        }
        refreshSidebarTitle();
        window[this.sendFunctionName]();
    }
}