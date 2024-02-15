function onSubmitChangeText (event) {
    event.preventDefault()
    const btn = event.target.querySelector('button')

    btn.innerText.toLowerCase() == 'Ответить' ?
        btn.innerText = 'редактировать' :
        btn.innerText = 'ответить'
}

