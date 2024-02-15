// Bootstrap form validation
(function () {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            }
    
            form.classList.add('was-validated')
        }, false)
        })
    })()

function  openModalQuestion(modalID) {
    if(document.querySelector(modalID)) {
        const modal = document.querySelector(modalID)
        modal.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget
        let recipient = button.getAttribute('data-bs-whatever')
        let modalTitle = modal.querySelector('.modal-name')
        modalTitle.textContent = recipient
        })
    }
}
openModalQuestion('#openQuestion')
openModalQuestion('#openReview')

function  openModalImg() {
    if(document.querySelector('#openFullImg')) {
        const modal = document.querySelector('#openFullImg')
        modal.addEventListener('show.bs.modal', function (event) {
            let img = event.relatedTarget
            let recipient = img.getAttribute('src')
            let modalImg = modal.querySelector('.modal-img img')
            modalImg.src = recipient
            console.log(modalImg.src)
        })
    }
}
openModalImg()

// Pass validation
function valid(event){
    const pas = document.querySelector('#registerInputPassword1').value
    const cpas = document.querySelector('#registerInputPassword2').value
    const messPas = document.querySelector('#headerRegisterPassCheck1')
    const messCpas = document.querySelector('#headerRegisterPassCheck2')
    console.log(pas)
    for(i=0;i < cpas.length; i++)
    {
    
     if(pas[i] != cpas[i] && event.key != 8)
     {
        messPas.classList.add('auth__invalid--unchecked')
        messCpas.classList.add('auth__invalid--unchecked')
       break;
     } else {
        messPas.classList.remove('auth__invalid--unchecked')
        messCpas.classList.remove('auth__invalid--unchecked')
     }
    }
}

// Carousel
async function initCarousel(id) {
    const myCarousel = document.getElementById(`${id}`)
    const indicatorsContainer = myCarousel.querySelector(".carousel-indicators")
    const indicators = myCarousel.querySelectorAll(".carousel-indicators button")
    const inner = myCarousel.querySelectorAll(".carousel-inner div")

    const lengElements = indicators.length
    let centerLenthElement;

    if (lengElements % 2 === 0) {
        centerLenthElement = lengElements / 2
    } else {
        centerLenthElement = lengElements / 2 + 0.5
    }

    for (let i = 0; i < lengElements; i++) {
        if ((i + 1) === centerLenthElement ) {
            indicators[i].classList.add("active")
            inner[i].classList.add("active")
        } else {
            indicators[i].classList.remove("active")
            inner[i].classList.remove("active")
        }
    }

    function setClassToPrevNextSlide() {
        const slideActive = myCarousel.querySelector('.carousel-indicators .active');
        if (slideActive.previousElementSibling) {
            slideActive.previousElementSibling.classList.add('near-active');
        }

        if (slideActive.nextElementSibling) {
            slideActive.nextElementSibling.classList.add('near-active');
        }
    }

    setClassToPrevNextSlide()

    myCarousel.addEventListener('slide.bs.carousel', event => {
        myCarousel.querySelectorAll('.carousel-indicators button').forEach((item) => {
            item.classList.remove('near-active');
        });
        new Promise(resolve => {
            let actualDifferent = event.from - event.to
            let different = event.to - event.from
            if (different < 0) {
                different = -different
            }
            if (event.direction === "left") {
                if (different < 2 || event.from === lengElements - 1) {
                    const indicatorFirst = myCarousel.querySelector(".carousel-indicators > button")
                    addToEnd(indicatorFirst)
                } else {
                    if (event.from === 0 && different === lengElements - 1) {
                        const indicatorLast = myCarousel.querySelector(".carousel-indicators > button:last-child")
                        addToStart(indicatorLast)
                    } else {
                        if (actualDifferent < 0 && different >= centerLenthElement) {
                            for (let i = 1; i <= (lengElements - event.to + event.from); i++) {
                                const indicatorLast = myCarousel.querySelector(`.carousel-indicators > button:last-child`)
                                addToStart(indicatorLast)
                            }
                        } else {
                            for (let i = 1; i <= different; i++) {
                                const indicatorFirst = myCarousel.querySelector(`.carousel-indicators > button:nth-child(1)`)
                                addToEnd(indicatorFirst)
                            }
                        }
                    }
                }
            } else if (event.direction === 'right')  {
                if (different < 2 || event.to === lengElements - 1) {
                    const indicatorLast = myCarousel.querySelector(".carousel-indicators > button:last-child")
                    addToStart(indicatorLast)
                } else {
                    if (event.from === lengElements - 1 && different === lengElements - 1) {
                        const indicatorFirst = myCarousel.querySelector(".carousel-indicators > button")
                        addToEnd(indicatorFirst)
                    } else {
                        if (actualDifferent > 0 && different >= centerLenthElement) {
                            for (let i = 1; i <= (lengElements - event.from + event.to); i++) {
                                const indicatorFirst = myCarousel.querySelector(`.carousel-indicators > button:nth-child(1)`)
                                addToEnd(indicatorFirst)
                            }
                        } else {
                            for (let i = 1; i <= different; i++) {
                                const indicatorLast = myCarousel.querySelector(`.carousel-indicators > button:last-child`)
                                addToStart(indicatorLast)
                            }
                        }
                    }
                }
            }
            resolve(true)
        }).then(() => {
            setClassToPrevNextSlide()
        })
    })

    function addToEnd(indicator) {
        const clone = indicator.cloneNode(true)
        indicator.remove()
        indicatorsContainer.append(clone)
    }

    function addToStart(indicator) {
        const clone = indicator.cloneNode(true)
        indicator.remove()
        indicatorsContainer.prepend(clone)
    }
}

