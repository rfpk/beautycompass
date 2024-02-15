
  document.addEventListener("DOMContentLoaded", function () {
    const select = document.querySelector(".tags__select");
    const selectHeader = document.querySelector(".select__header");
    const selectOptions = document.querySelector(".select__options");
    const optionSelected = document.querySelector(".tags__selected");
    const options = document.querySelectorAll(".tags__option");
    const textDefault = document.querySelector(".text-default");

    select.addEventListener("click", function (event) {

      // console.log('123')
      // if (selectOptions.classList.contains("open")) {
      //   selectOptions.classList.remove("open");
      // } else {
      //   selectOptions.classList.add("open");
      // }
  });

    options.forEach(function (option, index) {
    const optionId = `option-${index + 1}`;
    option.id = optionId;
    option.setAttribute("data-option-id", optionId);
    option.setAttribute("data-option-name", option.textContent);
    option.addEventListener("click", function () {

    const selectedValue = option.textContent
    const selectedOptionId = option.getAttribute("data-option-id")
    const selectedOptionName = option.getAttribute("data-option-name")

    const existingTagById = optionSelected.querySelector(`[data-tag-id="${selectedOptionId}"]`);
    const existingTagByName = optionSelected.querySelector(`[data-tag-name="${selectedOptionName}"]`);

    if (existingTagById) {
    optionSelected.removeChild(existingTagById);
    option.classList.remove("active");
  } else if (existingTagByName) {
    optionSelected.removeChild(existingTagByName);
    option.classList.remove("active");
  } else {
    const tag = document.createElement('div');
    tag.classList.add('tags__item');
    tag.setAttribute("data-tag-id", selectedOptionId);
    tag.innerHTML = `${selectedValue}`;
    option.classList.add("active");
    optionSelected.appendChild(tag);
  }

    const tagsExist = optionSelected.querySelector('.tags__item');
    if (!tagsExist) {
    textDefault.style.display = 'block';
    // optionSelected.classList.remove("filled");
  } else {
    textDefault.style.display = 'none';
    // optionSelected.classList.add("filled");
  }
    // console.log('tags-option: ' + selectedValue);

  })
  });

    document.addEventListener("click", function (event) {
    if (!event.target.closest(".tags__select")) {
    if (!event.target.closest(".select__options")) {
    selectOptions.classList.remove("open");
  }
  }
  });

    selectOptions.addEventListener("click", function (event) {
    event.stopPropagation();
  });

    optionSelected.addEventListener("click", function (event) {
    if (event.target.classList.contains("tags__item")) {
    const tagId = event.target.getAttribute("data-tag-id");
    const correspondingOption = select.querySelector(`.tags__option[data-option-id="${tagId}"]`);

    if (correspondingOption) {
    correspondingOption.classList.remove("active");
  }

    optionSelected.removeChild(event.target);

    const tagsExist = optionSelected.querySelector('.tags__item');
    if (!tagsExist) {
    textDefault.style.display = 'block';
  } else {
    textDefault.style.display = 'none';
  }

    event.stopPropagation();
  }
  });
})

