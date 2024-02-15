function userThanks (star) {
    star.classList.toggle('active')
    star.classList.contains('active') ? showThanksMess(star.firstElementChild) : null
}

function showThanksMess(mess) {
    mess.classList.add('show')
    setTimeout( () => {mess.classList.remove('show')}, 1200) 
}