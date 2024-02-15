


const selectWrap = document.querySelector(".select-assignment");
const sOptions = selectWrap.querySelector(".select-assignment__options");
const sOption = sOptions.querySelectorAll('.option')

console.log(sOption)

selectWrap.addEventListener("click", function () {

  // sOptions.classList.add('open')

  sOption.forEach((option) => {
    option.addEventListener('click', function () {
      option.classList.add('active')
    })
  })

})

document.addEventListener("click", function (event) {
  if (!selectWrap.contains(event.target)) {
    sOptions.classList.remove("open");
  }
});


// selectContainers.forEach((selectContainer) => {
//   const selectHeader = selectContainer.querySelector(".select__header");
//   const selectOptions = selectContainer.querySelector(".select__options");
//   const selectedValueElement = selectContainer.querySelector(".select__header-selected");
//
//   selectHeader.addEventListener("click", function () {
//     selectOptions.classList.add("open");
//   });
//
//   const options = selectContainer.querySelectorAll(".option");
//   options.forEach(function (option) {
//     option.addEventListener("click", function () {
//       // const selectedValue = option.textContent;
//       // selectedValueElement.textContent = selectedValue;
//       // selectOptions.classList.remove("open");
//       option.classList.add('active')
//     });
//   });
//
//   document.addEventListener("click", function (event) {
//     if (!selectContainer.contains(event.target)) {
//       selectOptions.classList.remove("open");
//     }
//   });
// });