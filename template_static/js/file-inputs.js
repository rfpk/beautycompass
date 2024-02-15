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
    console.log("Загруженный файл:", file.name);
  }
}




