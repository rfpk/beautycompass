
const select = document.querySelector(".tags__select");


const selectHeader = document.querySelector(".select__header");

const selectOptions = document.querySelector(".select__options");
const tagsContent = document.querySelector(".tags__content");
const optionSelected = document.querySelector(".tags__selected");

select.addEventListener("click", function () {
  if (selectOptions.classList.contains("open")) {
    selectOptions.classList.remove("open");
  } else {
    selectOptions.classList.add("open");
  }
})

const options = document.querySelectorAll(".tags__option");
options.forEach(function (option, index) {

  const optionId = `${option.textContent}`;
  option.setAttribute("data-option-id", optionId);

  option.addEventListener("click", function () {
    const selectedValue = option.textContent;
    const selectedOptionId = option.getAttribute("data-option-id");

    optionSelected.textContent = selectedValue;

    const existingTag = tagsContent.querySelector(`[data-tag-id="${selectedOptionId}"]`);

    if (existingTag) {
      tagsContent.removeChild(existingTag);
      option.classList.remove("active");
    } else {
      const tag = document.createElement('div');
      tag.classList.add('tags__item');
      tag.setAttribute("data-tag-id", selectedOptionId);
      tag.innerHTML = `<span>${selectedValue}</span>`;
      option.classList.add("active");
      tagsContent.appendChild(tag);
    }

    selectOptions.classList.remove("open");

    const tagsExist = tagsContent.querySelector('.tags__item');
    if (!tagsExist) {
      optionSelected.textContent = 'Выберите значение';
      tagsContent.classList.remove("filled");
    } else {
      optionSelected.textContent = selectedValue;
      tagsContent.classList.add("filled");
    }

    console.log('tags-option: ' + selectedValue);
  });
});

document.addEventListener("click", function (event) {
  if (!event.target.closest(".brand__tags-select")) {
    selectOptions.classList.remove("open");
  }
});