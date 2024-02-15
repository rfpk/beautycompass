const addInfoTrigger = document.querySelector(".add-info__trigger");
const addInfoContent = document.querySelector(".add-info__content");
const addInfoArrow = document.querySelector(".add-info__trigger svg");
const questionSign = document.querySelector(".question-sign");
let isOpen = false;
addInfoTrigger.addEventListener("click", function () {
  if (!isOpen) {
    addInfoContent.style.maxHeight = addInfoContent.scrollHeight + 20 + "px";
    isOpen = true;
    addInfoArrow.style.transform = "rotate(180deg)";
    addInfoContent.style.margin = "1.5rem 0 1rem 0";
  } else {
    addInfoContent.style.maxHeight = "0";
    isOpen = false;
    addInfoArrow.style.transform = "rotate(0)";
    addInfoContent.style.paddingTop = "0px";
    addInfoContent.style.margin = "0";
    addInfoContent.style.margin = "0";
    addInfoContent.style.margin = "0";
  }
});

// === creating brands ===

// const addInfoSchemeLeft = document.querySelector('.add-info__schemes .left .left-inner');
// const addInfoSchemeRight = document.querySelector('.add-info__schemes .right .right-inner');
//
// const addItem = () => {
//   event.preventDefault();
//   const leftItem = document.createElement('div');
//   leftItem.classList.add('left-inner__item');
//   const brandItem = document.createElement('div');
//   brandItem.classList.add('left-inner__brand', 'title--h5', 'hover--red',
//     'd-flex', 'align-items-end', 'ps-2');
//   brandItem.id = 'left-inner__brand-' + addInfoSchemeLeft.childElementCount + 1
//
//   const rightItem = document.createElement('div');
//   rightItem.classList.add('right-inner__item');
//   // rightItem.classList.add('my-3')
//   rightItem.innerHTML = `
//     <a
//       href=""
//       class="right__title title--h5 hover--red text-decoration-none position-relative">
//       <span>Бренд ${addInfoSchemeRight.childElementCount + 1}</span>
//       <img class="question right__question d-none d-md-inline mx-2" src="../img/plus-rect.svg" alt="question logo">
//     </a>
//     `
//   const imgSrc = addInfoSchemeLeft.childElementCount === 0
//     ? '../img/1-level.svg'
//     : '../img/1-level2.svg';
//
//     brandItem.innerHTML = `
//
//       <img src="${imgSrc}" alt="img">
//       <span
//         class="ps-2"
//         role='button'
//         >
//         Бренд ${addInfoSchemeLeft.childElementCount + 1}
//       </span>
//     `
//   leftItem.appendChild(brandItem)
//
//
//   brandItem.addEventListener('click', () => {
//       event.preventDefault();
//       addSeries(leftItem);
//     });
//
//   addInfoContent.style.maxHeight = (addInfoContent.scrollHeight + 50) + 'px';
//   addInfoSchemeLeft.classList.add('pt-4')
//   addInfoSchemeLeft.appendChild(leftItem);
//   addInfoSchemeRight.appendChild(rightItem);
// }
//
// const addSeries = (parentItem) => {
//   const inner2lvlItem = document.createElement('div');
//   inner2lvlItem.classList.add('left-inner__2lvl');
//   inner2lvlItem.innerHTML = `
//   <div
//     class="title--h5 hover--red d-flex align-items-end"
//     role='button'
//     style="padding-left: 2rem;"
//     onclick={event.preventDefault()}
//     >
//     <img src="../img/2-level.svg" alt="img">
//     <span class="ps-2">Серия ${parentItem.childElementCount}</span>
//   </div>
//   `
//   addInfoContent.style.maxHeight = (addInfoContent.scrollHeight + 50) + 'px';
//   addInfoSchemeLeft.classList.add('pt-4')
//   parentItem.appendChild(inner2lvlItem);
// }

const addInfoInner = document.querySelector(".add-info__inner");
const addItem = () => {
  event.preventDefault();

  const addInfoRow = document.createElement("div");
  addInfoRow.classList.add("add-info__row", "d-flex");

  const addInfoLeft = document.createElement("div");
  addInfoLeft.classList.add("add-info__left", "col-6 border--right", "pt-4");

  const addInfoRight = document.createElement("div");
  addInfoRight.classList.add("add-info__right", "col-6", "ps-4", "pt-4");

  const leftItem = document.createElement("div");
  leftItem.classList.add(
    "left-inner__item",
    "title--h5",
    "hover--red",
    "d-flex",
    "align-items-end",
    "ps-2"
  );

  const rightItem = document.createElement("div");
  rightItem.classList.add(
    "right-inner__item",
    "title--h5",
    "hover--red",
    "d-flex",
    "align-items-end",
    "ps-2"
  );
};