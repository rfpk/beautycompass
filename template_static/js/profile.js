// // accordion
// const addInfoTrigger = document.querySelector(".add-info__trigger");
// const addInfoContent = document.querySelector(".add-info__content");
// const addInfoArrow = document.querySelector(".add-info__trigger img");
// const questionSign = document.querySelector(".question-sign");
// let isOpen = false;
//
// addInfoTrigger.addEventListener("click", function () {
//   if (!isOpen) {
//     addInfoContent.style.maxHeight = addInfoContent.scrollHeight + 20 + "px";
//     isOpen = true;
//     addInfoArrow.style.transform = "rotate(180deg)";
//     addInfoContent.style.margin = "1.5rem 0 1rem 0";
//   } else {
//     addInfoContent.style.maxHeight = "0";
//     isOpen = false;
//     addInfoArrow.style.transform = "rotate(0)";
//     addInfoContent.style.paddingTop = "0px";
//     addInfoContent.style.margin = "0";
//   }
// });
//
// // tooltip
// tippy(".left__question", {
//   content: '<div class="cloud">Пример текста</div>',
//   theme: "light",
//   placement: "top-start",
//   arrow: false,
//   allowHTML: true,
// });
//
// tippy(".right__question", {
//   content:
//     '<div class="cloud">Вы можете задать порядок отображения средств перемещая их иконки</div>',
//   theme: "light",
//   placement: "top-start",
//   arrow: false,
//   allowHTML: true,
// });
//
// // creating brands
//
// // const addInfoSchemeLeft = document.querySelector('.add-info__schemes .left .left-inner');
// // const addInfoSchemeRight = document.querySelector('.add-info__schemes .right .right-inner');
// //
// // const addItem = () => {
// //   event.preventDefault();
// //   const leftItem = document.createElement('div');
// //   leftItem.classList.add('left-inner__item');
// //   const brandItem = document.createElement('div');
// //   brandItem.classList.add('left-inner__brand', 'title--h5', 'hover--red',
// //     'd-flex', 'align-items-end', 'ps-2');
// //   brandItem.id = 'left-inner__brand-' + addInfoSchemeLeft.childElementCount + 1
// //
// //   const rightItem = document.createElement('div');
// //   rightItem.classList.add('right-inner__item');
// //   // rightItem.classList.add('my-3')
// //   rightItem.innerHTML = `
// //     <a
// //       href=""
// //       class="right__title title--h5 hover--red text-decoration-none position-relative">
// //       <span>Бренд ${addInfoSchemeRight.childElementCount + 1}</span>
// //       <img class="question right__question d-none d-md-inline mx-2" src="../img/plus-rect.svg" alt="question logo">
// //     </a>
// //     `
// //   const imgSrc = addInfoSchemeLeft.childElementCount === 0
// //     ? '../img/1-level.svg'
// //     : '../img/1-level2.svg';
// //
// //     brandItem.innerHTML = `
// //
// //       <img src="${imgSrc}" alt="img">
// //       <span
// //         class="ps-2"
// //         role='button'
// //         >
// //         Бренд ${addInfoSchemeLeft.childElementCount + 1}
// //       </span>
// //     `
// //   leftItem.appendChild(brandItem)
// //
// //
// //   brandItem.addEventListener('click', () => {
// //       event.preventDefault();
// //       addSeries(leftItem);
// //     });
// //
// //   addInfoContent.style.maxHeight = (addInfoContent.scrollHeight + 50) + 'px';
// //   addInfoSchemeLeft.classList.add('pt-4')
// //   addInfoSchemeLeft.appendChild(leftItem);
// //   addInfoSchemeRight.appendChild(rightItem);
// // }
// //
// // const addSeries = (parentItem) => {
// //   const inner2lvlItem = document.createElement('div');
// //   inner2lvlItem.classList.add('left-inner__2lvl');
// //   inner2lvlItem.innerHTML = `
// //   <div
// //     class="title--h5 hover--red d-flex align-items-end"
// //     role='button'
// //     style="padding-left: 2rem;"
// //     onclick={event.preventDefault()}
// //     >
// //     <img src="../img/2-level.svg" alt="img">
// //     <span class="ps-2">Серия ${parentItem.childElementCount}</span>
// //   </div>
// //   `
// //   addInfoContent.style.maxHeight = (addInfoContent.scrollHeight + 50) + 'px';
// //   addInfoSchemeLeft.classList.add('pt-4')
// //   parentItem.appendChild(inner2lvlItem);
// // }
//
// const addInfoInner = document.querySelector(".add-info__inner");
//
// const addItem = () => {
//   event.preventDefault();
//
//   const addInfoRow = document.createElement("div");
//   addInfoRow.classList.add("add-info__row", "d-flex");
//
//   const addInfoLeft = document.createElement("div");
//   addInfoLeft.classList.add("add-info__left", "col-6 border--right", "pt-4");
//
//   const addInfoRight = document.createElement("div");
//   addInfoRight.classList.add("add-info__right", "col-6", "ps-4", "pt-4");
//
//   const leftItem = document.createElement("div");
//   leftItem.classList.add(
//     "left-inner__item",
//     "title--h5",
//     "hover--red",
//     "d-flex",
//     "align-items-end",
//     "ps-2"
//   );
//
//   const rightItem = document.createElement("div");
//   rightItem.classList.add(
//     "right-inner__item",
//     "title--h5",
//     "hover--red",
//     "d-flex",
//     "align-items-end",
//     "ps-2"
//   );
// };
//
// // modal price
// const modalPrices = document.getElementById("modal--prices");
// const modalPricesConfirm = document.getElementById("modal--confirm");
// const modalPricesCells = modalPrices.querySelectorAll(".table tr td");
//
// modalPricesCells.forEach((cell) => {
//   cell.setAttribute("data-bs-dismiss", "modal");
//   cell.setAttribute("data-bs-toggle", "modal");
//   cell.setAttribute("href", "#modal--confirm");
//
//   cell.addEventListener("click", () => {
//     console.log(cell);
//
//     const cellElement = cell.querySelector("span");
//     if (cellElement) {
//       const cellPrice = cellElement.textContent.trim();
//       const cellNumber = parseInt(cellPrice);
//       if (!isNaN(cellNumber)) {
//         console.log("Число внутри ячейки:", cellNumber);
//       } else {
//         console.log("Содержимое внутри ячейки не является числом:", cellPrice);
//       }
//     }
//   });
// });


