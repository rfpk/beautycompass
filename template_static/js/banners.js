const bannersContainer = document.querySelector(".banners__container");
const bannersAddBtn = document.querySelector(".banners__plus");

const addBannersItem = () => {
  const newBannersItem = document.createElement("div");
  newBannersItem.classList.add(
    "banners__item"
  );

  const banners = bannersContainer.querySelectorAll('.banners__item').length;
  console.log('banners: ', banners);

  newBannersItem.innerHTML = `
    <div type="button" class="banners__image input--image">
      <label for="banners__image" class="label label--light label--profile">Баннер</label>
        <img
          src="/static/img/gallery-add.svg"
          alt="gallery-add logo"
          class="position-absolute top-50 start-50 translate-middle"
        />
        <input type="file" onchange="handleFileSelected(event)" name="series_banners-${banners}-banner" class="file-input"/>
        <i class="tag-close">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 20C4.48372 20 0 15.5163 0 10C0 4.48372 4.48372 0 10 0C15.5163 0 20 4.48372 20 10C20 15.5163 15.5163 20 10 20Z" fill="#E31E24"/>
              <path d="M13.1289 7.86591L7.86671 13.1281C7.59702 13.3978 7.14974 13.3978 6.88005 13.1281C6.61036 12.8584 6.61036 12.4111 6.88005 12.1414L12.1422 6.87925C12.4119 6.60956 12.8592 6.60956 13.1289 6.87925C13.3986 7.14893 13.3986 7.59622 13.1289 7.86591Z" fill="#FAFAFA"/>
              <path d="M13.1289 13.1247C12.8592 13.3943 12.4119 13.3943 12.1422 13.1247L6.88005 7.86247C6.61036 7.59278 6.61036 7.1455 6.88005 6.87581C7.14974 6.60612 7.59702 6.60612 7.86671 6.87581L13.1289 12.138C13.3986 12.4077 13.3986 12.855 13.1289 13.1247Z" fill="#FAFAFA"/>
          </svg>
        </i>
    </div>

    <div class="input input--general banners__input">
      <label for="shops__name" class="label label--light label--profile">Ссылка к баннеру</label>
      <input class="" id="shops__name" name="link_banners" value="" type="text" required/>
      <input type="hidden" name="series_banners-${banners}-id" id="id_series_banners-${banners}-id" isacopy="y" style="display: none;">
    </div>
        `;

  bannersContainer.insertBefore(newBannersItem, bannersAddBtn);

  const tagClose = newBannersItem.querySelector(".tag-close");
  tagClose.addEventListener("click", () => removeBannersItem(newBannersItem));


  const allBanners = bannersContainer.querySelectorAll(".banners__item");

  allBanners.forEach((element, index) => {
    if (index === allBanners.length - 1) {
      element.classList.add('last');
    } else {
      element.classList.remove('last');
    }
  });

  if (allBanners.length % 3 === 0) {
    // bannersAddBtn.remove();
    bannersAddBtn.classList.add("center");
  } else {
    bannersAddBtn.classList.remove("center");
  }
};

bannersAddBtn.addEventListener("click", addBannersItem);

// remove banner
const removeBannersItem = (item) => {
  item.remove();
};

// addBannersItem();



