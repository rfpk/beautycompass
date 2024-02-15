function newFeedReplies() {

    const feeds = document.querySelectorAll('.feed')

    feeds.forEach( el => { 
        const newRepliesBtn = el.querySelector('.js-newAnswerBtn')
        newRepliesBtn?.addEventListener('click', function(event) { 

            event.preventDefault()
            this.classList.add('pe-none')
            
            if(this.classList.contains('feed__mark')){
                
                const feedTextEdit = el.querySelector('.feed__text').innerHTML
                createReplies(el, "Оставить комментарий", "Сохранить", feedTextEdit)
                addBanners(el)

            } else { 
                createReplies(el, "Оставить комментарий", "Отправить комментарий") 
                addBanners(el)
            }
            
        }, { once: true } )
    })

}

function createReplies(parent, placeholder, button, value = '') {

    //CREATE text editor
    const replies = document.createElement("div");
    replies.classList.add( "feed-replies", "my-2");
    
    replies.innerHTML = `
        <form action="" method="post" name="comment-form" enctype="multipart/form-data">
            <textarea name="content" class="editor" placeholder="${placeholder}">${value}</textarea>

            <div class="profile__images profile__products-images banners__row mt-3">
                <div class="banners banners__pic position-relative m-0">
                    <div class="input image input--image profile__input profile__image products__image profile__products-image profile__products-input">
                        <img src="/static/img/gallery-add.svg" alt="logo" class="position-absolute top-50 start-50 translate-middle"/>
                        <input type="file" name="products__file-input" id="products__file-input" class="file-input profile__file-input products__file-input" onchange="handleFileSelected(this)"/>
                    </div>
                </div>

                <div class="profile__products-plus banners__plus">
                    <svg role="button" class="banners__plus-image hover-red" viewBox="0 0 26 26" fill="none"xmlns="http://www.w3.org/2000/svg" >
                        <path d="M12.9993 24.6452C6.57518 24.6452 1.35352 19.4235 1.35352 12.9993C1.35352 6.57518 6.57518 1.35352 12.9993 1.35352C19.4235 1.35352 24.6452 6.57518 24.6452 12.9993C24.6452 19.4235 19.4235 24.6452 12.9993 24.6452ZM12.9993 2.97852C7.47435 2.97852 2.97852 7.47435 2.97852 12.9993C2.97852 18.5243 7.47435 23.0202 12.9993 23.0202C18.5243 23.0202 23.0202 18.5243 23.0202 12.9993C23.0202 7.47435 18.5243 2.97852 12.9993 2.97852Z" fill="#1560BD"/>
                        <path d="M17.3327 13.8125H8.66602C8.22185 13.8125 7.85352 13.4442 7.85352 13C7.85352 12.5558 8.22185 12.1875 8.66602 12.1875H17.3327C17.7769 12.1875 18.1452 12.5558 18.1452 13C18.1452 13.4442 17.7769 13.8125 17.3327 13.8125Z" fill="#1560BD" />
                        <path d="M13 18.1452C12.5558 18.1452 12.1875 17.7769 12.1875 17.3327V8.66602C12.1875 8.22185 12.5558 7.85352 13 7.85352C13.4442 7.85352 13.8125 8.22185 13.8125 8.66602V17.3327C13.8125 17.7769 13.4442 18.1452 13 18.1452Z" fill="#1560BD" />
                    </svg>
                </div>
            </div>


            <input type="submit" value="${button}" class="btn btn--base mt-3">
        </form>
    `;

    parent.insertAdjacentElement('beforeend', replies)


    // INIT text editor
    ClassicEditor
        .create( parent.querySelector( '.editor' ), {
            toolbar: {
                items: [
                    'bold',
                    'italic',
                    'strikethrough',
                    'underline',
                    '|',
                    'numberedList',
                    'bulletedList',
                    '|',
                    'link',
                ]
            },
        } )
        .then( editor => {
            window.editor = editor;
        } )
        .catch( handleSampleError );

        function handleSampleError( error ) {
            const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

            const message = [
                'Oops, something went wrong!',
                `Please, report the following error on ${ issueUrl } with the build id "imv2hnq0y3vb-2iq20258slh1" and the error stack trace:`
            ].join( '\n' );

            console.error( message );
            console.error( error );
        }
}

function addBanners(parent){

    const bannersContainer = parent.querySelector(".banners__row");
    const bannersAddBtn = parent.querySelector(".banners__plus");

    const addBannersItem = () => {

        const newBannersItem = document.createElement("div");
        newBannersItem.classList.add(
            "banners", "banners__pic", "position-relative", "m-0"
        );

        newBannersItem.innerHTML = `
        <div class="input image input--image profile__input profile__image products__image profile__products-image profile__products-input">
            <img src="/static/img/gallery-add.svg" alt="logo" class="position-absolute top-50 start-50 translate-middle"/>
            <input type="file" name="products__file-input" id="products__file-input" class="file-input profile__file-input products__file-input" onchange="handleFileSelected(this)"/>

            <i class="tag-close">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 20C4.48372 20 0 15.5163 0 10C0 4.48372 4.48372 0 10 0C15.5163 0 20 4.48372 20 10C20 15.5163 15.5163 20 10 20Z" fill="#E31E24"></path>
                <path d="M13.1289 7.86591L7.86671 13.1281C7.59702 13.3978 7.14974 13.3978 6.88005 13.1281C6.61036 12.8584 6.61036 12.4111 6.88005 12.1414L12.1422 6.87925C12.4119 6.60956 12.8592 6.60956 13.1289 6.87925C13.3986 7.14893 13.3986 7.59622 13.1289 7.86591Z" fill="#FAFAFA"></path>
                <path d="M13.1289 13.1247C12.8592 13.3943 12.4119 13.3943 12.1422 13.1247L6.88005 7.86247C6.61036 7.59278 6.61036 7.1455 6.88005 6.87581C7.14974 6.60612 7.59702 6.60612 7.86671 6.87581L13.1289 12.138C13.3986 12.4077 13.3986 12.855 13.1289 13.1247Z" fill="#FAFAFA"></path>
            </svg>
            </i>
        </div>
        `;

        bannersContainer.insertBefore(newBannersItem, bannersAddBtn);

        const tagClose = newBannersItem.querySelector(".tag-close");
        tagClose.addEventListener("click", () => removeBannersItem(newBannersItem));


    };

    bannersAddBtn.addEventListener("click", () => { addBannersItem() });

    const removeBannersItem = (item) => { item.remove(); };

}

newFeedReplies()