// accordion
const addInfoTrigger = document.querySelector(".add-info__trigger");
const addInfoContent = document.querySelector(".add-info__content");
const addInfoArrow = document.querySelector(".add-info__trigger img");
const questionSign = document.querySelector(".question-sign");
let isOpen = false;

addInfoTrigger.addEventListener("click", function () {
  if (!isOpen) {
    addInfoContent.style.maxHeight = "none";
    isOpen = true;
    addInfoArrow.style.transform = "rotate(180deg)";
    addInfoContent.style.margin = "1.5rem 0 1rem 0";
  } else {
    addInfoContent.style.maxHeight = "0";
    isOpen = false;
    addInfoArrow.style.transform = "rotate(0)";
    addInfoContent.style.paddingTop = "0px";
    addInfoContent.style.margin = "0";
  }
});
const addInfoInner = document.querySelector(".add-info__inner");

const addItem = (event) => {
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

// modal price
const modalPrices = document.getElementById("modal--prices");
const modalPricesConfirm = document.getElementById("modal--confirm");
let modalPricesCells;

if (modalPrices) {
  modalPricesCells = modalPrices.querySelectorAll(".table tr td");

  modalPricesCells.forEach((cell) => {
    cell.setAttribute("data-bs-dismiss", "modal");
    cell.setAttribute("data-bs-toggle", "modal");
    cell.setAttribute("href", "#modal--confirm");

    cell.addEventListener("click", () => {
      console.log(cell);

      const cellElement = cell.querySelector("span");
      if (cellElement) {
        const cellPrice = cellElement.textContent.trim();
        const cellNumber = parseInt(cellPrice);
        if (!isNaN(cellNumber)) {
          console.log("Число внутри ячейки:", cellNumber);
        } else {
          console.log("Содержимое внутри ячейки не является числом:", cellPrice);
        }
      }
    });
  });
}


var outputInfoDetails=''

//предпологаемый и желаемый JSON данные в manufacter-lk/profile.json

function fetchJSONFile(path, callback) {
  //path ссыллка на ресурс получения
  //callback что делать с полученными данными
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function() {
      if (httpRequest.readyState === 4) {
          if (httpRequest.status === 200) {
              var data = JSON.parse(httpRequest.responseText);
              if (callback) callback(data);
          }
      }
  };
  httpRequest.open('GET', path);
  httpRequest.send();
}

var globalPageSize=4

//функция вывода данных

$('#remItm').on('show.bs.modal', function (event) {

  const buttonPar =  event.relatedTarget

  let butRem= event.currentTarget.children[0].children[0].children[2].children[0]

  const pathDB=buttonPar.getAttribute('data-bs-pathDB')

  const idItm=buttonPar.getAttribute('data-bs-idItm')

  $(butRem).click(function (e) {

    //обработка данных с сервера

    // $.ajax({
    //   type: "post",
    //   url: "url",
    //   data: [pathDB, idItm],
    //   dataType: "json",
    //   success: function (response) {

    //     $('#remItm').modal('toggle');
    //   }
    // });

    console.log('удаление прошло');

    $('#remItm').modal('hide')
  });

})

function outputInfo(outpBlock, arraysData, objLabAddBut, classNexPag, collectBD,collectChange,lastTrig=false, selectPage=1, elStart=0 ,pageItemCount=globalPageSize) {

  // outpBlock, блок для вывода
  // arraysData, набор массивов для вывода
  // objLabAddBut, объект с данными о надписи на поиске, и данных кнопок
  // classNexPag, класс для последующих вложений

  // collectBD набор бд для запросов,
  // collectChange набор бд для пересылки на изменяющую страницу,

  // lastTrig=false, если последний в иерархии, то true
  // selectPage=1, выбранная страница, как правило не меняется, но всякое может быть
  // elStart=0 , с какого элемента начинать вывод
  // pageItemCount=globalPageSize кол-во выводимых элементов

  html='<div class="outputInf">'

    html+='<div class="details__search_wrap">'
    +'<div class="input input--general">'
    +'  <label for="search" class="details__search label label--light label--profile">'
    +objLabAddBut.labelSearch
    +'</label>'
    +'  <input id="search" value="" type="text" class="details__search-input ">'
    +'</div>'
    objLabAddBut.buttons.forEach(button=>{
      html+='  <a href="'+button.link+'" class="details__btn btn btn--blue"> '
      +'    <p class="text--15-25">'
      +button.text
      +'</p>'
      +'  </a>'
    })
    html+='</div>'

    let arrayData=[]

    let trigNextClass=-1

    arraysData.forEach(el=>{
      if (el!=undefined) {
        el.forEach(e=>{
          arrayData.push(e)
        })
        if(collectBD.length>1 && trigNextClass==-1){
          trigNextClass=arrayData.length
        }
      }

    })

    if (arrayData[0]!=undefined) {

        html+='<ul class="all-object">'

        for (let i = 0; i < arrayData.length; i++) {
          const element = arrayData[i];

          html+='<div class="details__view '

          if(i<elStart || i>elStart+pageItemCount) html+='d-none">'
          else html+='">'

              html+='<input type="text" value="'+element.place_display+'" class="details__view-place">'
              +'<details class="details">'
              +'<summary class="details__summary '

              if( lastTrig || i>=trigNextClass && trigNextClass!=-1 ) html+='details__summary--last-item '
              html+='">'
              html+='<p class="title--h5">'+element.name+'</p>'
              +'<div class="details-button">    '
              +'<a class="details-button__edit btn change_item" href="'
              if(i<trigNextClass)
                html+=collectChange[1]
              else
                html+=collectChange[0]

              //get параметры, не знаю какие параметры нужны, поэтому пока id передам

              html+='?id='+element.idDB+'">'

              +'<img src="../img/btn_pen.svg" alt="Изменить"></a>'
              +'<a data-bs-toggle="modal" '
              +'data-bs-pathDB="'

              if(i<trigNextClass)
                html+=collectBD[1]
              else
                html+=collectBD[0]

              html+='"'
              +'data-bs-idItm="' +element.idDB+'"'

              html+=' data-bs-target="#remItm" class="details-button__del btn rem_item">'
              +'<img src="../img/destr.svg" alt="Удаление">'

              html+='</a>'
              +'</div>'
              +'</summary>'
              if(classNexPag!=''){
                html+='<div class="content">'
                +'<div class="pagin__output-info">  '
                +'<div class="pagin__output-info" id="view-all-'+classNexPag+'-'+element.idDB+'">'
                +'</div>'
                +'</div>'
                +'</div>'
              }
              html+='</details>'


          html+='</div>'
        }

        html+='</ul>'

        if (arrayData.length>pageItemCount) {

          html+='<div class="paginationjs">'
          +'            <div class="paginationjs-pages">'
          +'              <ul>'
          +'                <li class="paginationjs-prev ">'
          +'                  <a></a>'
          +'                </li>'

          for (let i = 1; i < Math.ceil(arrayData.length/pageItemCount); i++) {
            html+='<li class="paginationjs-page J-paginationjs-page'
            if (i==selectPage) {
              html+=' active'
            }
            html+='" data-num="'+i+'">'
            +'<a>'+i+'</a>'
            +'</li>'
          }

          html+='                <li class="paginationjs-next ">'
          +'                  <a></a>'
          +'                </li>'
          +'              </ul>'
          +'            </div>'
          +'          </div>'
          html+='</div>'
        }
      }

      $(outpBlock).html(html)
}

function changePage(params) {

  //самодельная пагинация

  //объекты для сортировки
  collectSort=params.data.pageSelect.parentElement.parentElement.parentElement.parentElement.children[1].children

  for (let i = 0; i < collectSort.length; i++) {
    const element = collectSort[i];
    //скрытие всех элементов
    element.classList.add('d-none')
  }

  numListActive=-1

  switch (params.data.pageSelect.attributes[0].value.split(' ')[0].split('-')[1]) {
    case 'page':

      selectPage=params.data.pageSelect.attributes[1].value

      searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
      next=searchArray.pop().previousElementSibling
      prev=searchArray.shift().nextElementSibling

      searchArray.forEach(el=>{
        if(el.classList.contains('active')){
          el.classList.remove('active');
        }
      })

      params.data.pageSelect.classList.add('active')


      if(selectPage<=prev.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[0])[0].classList.add('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

      }else if(selectPage+1>=next.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.add('disabled')

      }else{
        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')
      }

      break;
    case 'prev':

      if (!params.data.pageSelect.classList.contains('disabled')) {
        activeValue=0;

        searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
        trash=searchArray.pop()
        trash=searchArray.shift()

        for (let ch = 0; ch < searchArray.length; ch++) {
          const child = searchArray[ch];

          if(child.classList[2]=='active'){

            numListActive=ch

            activeValue=Number(child.attributes["data-num"].value)

            child.classList.remove('active')
          }
        }

        if(activeValue-1>=params.data.pageSelect.nextElementSibling.attributes[1].value)
          selectPage=activeValue-1
        else
          selectPage=params.data.pageSelect.nextElementSibling.attributes[1].value



        if(activeValue-1<=params.data.pageSelect.nextElementSibling.attributes[1].value){

          $(params.data.pageSelect.parentElement.children[0])[0].classList.add('disabled')

          $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        }else if(activeValue-1>params.data.pageSelect.nextElementSibling.attributes[1].value){

          $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

          $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        }else{

        }

        if(numListActive-1>=0 )
          searchArray[numListActive-1].classList.add('active')
        else
          searchArray[0].classList.add('active')
      }

      break;
    case 'next':

    if (!params.data.pageSelect.classList.contains('disabled')) {

      activeValue=0;

      searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
      trash=searchArray.pop()
      trash=searchArray.shift()

      for (let ch = 0; ch < searchArray.length; ch++) {
        const child = searchArray[ch];

        if(child.classList[2]=='active'){

          numListActive=ch

          activeValue=Number(child.attributes["data-num"].value)

          child.classList.remove('active')

        }
      }

      if(activeValue+1<=params.data.pageSelect.previousElementSibling.attributes[1].value)
        selectPage=activeValue+1
      else
        selectPage=params.data.pageSelect.previousElementSibling.attributes[1].value

      if(activeValue+1>=params.data.pageSelect.previousElementSibling.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.add('disabled')

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

      }else if(activeValue+1<params.data.pageSelect.previousElementSibling.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

      }else{

      }

      if(numListActive+1<=searchArray.length )

        numListActive+1==searchArray.length ? searchArray[searchArray.length-1].classList.add('active') : searchArray[numListActive+1].classList.add('active')
      else
        searchArray[searchArray.length-1].classList.add('active')

    }

      break;
  }

  startCikle=Number(selectPage)
  finishCikle=0

  startCikle==1 ? startCikle=0 : startCikle=globalPageSize*(Number(selectPage)-1)+1

  finishCikle=startCikle+globalPageSize

  for (let i = startCikle; i <= finishCikle; i++) {

    const element = collectSort[i];
    if(element==undefined)
      break;
    //скрытие всех элементов
    element.classList.remove('d-none')
  }

  html=new DOMParser().parseFromString('<li class="paginationjs-page J-paginationjs-page disabled"><a>...</a></li>', "text/html").getElementsByTagName("li")[0]

  for (let k = 1; k < params.data.pageSelect.parentElement.children.length-1; k++) {
    const element = params.data.pageSelect.parentElement.children[k];
    const elemPrev=params.data.pageSelect.parentElement.children[k-1]
    const elemNext=params.data.pageSelect.parentElement.children[k+1]

    element.classList.add('d-none')

    if(!(k==1 || k==params.data.pageSelect.parentElement.children.length-2)){

      if(element.classList.contains('active')){

        element.classList.remove('d-none')

        if(k-1!=1){
          if (k-2>3) {
            //перенести выше в отдельную переменную

            // console.log('Добавить блок с точками после');
          }

          element.classList.remove('d-none')
        }
        if(k+1!=(element.parentElement.children.length-1)){
          if (k+2<(element.parentElement.children.length-2)) {
            //перенести выше в отдельную переменную

            // console.log('Добавить блок с точками перед');
          }

          element.classList.remove('d-none')
        }
      }
      else{
        if(params.data.pageSelect.parentElement.children[k-1].classList.contains('active') || params.data.pageSelect.parentElement.children[k+1].classList.contains('active'))
          element.classList.remove('d-none')
      }
      if(k==Math.ceil((element.parentElement.children.length-1)/2))
        element.classList.remove('d-none')
    }
    else{
      element.classList.remove('d-none')

      if(element.classList.contains('active'))
        k==1 ? element.parentElement.children[k+1].classList.remove('d-none') : element.parentElement.children[k-1].classList.remove('d-none')
    }
  }
}

function search(el){

searchText=el.data.input.value

allObject=el.data.input.parentElement.parentElement.parentElement.children[1].children

paginBlock=el.data.input.parentElement.parentElement.parentElement.children[2]

for (let i = 0; i < allObject.length; i++) {
  const element = allObject[i];
  element.classList.remove('d-none')
}

for (let i = 0; i < allObject.length; i++) {
  const element = allObject[i];

  if(!element.children[1].children[0].children[0].outerText.includes(searchText)){
    element.classList.add('d-none')
  }
}

if(searchText==''){
  paginBlock.classList.add('d-block')
  paginBlock.classList.remove('d-none')

  for (let i = 0; i < allObject.length; i++) {
    const element = allObject[i];
    element.classList.add('d-none')
  }

  pageArray=paginBlock.children[0].children[0].children

  selectPage=-1

  for (let k = 1; k < pageArray.length-1; k++) {
    const element = pageArray[k];
    if (element.classList.contains('active')) {

      selectPage=element.attributes[1].value
    }
  }

  startCikle=Number(selectPage)
  finishCikle=0

  startCikle==1 ? startCikle=0 : startCikle=globalPageSize*(Number(selectPage)-1)+1

  finishCikle=startCikle+globalPageSize

  for (let i = startCikle; i <= finishCikle; i++) {

    const element = allObject[i];
    if(element==undefined)
      break;
    //скрытие всех элементов
    element.classList.remove('d-none')
  }
}
else{
  paginBlock.classList.add('d-none')
  paginBlock.classList.remove('d-block')
}

}

//анимация details
class Accordion {
  constructor(el) {
    this.el = el;
    this.summary = el.querySelector('summary');
    this.content = el.querySelector('.content');

    this.animation = null;
    this.isClosing = false;
    this.isExpanding = false;
    this.summary.addEventListener('click', (e) => this.onClick(e));
  }

  onClick(e) {
    e.preventDefault();
    this.el.style.overflow = 'hidden';
    if (this.isClosing || !this.el.open) {
      this.open();
    } else if (this.isExpanding || this.el.open) {
      this.shrink();
    }
  }

  shrink() {
    this.isClosing = true;

    const startHeight = `${this.el.offsetHeight}px`;
    const endHeight = `${this.summary.offsetHeight}px`;

    if (this.animation) {
      this.animation.cancel();
    }

    this.animation = this.el.animate({
      height: [startHeight, endHeight]
    }, {
      duration: 400,
      easing: 'ease-out'
    });
    this.animation.onfinish = () => this.onAnimationFinish(false);
    this.animation.oncancel = () => this.isClosing = false;
  }

  open() {
    this.el.style.height = `${this.el.offsetHeight}px`;
    this.el.open = true;
    window.requestAnimationFrame(() => this.expand());
  }

  expand() {
    this.isExpanding = true;
    const startHeight = `${this.el.offsetHeight}px`;
    const endHeight = `${this.summary.offsetHeight + this.content.offsetHeight}px`;

    if (this.animation) {
      this.animation.cancel();
    }

    this.animation = this.el.animate({
      height: [startHeight, endHeight]
    }, {
      duration: 400,
      easing: 'ease-out'
    });
    this.animation.onfinish = () => this.onAnimationFinish(true);
    this.animation.oncancel = () => this.isExpanding = false;
  }

  onAnimationFinish(open) {
    this.el.open = open;
    this.animation = null;
    this.isClosing = false;
    this.isExpanding = false;
    this.el.style.height = this.el.style.overflow = '';
  }
}
// Присваивание анимаций
document.querySelectorAll('.add-info__schemes details').forEach((el) => {
  new Accordion(el);
});

//вывод информации с помощью пагинации
//производитель

var adressDB={
  tabels:[
    "link_to_brands",
    "link_to_serie",
    "link_to_cosmetic",
  ]
}

var adressChages={
  links:[
    'page-brand-info.html',
    'page-series-info.html',
    'page-product-info.html',
  ]
}

function outputInfBrands(){

  var prompt = new Promise((resolve, reject) => {

    fetchJSONFile('profile.json', function(data){
      outputInfoDetails=data
      resolve(outputInfoDetails)
    });

  });

  prompt.then(data=>{

    return new Promise((resolve, reject)=>{

      var classPg='brand'

      outputInfo($('#view-all-item'), [data.brands],
      {
        labelSearch:'Поиск бренда',
        buttons:[
          {
            link:adressChages.links[0],
            text:'Добавить бренд',
          },
        ]
      }
      ,classPg, [adressDB.tabels[0]],[adressChages.links[0]] )

      params=[{
        brands:data.brands,
        class:classPg
      }]
      resolve(params)
    })
  }).then(params=>{

    return new Promise((resolve, reject)=>{
      brandWithSer=[];

      var nxtClassPg='serie'

      output: for (let k = 0; k < params[0].brands.length; k++) {
        const brand = params[0].brands[k];

        if(brand.series != undefined && brand.cosmetics != undefined){
          outputInfo($('#view-all-'+params[0].class+'-'+brand.idDB), [brand.series,brand.cosmetics],
          {
            labelSearch:'Поиск  средства/серии',
            buttons:[
              {
                link:adressChages.links[1],
                text:'Добавить серию',
              },
              {
                link:adressChages.links[2],
                text:'Добавить средство',
              },
            ]
          },nxtClassPg,[adressDB.tabels[1], adressDB.tabels[2] ],[adressChages.links[1], adressChages.links[2] ] ,false  )

          brand.series.forEach(serie=>{
            outputInfo($('#view-all-'+nxtClassPg+'-'+serie.idDB), [serie.cosmetics],
            {
              labelSearch:'Поиск  средства',
              buttons:[
                {
                  link:adressChages.links[2],
                  text:'Добавить средство',
                },
              ]
            }
            ,'',[adressDB.tabels[2]],[adressChages.links[2]],true )
          })

          continue output;
        }

        if (brand.series != undefined) {
          brandWithSer.push(brand)
        }

        outputInfo($('#view-all-'+params[0].class+'-'+brand.idDB), [brand.cosmetics],
        {
          labelSearch:'Поиск средства/серии',
          buttons:[
            {
              link:adressChages.links[1],
              text:'Добавить серию',
            },
            {
              link:adressChages.links[2],
              text:'Добавить средство',
            },
          ]
        },'',[adressDB.tabels[2]],[adressChages.links[2]],true  )

      }

      resolve({brands:brandWithSer,classPrev:params[0].class,class:nxtClassPg})

    })
  })
  .then((brandWithSer)=>{

    var outputCosmetic=[];

    return new Promise((resolve, reject)=>{
      brandWithSer.brands.forEach((brand)=>{

          outputInfo($('#view-all-'+brandWithSer.classPrev+'-'+brand.idDB), [brand.series],
          {
            labelSearch:'Поиск  средства/ серии',
            buttons:[
              {
                link:adressChages.links[1],
                text:'Добавить серию',
              },
              {
                link:adressChages.links[2],
                text:'Добавить средство',
              },
            ]
          },
          brandWithSer.class,[adressDB.tabels[1]],[adressChages.links[1]] )

          outputCosmetic.push(brand.series)

      })
      resolve({series:outputCosmetic, class:brandWithSer.class})
    })

  }).then((serWithClass)=>{

    return new Promise((resolve, reject)=>{

      outputItem=[]
      serWithClass.series.forEach(cosmetics => {
        cosmetics.forEach(element => {
          outputItem.push(element)
        });
      })

      resolve({outputItem:outputItem, class:serWithClass.class})
    })
  })
  .then((outputInf)=>{

    outputInf.outputItem.forEach(serie => {
      outputInfo($('#view-all-'+outputInf.class+'-'+serie.idDB), [serie.cosmetics],
      {
        labelSearch:'Поиск  средства',
        buttons:[
          {
            link:adressChages.links[2],
            text:'Добавить средство',
          },
        ]
      }
      ,'',[adressDB.tabels[2]],[adressChages.links[2]],true )
  });
  })
  .then(()=>{
    for (let i = 0; i < $('li[class^="paginationjs"]').length; i++) {
      const element = $('li[class^="paginationjs"]')[i];

      triger=false
      element.classList.forEach((classEl)=>{
        if(classEl=='disabled'){
          triger=true
        }
      })
      if(!triger){
        $(element).bind('click', {pageSelect: element}, changePage);
        html=new DOMParser().parseFromString('<li class="paginationjs-page J-paginationjs-page disabled"><a>...</a></li>', "text/html").getElementsByTagName("li")[0]


        for (let k = 1; k < element.parentElement.children.length-1; k++) {
          const pageSelector = element.parentElement.children[k];

          pageSelector.classList.add('d-none')

          if(!(k==1 || k==pageSelector.parentElement.children.length-2)){

            if(pageSelector.classList.contains('active')){

              pageSelector.classList.remove('d-none')

              if(k-1!=1){
                pageSelector.classList.remove('d-none')
              }
              if(k+1!=(pageSelector.parentElement.children.length-1)){
                pageSelector.classList.remove('d-none')
              }
            }else{
              if(pageSelector.parentElement.children[k-1].classList.contains('active') || pageSelector.parentElement.children[k+1].classList.contains('active'))
              pageSelector.classList.remove('d-none')
            }
            if(k==Math.ceil((element.parentElement.children.length-1)/2)){
              pageSelector.classList.remove('d-none')
            }
          }
          else{
            pageSelector.classList.remove('d-none')

            if(pageSelector.classList.contains('active'))
              k==1 ? element.parentElement.children[k+1].classList.remove('d-none') : element.parentElement.children[k-1].classList.remove('d-none')

          }

        }
      }
    }

    for(let i=0;i<$('input[id="search"]').length;i++){
      const element = $('input[id="search"]')[i];
      array=element.parentElement.parentElement.children[1].children
      $(element).bind('keyup', {input: element, arraySearch:array}, search)
    }
  })
}

//присвоить кнопкам удаления функцию
function detais(){

}

$(document).ready(
  outputInfBrands()
)

function handleFileSelected(event) {
  const file = event.target.files[0];
  if (file) {
    // Обработка загруженного файла
    let reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function () {
      let img=$('.profile__body-photo')[0].children[1].children[0]
      img.src=reader.result
      // img.classList.add('upload-img')
      console.log(img)
    }

    console.log("Загруженный файл:", file.name);
  }
}

$('#visPassword').on('click',function(event){

  event.preventDefault()
  if(event.currentTarget.previousElementSibling.type=='password'){
      $('#visPassword').css('background-image','url("/static/img/eye_hide.svg")');
      event.currentTarget.previousElementSibling.type='text'
  }
  else{
      event.currentTarget.previousElementSibling.type='password'
      $('#visPassword').css('background-image','url("/static/img/eye_show.svg")');
  }
})

$('#visPasswordRep').on('click',function(event){

  event.preventDefault()
  if(event.currentTarget.previousElementSibling.type=='password'){
      $('#visPasswordRep').css('background-image','url("/static/img/eye_hide.svg")');
      event.currentTarget.previousElementSibling.type='text'
  }
  else{
      $('#visPasswordRep').css('background-image','url("/static/img/eye_show.svg")');
      event.currentTarget.previousElementSibling.type='password'
  }
})

$('.feed-button__settng').click((e)=>{
  e.preventDefault()
  $('.profile__body-modify')[0].classList.add('active')
  $('.feed-button__settng')[0].classList.add('d-none')
})

$("#sendParam").click((e)=>{
  e.preventDefault()

  let nameProf=$('#name')[0].value
  let phone=$('#phone')[0].value
  let email=$('#email')[0].value
  let passw=$('#pass')[0].value
  let passwRep=$('#passRep')[0].value
  let modal= $('#errorMess')
  let modalHead= $('#errorMess').find('.modal-title')[0]
  let modalBody= $('#errorMess').find('.modal-body')[0]

  let triger=true
  if(
    nameProf=='' &
    phone=='' &
    email=='' &
    passw=='' &
    passwRep==''
  ){
    modalHead.innerText='Не все поля заполнены'
    modalBody.innerText='Проверьте каждое поле'
    modal.modal('show')

    triger=false
  }

  if(!/([\+]?[7|8][\s-(]?[9][0-9]{2}[\s-)]?)?([\d]{3})[\s-]?([\d]{2})[\s-]?([\d]{2})/.test(phone)){
    modalHead.innerText='Неверно введен номер телефона'
    modalBody.innerText='Пример: +70000000000, 80000000000, +7 (000) 000 00 00'
    triger=false
    modal.modal('show')
  }

  if(!/^((([0-9A-Za-z]{1}[-0-9A-z\.]{1,}[0-9A-Za-z]{1})|([0-9А-Яа-я]{1}[-0-9А-я\.]{1,}[0-9А-Яа-я]{1}))@([-A-Za-z]{1,}\.){1,2}[-A-Za-z]{2,})$/u.test(email)){
    modalHead.innerText='Неверно введена почта'
    modalBody.innerText='Пример: 123456@i.ru, 1login@ru.name.ru, логин-1@i.ru'
    triger=false
    modal.modal('show')
  }

  if(!/(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}/g.test(passw)){
    modalHead.innerText='Ваш пароль не подходит'
    modalBody.innerText='Ваш пароль должен содержать хотя бы одна число, хотя бы один спец. символ (!@#$%^&*), хотя бы одна буква в нижнем регистре и в верхнем и состоять из минимум 6 символов'
    triger=false
    modal.modal('show')
  }

  if(passw!=passwRep){
    modalHead.innerText='Подтверждение пароля провалилось'
    modalBody.innerText='Поля "Пароль" и "Повтор пароля" не совпадают'
    triger=false
    modal.modal('show')
  }

  if(triger){
    let form=new FormData($('#profileInfo')[0])
    $.ajax({
      type: "POST",
      url: "#",
      processData: false,
      contentType: false,
      data: form,
      success: function (response) {
        console.log('Отправка на сервер')
        $('.profile__body-modify')[0].classList.remove('active')
        $('.feed-button__settng')[0].classList.remove('d-none')
      }

    });
    $('.profile__body-modify')[0].classList.remove('active')
    $('.feed-button__settng')[0].classList.remove('d-none')
  }

})


// tooltip
// tippy(".left__question", {
//   content: '<div class="cloud">Пример текста</div>',
//   theme: "light",
//   placement: "top-start",
//   arrow: false,
//   allowHTML: true,
// });

// tippy(".right__question", {
//   content:
//     '<div class="cloud">Вы можете задать порядок отображения средств перемещая их иконки</div>',
//   theme: "light",
//   placement: "top-start",
//   arrow: false,
//   allowHTML: true,
// });

// creating brands

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


modalPricesCells.forEach((cell) => {
  cell.setAttribute("data-bs-dismiss", "modal");
  cell.setAttribute("data-bs-toggle", "modal");
  cell.setAttribute("href", "#modal--confirm");

  cell.addEventListener("click", () => {
    console.log(cell);

    const cellElement = cell.querySelector("span");
    if (cellElement) {
      const cellPrice = cellElement.textContent.trim();
      const cellNumber = parseInt(cellPrice);
      if (!isNaN(cellNumber)) {
        console.log("Число внутри ячейки:", cellNumber);
      } else {
        console.log("Содержимое внутри ячейки не является числом:", cellPrice);
      }
    }
  });
});

var outputInfoDetails=''

//предпологаемый и желаемый JSON данные в manufacter-lk/profile.json

function fetchJSONFile(path, callback) {
  //path ссыллка на ресурс получения
  //callback что делать с полученными данными
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function() {
      if (httpRequest.readyState === 4) {
          if (httpRequest.status === 200) {
              var data = JSON.parse(httpRequest.responseText);
              if (callback) callback(data);
          }
      }
  };
  httpRequest.open('GET', path);
  httpRequest.send();
}

var globalPageSize=4

//функция вывода данных

$('#remItm').on('show.bs.modal', function (event) {

  const buttonPar =  event.relatedTarget

  let butRem= event.currentTarget.children[0].children[0].children[2].children[0]

  const pathDB=buttonPar.getAttribute('data-bs-pathDB')

  const idItm=buttonPar.getAttribute('data-bs-idItm')

  $(butRem).click(function (e) {

    //обработка данных с сервера

    // $.ajax({
    //   type: "post",
    //   url: "url",
    //   data: [pathDB, idItm],
    //   dataType: "json",
    //   success: function (response) {

    //     $('#remItm').modal('toggle');
    //   }
    // });

    console.log('удаление прошло');

    $('#remItm').modal('hide')
  });

})

function outputInfo(outpBlock, arraysData, objLabAddBut, classNexPag, collectBD,collectChange,lastTrig=false, selectPage=1, elStart=0 ,pageItemCount=globalPageSize) {

  // outpBlock, блок для вывода
  // arraysData, набор массивов для вывода
  // objLabAddBut, объект с данными о надписи на поиске, и данных кнопок
  // classNexPag, класс для последующих вложений

  // collectBD набор бд для запросов,
  // collectChange набор бд для пересылки на изменяющую страницу,

  // lastTrig=false, если последний в иерархии, то true
  // selectPage=1, выбранная страница, как правило не меняется, но всякое может быть
  // elStart=0 , с какого элемента начинать вывод
  // pageItemCount=globalPageSize кол-во выводимых элементов

  html='<div class="outputInf">'

    html+='<div class="details__search_wrap">'
    +'<div class="input input--general">'
    +'  <label for="search" class="details__search label label--light label--profile">'
    +objLabAddBut.labelSearch
    +'</label>'
    +'  <input id="search" value="" type="text" class="details__search-input ">'
    +'</div>'
    objLabAddBut.buttons.forEach(button=>{
      html+='  <a href="'+button.link+'" class="details__btn btn btn--blue"> '
      +'    <p class="text--15-25">'
      +button.text
      +'</p>'
      +'  </a>'
    })
    html+='</div>'

    let arrayData=[]

    let trigNextClass=-1

    arraysData.forEach(el=>{
      if (el!=undefined) {
        el.forEach(e=>{
          arrayData.push(e)
        })
        if(collectBD.length>1 && trigNextClass==-1){
          trigNextClass=arrayData.length
        }
      }

    })

    if (arrayData[0]!=undefined) {

        html+='<ul class="all-object">'

        for (let i = 0; i < arrayData.length; i++) {
          const element = arrayData[i];

          html+='<div class="details__view '

          if(i<elStart || i>elStart+pageItemCount) html+='d-none">'
          else html+='">'

              html+='<input type="text" value="'+element.place_display+'" class="details__view-place">'
              +'<details class="details">'
              +'<summary class="details__summary '

              if( lastTrig || i>=trigNextClass && trigNextClass!=-1 ) html+='details__summary--last-item '
              html+='">'
              html+='<p class="title--h5">'+element.name+'</p>'
              +'<div class="details-button">    '
              +'<a class="details-button__edit btn change_item" href="'
              if(i<trigNextClass)
                html+=collectChange[1]
              else
                html+=collectChange[0]

              //get параметры, не знаю какие параметры нужны, поэтому пока id передам

              html+='?id='+element.idDB+'">'

              +'<img src="../img/btn_pen.svg" alt="Изменить"></a>'
              +'<a data-bs-toggle="modal" '
              +'data-bs-pathDB="'

              if(i<trigNextClass)
                html+=collectBD[1]
              else
                html+=collectBD[0]

              html+='"'
              +'data-bs-idItm="' +element.idDB+'"'

              html+=' data-bs-target="#remItm" class="details-button__del btn rem_item">'
              +'<img src="../img/destr.svg" alt="Удаление">'

              html+='</a>'
              +'</div>'
              +'</summary>'
              if(classNexPag!=''){
                html+='<div class="content">'
                +'<div class="pagin__output-info">  '
                +'<div class="pagin__output-info" id="view-all-'+classNexPag+'-'+element.idDB+'">'
                +'</div>'
                +'</div>'
                +'</div>'
              }
              html+='</details>'


          html+='</div>'
        }

        html+='</ul>'

        if (arrayData.length>pageItemCount) {

          html+='<div class="paginationjs">'
          +'            <div class="paginationjs-pages">'
          +'              <ul>'
          +'                <li class="paginationjs-prev ">'
          +'                  <a></a>'
          +'                </li>'

          for (let i = 1; i < Math.ceil(arrayData.length/pageItemCount); i++) {
            html+='<li class="paginationjs-page J-paginationjs-page'
            if (i==selectPage) {
              html+=' active'
            }
            html+='" data-num="'+i+'">'
            +'<a>'+i+'</a>'
            +'</li>'
          }

          html+='                <li class="paginationjs-next ">'
          +'                  <a></a>'
          +'                </li>'
          +'              </ul>'
          +'            </div>'
          +'          </div>'
          html+='</div>'
        }
      }

      $(outpBlock).html(html)
}

function changePage(params) {

  //самодельная пагинация

  //объекты для сортировки
  collectSort=params.data.pageSelect.parentElement.parentElement.parentElement.parentElement.children[1].children

  for (let i = 0; i < collectSort.length; i++) {
    const element = collectSort[i];
    //скрытие всех элементов
    element.classList.add('d-none')
  }

  numListActive=-1

  switch (params.data.pageSelect.attributes[0].value.split(' ')[0].split('-')[1]) {
    case 'page':

      selectPage=params.data.pageSelect.attributes[1].value

      searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
      next=searchArray.pop().previousElementSibling
      prev=searchArray.shift().nextElementSibling

      searchArray.forEach(el=>{
        if(el.classList.contains('active')){
          el.classList.remove('active');
        }
      })

      params.data.pageSelect.classList.add('active')


      if(selectPage<=prev.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[0])[0].classList.add('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

      }else if(selectPage+1>=next.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.add('disabled')

      }else{
        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')
      }

      break;
    case 'prev':

      if (!params.data.pageSelect.classList.contains('disabled')) {
        activeValue=0;

        searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
        trash=searchArray.pop()
        trash=searchArray.shift()

        for (let ch = 0; ch < searchArray.length; ch++) {
          const child = searchArray[ch];

          if(child.classList[2]=='active'){

            numListActive=ch

            activeValue=Number(child.attributes["data-num"].value)

            child.classList.remove('active')
          }
        }

        if(activeValue-1>=params.data.pageSelect.nextElementSibling.attributes[1].value)
          selectPage=activeValue-1
        else
          selectPage=params.data.pageSelect.nextElementSibling.attributes[1].value



        if(activeValue-1<=params.data.pageSelect.nextElementSibling.attributes[1].value){

          $(params.data.pageSelect.parentElement.children[0])[0].classList.add('disabled')

          $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        }else if(activeValue-1>params.data.pageSelect.nextElementSibling.attributes[1].value){

          $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

          $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        }else{

        }

        if(numListActive-1>=0 )
          searchArray[numListActive-1].classList.add('active')
        else
          searchArray[0].classList.add('active')
      }

      break;
    case 'next':

    if (!params.data.pageSelect.classList.contains('disabled')) {

      activeValue=0;

      searchArray=Array.prototype.slice.call(params.data.pageSelect.parentElement.children)
      trash=searchArray.pop()
      trash=searchArray.shift()

      for (let ch = 0; ch < searchArray.length; ch++) {
        const child = searchArray[ch];

        if(child.classList[2]=='active'){

          numListActive=ch

          activeValue=Number(child.attributes["data-num"].value)

          child.classList.remove('active')

        }
      }

      if(activeValue+1<=params.data.pageSelect.previousElementSibling.attributes[1].value)
        selectPage=activeValue+1
      else
        selectPage=params.data.pageSelect.previousElementSibling.attributes[1].value

      if(activeValue+1>=params.data.pageSelect.previousElementSibling.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.add('disabled')

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

      }else if(activeValue+1<params.data.pageSelect.previousElementSibling.attributes[1].value){

        $(params.data.pageSelect.parentElement.children[params.data.pageSelect.parentElement.children.length-1])[0].classList.remove('disabled')

        $(params.data.pageSelect.parentElement.children[0])[0].classList.remove('disabled')

      }else{

      }

      if(numListActive+1<=searchArray.length )

        numListActive+1==searchArray.length ? searchArray[searchArray.length-1].classList.add('active') : searchArray[numListActive+1].classList.add('active')
      else
        searchArray[searchArray.length-1].classList.add('active')

    }

      break;
  }

  startCikle=Number(selectPage)
  finishCikle=0

  startCikle==1 ? startCikle=0 : startCikle=globalPageSize*(Number(selectPage)-1)+1

  finishCikle=startCikle+globalPageSize

  for (let i = startCikle; i <= finishCikle; i++) {

    const element = collectSort[i];
    if(element==undefined)
      break;
    //скрытие всех элементов
    element.classList.remove('d-none')
  }

  html=new DOMParser().parseFromString('<li class="paginationjs-page J-paginationjs-page disabled"><a>...</a></li>', "text/html").getElementsByTagName("li")[0]

  for (let k = 1; k < params.data.pageSelect.parentElement.children.length-1; k++) {
    const element = params.data.pageSelect.parentElement.children[k];
    const elemPrev=params.data.pageSelect.parentElement.children[k-1]
    const elemNext=params.data.pageSelect.parentElement.children[k+1]

    element.classList.add('d-none')

    if(!(k==1 || k==params.data.pageSelect.parentElement.children.length-2)){

      if(element.classList.contains('active')){

        element.classList.remove('d-none')

        if(k-1!=1){
          if (k-2>3) {
            //перенести выше в отдельную переменную

            // console.log('Добавить блок с точками после');
          }

          element.classList.remove('d-none')
        }
        if(k+1!=(element.parentElement.children.length-1)){
          if (k+2<(element.parentElement.children.length-2)) {
            //перенести выше в отдельную переменную

            // console.log('Добавить блок с точками перед');
          }

          element.classList.remove('d-none')
        }
      }
      else{
        if(params.data.pageSelect.parentElement.children[k-1].classList.contains('active') || params.data.pageSelect.parentElement.children[k+1].classList.contains('active'))
          element.classList.remove('d-none')
      }
      if(k==Math.ceil((element.parentElement.children.length-1)/2))
        element.classList.remove('d-none')
    }
    else{
      element.classList.remove('d-none')

      if(element.classList.contains('active'))
        k==1 ? element.parentElement.children[k+1].classList.remove('d-none') : element.parentElement.children[k-1].classList.remove('d-none')
    }
  }
}

function search(el){

searchText=el.data.input.value

allObject=el.data.input.parentElement.parentElement.parentElement.children[1].children

paginBlock=el.data.input.parentElement.parentElement.parentElement.children[2]

for (let i = 0; i < allObject.length; i++) {
  const element = allObject[i];
  element.classList.remove('d-none')
}

for (let i = 0; i < allObject.length; i++) {
  const element = allObject[i];

  if(!element.children[1].children[0].children[0].outerText.includes(searchText)){
    element.classList.add('d-none')
  }
}

if(searchText==''){
  paginBlock.classList.add('d-block')
  paginBlock.classList.remove('d-none')

  for (let i = 0; i < allObject.length; i++) {
    const element = allObject[i];
    element.classList.add('d-none')
  }

  pageArray=paginBlock.children[0].children[0].children

  selectPage=-1

  for (let k = 1; k < pageArray.length-1; k++) {
    const element = pageArray[k];
    if (element.classList.contains('active')) {

      selectPage=element.attributes[1].value
    }
  }

  startCikle=Number(selectPage)
  finishCikle=0

  startCikle==1 ? startCikle=0 : startCikle=globalPageSize*(Number(selectPage)-1)+1

  finishCikle=startCikle+globalPageSize

  for (let i = startCikle; i <= finishCikle; i++) {

    const element = allObject[i];
    if(element==undefined)
      break;
    //скрытие всех элементов
    element.classList.remove('d-none')
  }
}
else{
  paginBlock.classList.add('d-none')
  paginBlock.classList.remove('d-block')
}

}