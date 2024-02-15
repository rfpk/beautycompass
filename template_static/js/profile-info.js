document.addEventListener("DOMContentLoaded", () => {
  const shopsWrap = document.querySelector(".shops__wrap");
  const shopsPlus = document.querySelector(".shops__plus");

  const addShopsItem = () => {
    const newShopsItem = document.createElement("div");
    newShopsItem.classList.add("shops__item", "col-9", "col-md-4");

    newShopsItem.innerHTML = `
      <div class="mb-1">
        <label for="shops__form-name" class="title">
          Название кнопки
        </label>
        <input
          class="input input--regular"
          id="shops__form-name"
          value="Оффициальный магазин"
        />
      </div>
      <div>
        <label for="shops__form-url" class="title"> URL </label>
        <input
          class="input input--regular"
          id="shops__form-url"
          value="http://beautycompass.ru"
        />
      </div>
    `;

    shopsWrap.insertBefore(newShopsItem, shopsPlus);
  };

  shopsPlus.addEventListener("click", addShopsItem);

  const bannersForm = document.querySelector(".banners__form");
  const bannersAddBtn = document.querySelector(".banners__add-btn");

  const addBannersItem = () => {
    const newBannersItem = document.createElement("div");
    newBannersItem.classList.add(
      "banners__item",
      "col-12",
      "col-md-4",
      "col-xxl-4",
      "d-flex",
      "flex-wrap",
      "gy-4",
      "gy-md-5"
    );

    newBannersItem.innerHTML = `
      <div class="banners_banner col-5 col-md-12 mb-md-4">
         <div
                      type="button"
                      onclick="triggerFileInputShop()"
                      class="shops__photo position-relative"
              >
                <label
                        for="shops__photo"
                        class="label--light shops__label position-absolute"
                >Баннер бренда (1080х277 рх)</label
                >
                <img
                        src="/static/img/gallery-add.svg"
                        alt="gallery-add logo"
                        id="shops__photo"
                        class="position-absolute top-50 start-50 translate-middle"
                />
                <input
                        type="file"
                        id="shop__file-input"
                        onchange="handleFileSelected(event)"
                        class="input--file"
                />
              </div>
      </div>
      <div class="banners__link col-7 col-md-12">
          <div class="input--wrapper position-relative">
                <label
                        for="shops__name"
                        class="label--light profile__label position-absolute"
                >Ссылка к баннеру</label
                >
                <input
                        class="profile__input profile__name input--regular w-100 h-100 border-0"
                        id="shops__name"
                        value=""
                        type="text"
                        required
                />
              </div>
      </div>
    `;

    bannersForm.insertBefore(newBannersItem, bannersAddBtn.parentElement);
  };

  bannersAddBtn.addEventListener("click", addBannersItem);
});