const carousels = document.querySelectorAll('.carousel--base')
for (var i=0; i<carousels.length; i++)
{
    initCarousel(carousels[i].id)
}


// Hide tag links

function hideTagListInit(indexStartHide, wrapTagList) {
    const tagList = wrapTagList.querySelectorAll('.tag-links > .tag')
    const dots = createDots()

    const tagListHide = hideTagList(tagList, indexStartHide)

    tagListHide.forEach(item => wrapTagList.appendChild(item))
    if (tagList.length > (indexStartHide + 1)) {
        wrapTagList.appendChild(dots)
    }

    dots.addEventListener('click', function() {
        for (let i = indexStartHide; i < tagList.length; i++) {
            tagList[i].classList.remove('hide')
        }
        dots.remove()
    })
}

const createDots = () => {
    const dots = document.createElement('div')
    dots.className = 'tag tag--dots'
    dots.textContent = '• • •'
    return dots
}

const hideTagList = (tagList, indexStartHide) => {
    if (tagList.length > (indexStartHide + 1)) {
        for (let i = indexStartHide; i < tagList.length; i++) {
            tagList[i].classList.add('hide')
        }
    }
    return tagList
}

const tagList = document.querySelectorAll('.tag-links')
if(tagList) {
    for (var i=0; i<tagList.length; i++)
    {
        hideTagListInit(2, tagList[i])
    }
}

// function userInterface() {
//     let userId

//     // Authorization
//     function saveUserLocalStorage() {
//         const authForm = document.querySelector('.auth__form')
//         authForm.onsubmit = async function(e) {
//             // const formData = new FormData(e.target)
//             const emailValue = document.querySelector('#headerAuthEmail')
//             const passValue = document.querySelector('#authInputPassword')
//             e.preventDefault()
//             const authBody = { 
//                 // email: emailValue,
//                 // password: passValue,
//                 username: 'kminchelle',
//                 password: '0lelplR',
//             }
//             const resp = await fetch('https://dummyjson.com/auth/login',{
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json'},
//                 body: JSON.stringify(authBody)
//             })
//             const result = await resp.json()
//             localStorage.setItem('userToken', result['token'])
//             localStorage.setItem('userId', result['id'])
//             console.log(userId)
//         }    
//     }
//     saveUserLocalStorage()  

