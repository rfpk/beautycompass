const bannersContainer = document.querySelector(".banners__row");
const bannersAddBtn = document.querySelector(".banners__plus");


const addBannersItem = () => {
  const newBannersItem = document.createElement("div");
  newBannersItem.classList.add(
    "banners", "banners__pic", "position-relative", "m-0"
  );

  newBannersItem.innerHTML = `
  <div class="input image input--image profile__input profile__image products__image profile__products-image profile__products-input">
    <img src="/static/img/gallery-add.svg" alt="logo" class="position-absolute top-50 start-50 translate-middle"/>
    <input type="file" name="images" id="products__file-input" class="file-input profile__file-input products__file-input" onchange="handleFileSelected(this)"/>

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

// remove banner
const removeBannersItem = (item) => { item.remove(); };


