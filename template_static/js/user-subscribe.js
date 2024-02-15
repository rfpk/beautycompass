function userSubscribe (btn, event) {
    event.preventDefault()
    btn.innerText.toLowerCase() == 'подписаться' ?
        btn.innerText = 'подписка' : 
        btn.innerText = 'подписаться'
    btn.classList.toggle('active')
}