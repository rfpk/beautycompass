


// ++++++++++++++++++
// === file input ===
// function triggerFileInput() {
//   const fileInput = document.querySelectorAll(".file-input");
//   fileInput.forEach((input) => {
//     input.click();
//   });
// }
// function handleFileSelected(event) {
//   const file = event.target.files[0];
//   if (file) {
//     // Обработка загруженного файла
//     console.log("Загруженный файл:", file.name);
//   }
// }


// ++++++++++++++++++
// === checkboxes ===
const customCheckboxes = document.querySelectorAll('input[type="checkbox"]');
customCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', () => {
    const parentClass = checkbox.parentElement.classList[0];
    if (checkbox.checked) {
      console.log('чекбокс: ' + parentClass + ' отмечен');
    } else {
      console.log('чекбокс: ' + parentClass + ' отметка снята');
    }
  });
});


// +++++++++++++++++++++
// === tagging-cards ===

const tagsCount = document.querySelectorAll('i.tag-count')
tagsCount.forEach((tag) => {
  tag.addEventListener('click', () => {
    console.log(+tag.textContent);
  })
})