//     // Add/remove class 'active' for favorite-brand
//     async function toggleFavoriteBrand() {
//         const favoriteBrand = document.querySelector('.favorite--brand')
//         const userToken = localStorage.getItem('userToken')
//         if (userToken) {
//             const resp = await fetch('https://64a990b78b9afaf4844ad897.mockapi.io/favoritebrand')
//             const result = await resp.json()
//             userObject = result.find(elem => elem.id === userId)
//             if (userObject) {
//                 favoriteBrand.classList.add('active')
//             }
//         } else {
//             console.log('Unauth')
//         }
//     }    
//     //toggleFavoriteBrand()    

// }
// userInterface()


// opent active product img

function imgSetAttributes() {
    if (document.querySelector('.carousel--product')){
        const indicators = document.querySelector('.carousel--product .carousel-indicators')
        imgProductSetAttributes()
        restartSetAttributes(indicators)
    }
    function imgProductSetAttributes() {  
        let productPics = document.querySelectorAll('.carousel--product .carousel-item')    
        console.log('productPics ', productPics)  
        for (let i=0; i < productPics.length; i++) {
            if(productPics[i].classList.contains('active')) {
                productPics[i].querySelector('img').setAttribute('data-bs-toggle', 'modal')
                productPics[i].querySelector('img').setAttribute('data-bs-target', '#openFullImg')
            }else {
                productPics[i].querySelector('img').removeAttribute('data-bs-toggle', 'modal')
                productPics[i].querySelector('img').removeAttribute('data-bs-target', '#openFullImg')

            }
        }
    }
    function restartSetAttributes(indicators) {
        indicators.addEventListener('click', e => imgProductSetAttributes())
    }
}

imgSetAttributes()

// add img multiple 
function upploadImgMultyple() {
    if (document.querySelector('#img-multiple')) {
        let fileInput = document.querySelector('#img-multiple')

    }
}

// splide settings

if(document.querySelector('.splide--vertical')) {
    document.addEventListener( 'DOMContentLoaded', function() {
        const splide = new Splide ( '.splide--vertical', {
            direction   : 'ttb',
            height : 484,
            type   : 'slide',
            perPage: 3,
            pagination : false,
            fixedHeight : 138,
            rewind: false,
            arrowPath : '0',
            breakpoints: {
                1400: {
                    height : 268,
                    fixedHeight : 70,
                    gap : 0,
                    heightRatio : 0.6,
                },
            }
        } );
        splide.mount();
    } );
}

if(document.querySelector('.splide--gallery')) {
    document.addEventListener( 'DOMContentLoaded', function() {
        const splide = new Splide( '.splide--gallery', {
            height : 120,
            type   : 'slide',
            perPage: 9,
            gap : 30,
            pagination : false,
            arrows: true,
            arrowPath : '0',
            breakpoints: {
                1400: {
                    perPage : 5,
                    gap : 14,
                    padding: { left: 0, right: 40 },
                    arrows: false,
                },
                768: {
                    perPage : 3,
                },
            }
        } );
        splide.mount();
    } );
}

if(document.querySelector('.splide--users-feedback')) {
    document.addEventListener( 'DOMContentLoaded', function() {
        let elms = document.querySelectorAll( '.splide--users-feedback' )
        for ( var i = 0; i < elms.length; i++ ) {
        new Splide( elms[i], {
            type   : 'slide',
            perPage: 3,
            gap : 45,
            pagination : false,
            padding: { left: 12, right: 12 },
            arrows: true,
            arrowPath : '0',
            breakpoints: {
                1400: {
                    perPage : 2,
                    gap : 14,
                    padding: { left: 10, right: 60 },
                    arrows: false,
                },
                768: {
                    perPage : 1,
                },
            }
        } ).mount();
    }
    } );
}

// add rating

