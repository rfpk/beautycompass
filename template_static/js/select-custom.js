const selectContainers = document.querySelectorAll(".select__custom");

selectContainers.forEach((selectContainer) => {
  const selectHeader = selectContainer.querySelector(".select__header");
  const selectOptions = selectContainer.querySelector(".select__options");
  const selectedValueElement = selectContainer.querySelector(".select__header-selected");

  selectHeader.addEventListener("click", function () {
    selectOptions.classList.contains("open") ? selectOptions.classList.remove("open") : selectOptions.classList.add("open");
  });

  const options = selectContainer.querySelectorAll(".option");
  options.forEach(function (option) {
    option.addEventListener("click", function () {
      const selectedValue = option.textContent;
      selectedValueElement.textContent = selectedValue;
      selectOptions.classList.remove("open");
    });
  });

  document.addEventListener("click", function (event) {
    if (!selectContainer.contains(event.target)) {
      selectOptions.classList.remove("open");
    }
  });
});