

const elementsWithDataQuestion = document.querySelectorAll("[data-question]");
const productsImageCloud = document.querySelector('.profile__products-image_cloud')



elementsWithDataQuestion.forEach((question, index) => {
  // console.log(question)

  const dataAttributeValue = question.getAttribute("data-question");
  const cloudClass = `${dataAttributeValue}_cloud`;
  question.setAttribute('data-question-id', dataAttributeValue + index);
  const dataId = question.getAttribute("data-question-id");
  const parentElement = question.parentElement;
  const cloud = parentElement.querySelector('.question__cloud')

  question.addEventListener("mouseenter", () => {
    if (cloud) {
      cloud.classList.add('open');
    }
  });

  question.addEventListener("mouseleave", () => {
    if (cloud) {
      cloud.classList.remove('open');
    }
  });

});

window.addEventListener("load", checkScreenWidth);
window.addEventListener("resize", checkScreenWidth);
function checkScreenWidth() {
  if (window.innerWidth >= 1400) {
    productsImageCloud.textContent = `Установите порядок показа превью, перемещая иконки  Фото до 10 МБ. Формат JPG, JPEG, BMP, GIF (размеры, соотношение сторон, максимальный вес итд)`
  } else {
    productsImageCloud.textContent = `Установите порядок показа превью, перемещая иконки`
  }
}