const ratings = document.querySelectorAll('.rating')
if (ratings.length > 0) {
    initRatings();
}

function initRatings() {
    let ratingActive, ratingValue
    for (let i = 0; i < ratings.length; i++) {
        const rating = ratings[i];
        initRating(rating);
    }

    function initRating(rating) {
        initRatingVars(rating);

        setActiveRatingWidth();

        if (rating.classList.contains('rating--set')) {
            setRaring(rating)
        }
    }

    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__active')
        if (rating.querySelector('.rating__value')) {
            ratingValue = rating.querySelector('.rating__value')
        } else ratingValue = 0
    }
    
    function setActiveRatingWidth(i = ratingValue.innerHTML) {   
        const ratingActiveWidth = i / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }

    function setRaring(rating) {
        const ratingItems = rating.querySelectorAll('.rating__item')
        for (let i = 0; i < ratingItems.length; i++) {
            const ratingItem = ratingItems[i];
            ratingItem.addEventListener('mouseenter', function(e) {
                initRatingVars(rating);
                setActiveRatingWidth(ratingItem.value);
            })

            ratingItem.addEventListener('mouseleave', function(e) {
                setActiveRatingWidth();
            })

            ratingItem.addEventListener('click', function(e) {
                initRatingVars(rating);
                ratingValue.innerHTML = i + 1;
                setActiveRatingWidth();
            })
        }
    }
}

function countChars() {
    if (document.querySelector(".leave-feed__count")) {
        areas = document.querySelectorAll(".leave-feed__textarea")
        for (let i = 0; i < areas.length; i++) {
            let area = areas[i].querySelector('textarea')
            let areaCounter =  areas[i].querySelector(".leave-feed__num")
            area.addEventListener('keyup', e => {
                areaCounter.innerHTML = area.value.length
            })
        }
    }
}

countChars();

//For demonstration

// Add/remove class 'active' for favorite brand
function toggleFavoriteBrand() {
    const favoriteList = document.querySelectorAll('.favorite--brand')
    favoriteList.forEach(item => {
        item.addEventListener('click', elem => {
            elem.preventDefault()
            if(!elem.target.classList.contains('active')) {
                elem.target.classList.add('active')
            } else
            elem.target.classList.remove('active')
        }) 
    })
}
toggleFavoriteBrand()

// Add/remove class 'active' for favorite product
function toggleFavoriteProduct() {
    const favoriteList = document.querySelectorAll('.favorite--product')
    favoriteList.forEach(item => {
        item.addEventListener('click', elem => {
            elem.preventDefault()
            if(!elem.target.classList.contains('active')) {
                elem.target.classList.add('active')
            } else
            elem.target.classList.remove('active')
        }) 
    })
}

toggleFavoriteProduct()


// Add/remove class 'active' for favorite product full
function toggleFavoriteProductFull() {
    const favoriteList = document.querySelectorAll('.favorite--product-full')
    favoriteList.forEach(item => {
        item.addEventListener('click', elem => {
            elem.preventDefault()
            if(!elem.target.classList.contains('active')) {
                elem.target.classList.add('active')
                text = 'В избранном'
                document.querySelector('.favorite--product-full').textContent = text
            } else {
                elem.target.classList.remove('active')
                text = 'Добавить в избранное'
                document.querySelector('.favorite--product-full').textContent = text
            }
        }) 
    })
}

toggleFavoriteProductFull()


// Add/remove class 'active' for subscription
function toggleSubscription() {
    const subBtn = document.querySelector('.follow-brand')
    let text
    if(subBtn) {
        subBtn.addEventListener('click', event => {
            if(!event.target.classList.contains('active')) {
                text = 'Вы подписаны'
                event.target.classList.add('active')
                document.querySelector('.follow-brand').textContent = text
            } else{
                text = 'Подписаться'
                event.target.classList.remove('active')
                document.querySelector('.follow-brand').textContent = text
            }
        }) 
    }
}

toggleSubscription()