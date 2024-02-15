// === adding shops ===

// const shopsWrap = document.querySelector(".shops__wrap");
// const shopsPlus = document.querySelector(".shops__plus");
//
// const addShopsItem = () => {
//   const newShopsItem = document.createElement("div");
//   newShopsItem.classList.add("shops__item", "card--close", "col-9", "col-md-4");
//
//   newShopsItem.innerHTML = `
//     <div>
//       <label for="shops__form-name" class="title">
//         Название кнопки
//       </label>
//       <input
//         class="input input--regular"
//         id="shops__form-name"
//         placeholder="Официальный магазин"
//       />
//     </div>
//     <div>
//       <label for="shops__form-url" class="title"> URL </label>
//       <input
//         class="input input--regular"
//         id="shops__form-url"
//         placeholder="http://"
//       />
//     </div>
//       <i class="tag-close">
//         <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
//           <path d="M10 20C4.48372 20 0 15.5163 0 10C0 4.48372 4.48372 0 10 0C15.5163 0 20 4.48372 20 10C20 15.5163 15.5163 20 10 20Z" fill="#E31E24"/>
//           <path d="M13.1289 7.86591L7.86671 13.1281C7.59702 13.3978 7.14974 13.3978 6.88005 13.1281C6.61036 12.8584 6.61036 12.4111 6.88005 12.1414L12.1422 6.87925C12.4119 6.60956 12.8592 6.60956 13.1289 6.87925C13.3986 7.14893 13.3986 7.59622 13.1289 7.86591Z" fill="#FAFAFA"/>
//           <path d="M13.1289 13.1247C12.8592 13.3943 12.4119 13.3943 12.1422 13.1247L6.88005 7.86247C6.61036 7.59278 6.61036 7.1455 6.88005 6.87581C7.14974 6.60612 7.59702 6.60612 7.86671 6.87581L13.1289 12.138C13.3986 12.4077 13.3986 12.855 13.1289 13.1247Z" fill="#FAFAFA"/>
//         </svg>
//       </i>
//   `;
//
//   shopsWrap.insertBefore(newShopsItem, shopsPlus);
//
//   const tagClose = newShopsItem.querySelector(".tag-close");
//   tagClose.addEventListener("click", () => removeShopsItem(newShopsItem));
// };
//
// const removeShopsItem = (item) => {
//   item.remove();
// };
//
// shopsPlus.addEventListener("click", addShopsItem);
// addShopsItem();

// // === adding banners ===
//
// const bannersForm = document.querySelector(".banners__form");
// const bannersAddBtn = document.querySelector(".banners__add-btn");
//
// const addBannersItem = () => {
//   const newBannersItem = document.createElement("div");
//   newBannersItem.classList.add(
//     "banners__item",
//     "col-12",
//     "col-md-4",
//     "d-flex",
//     "flex-wrap",
//     "gy-5"
//   );
//
//   newBannersItem.innerHTML = `
//       <div class="col-5 col-md-12 mb-md-4">
//             <div
//                     type="button"
//                     class="banners__photo position-relative"
//             >
//               <label
//                       for="banners__photo"
//                       class="label--light shops__label position-absolute"
//               >Баннер бренда (1080х277 рх)</label
//               >
//               <img
//                       src="../img/gallery-add.svg"
//                       alt="gallery-add logo"
//                       id="banners__photo"
//                       class="position-absolute top-50 start-50 translate-middle"
//               />
//               <input
//                       type="file"
//                       onchange="handleFileSelected(event)"
//                       class="file-input"
//               />
//               <i class="tag-close">
//                 <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
//                     <path d="M10 20C4.48372 20 0 15.5163 0 10C0 4.48372 4.48372 0 10 0C15.5163 0 20 4.48372 20 10C20 15.5163 15.5163 20 10 20Z" fill="#E31E24"/>
//                     <path d="M13.1289 7.86591L7.86671 13.1281C7.59702 13.3978 7.14974 13.3978 6.88005 13.1281C6.61036 12.8584 6.61036 12.4111 6.88005 12.1414L12.1422 6.87925C12.4119 6.60956 12.8592 6.60956 13.1289 6.87925C13.3986 7.14893 13.3986 7.59622 13.1289 7.86591Z" fill="#FAFAFA"/>
//                     <path d="M13.1289 13.1247C12.8592 13.3943 12.4119 13.3943 12.1422 13.1247L6.88005 7.86247C6.61036 7.59278 6.61036 7.1455 6.88005 6.87581C7.14974 6.60612 7.59702 6.60612 7.86671 6.87581L13.1289 12.138C13.3986 12.4077 13.3986 12.855 13.1289 13.1247Z" fill="#FAFAFA"/>
//                 </svg>
//               </i>
//             </div>
//           </div>
//     <div class="banners__link col-7 col-md-12">
//         <div class="input--wrapper position-relative">
//               <label
//                       for="shops__name"
//                       class="label--light profile__label position-absolute"
//               >Ссылка к баннеру</label
//               >
//               <input
//                       class="profile__input profile__name input--regular w-100 h-100 border-0"
//                       id="shops__name"
//                       value=""
//                       type="text"
//                       required
//               />
//             </div>
//     </div>
//   `;
//
//   bannersForm.insertBefore(newBannersItem, bannersAddBtn.parentElement);
//
//   const tagClose = newBannersItem.querySelector(".tag-close");
//   tagClose.addEventListener("click", () => removeBannersItem(newBannersItem));
// };
//
// bannersAddBtn.addEventListener("click", addBannersItem);
//
// const removeBannersItem = (item) => {
//   item.remove();
// };
//
// addBannersItem();

// === input files ===

function triggerFileInput() {
  const fileInput = document.querySelectorAll(".file-input");
  fileInput.forEach((input) => {
    input.click();
  });
}

function handleFileSelected(event) {
  const file = event.target.files[0];
  if (file) {
      // Обработка загруженного файла
      let reader = new FileReader();
      reader.readAsDataURL(file);
       // Banner Images
      reader.onload = function() {
          const elem = event.srcElement.parentElement.querySelector('img');
          $(elem).attr('src', reader.result); 
      }
  }
}

// === textareas ===

const textareas = document.querySelectorAll("textarea");

textareas.forEach((textarea) => {
  textarea.setSelectionRange(0, 0);
});
