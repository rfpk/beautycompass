const shopsData = [];
const shopsName = {};

const shops = document.querySelectorAll('.shops')
shops.forEach((shop,index) => {
  const shopsContainer = shop.querySelector(".shops__container");
  const shopsPlus = shop.querySelector(".shops__plus");
  const shopsContainerName = shopsContainer.getAttribute('data-shops')
  const addShopsItem = () => {
    const newShopsItem = document.createElement("div");
    newShopsItem.classList.add("shops__item");
    const newShopsItemId = Date.now();
    newShopsItem.dataset.itemId = newShopsItemId
    newShopsItem.dataset.shopsName = shopsContainerName
    newShopsItem.innerHTML = `
    <div>
      <div class="input input--general shops__name">
        <label for="shops__name-input" class="label label--primary">Название кнопки</label>
        <input
                class=""
                id="shops__name-input"
                placeholder="Официальный магазин"
                name="shops__name-input"
        />
      </div>
      <div class="input input--general shops__url">
          <label for="shops__url-input" class="label label--primary"> URL </label>
          <input
                  class="input input--general"
                  id="shops__url-input"
                  placeholder="http://"
                  name="shops__url-input"
          />
      </div>
      <i class="tag-close">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 20C4.48372 20 0 15.5163 0 10C0 4.48372 4.48372 0 10 0C15.5163 0 20 4.48372 20 10C20 15.5163 15.5163 20 10 20Z" fill="#E31E24"/>
            <path d="M13.1289 7.86591L7.86671 13.1281C7.59702 13.3978 7.14974 13.3978 6.88005 13.1281C6.61036 12.8584 6.61036 12.4111 6.88005 12.1414L12.1422 6.87925C12.4119 6.60956 12.8592 6.60956 13.1289 6.87925C13.3986 7.14893 13.3986 7.59622 13.1289 7.86591Z" fill="#FAFAFA"/>
            <path d="M13.1289 13.1247C12.8592 13.3943 12.4119 13.3943 12.1422 13.1247L6.88005 7.86247C6.61036 7.59278 6.61036 7.1455 6.88005 6.87581C7.14974 6.60612 7.59702 6.60612 7.86671 6.87581L13.1289 12.138C13.3986 12.4077 13.3986 12.855 13.1289 13.1247Z" fill="#FAFAFA"/>
          </svg>
        </i>
    </div>
    `;
    shopsContainer.insertBefore(newShopsItem, shopsPlus);
    const tagClose = newShopsItem.querySelector(".tag-close");
    tagClose.addEventListener("click", () => removeShopsItem(newShopsItem));
  };
  const removeShopsItem = (item) => {
    item.remove();
  };
  shopsPlus.addEventListener("click", addShopsItem);
  // addShopsItem();
})

const pageConfirm = document.querySelector('.btn__products-confirm')
pageConfirm.addEventListener("click", () => {
  shopsData.length = 0;
  const shopsItems = document.querySelectorAll(".shops__item");
  shopsItems.forEach(newShopsItem => {
    const nameInput = newShopsItem.querySelector(".shops__name input");
    const urlInput = newShopsItem.querySelector(".shops__url input");

    const shopId = newShopsItem.getAttribute('data-item-id');
    const shopsOriginName = newShopsItem.getAttribute('data-shops-name')

    const shopData = {
      id: shopId,
      shopOriginName: shopsOriginName,
      name: nameInput.value,
      url: urlInput.value,
    };


    shopsData.push(shopData)
  });
  console.log(shopsData)

  // fetch(url, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify(shopsData),
  // })
  //   .then(response => response.json())
  //   .then(responseData => {
  //     // Обработка ответа от сервера
  //     console.log("Ответ от сервера:", responseData);
  //   })
  //   .catch(error => {
  //     console.error("Ошибка при отправке запроса:", error);
  //   });
});



