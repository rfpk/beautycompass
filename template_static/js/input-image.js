const profileImagesList = document.querySelectorAll(".profile__images");
profileImagesList.forEach((profileImages) => {

  const profileImagesPlus = profileImages.querySelector('.profile__images-plus');

  profileImagesPlus.addEventListener('click', () => {
    const imagesItem = document.createElement('div')
    imagesItem.classList.add('profile__images-item')

    imagesItem.innerHTML = `
      <div class="input image input--image profile__products-image">
        <div class="profile__image-file_box profile__products-image_item">
            <img
                src="/static/img/gallery-add.svg" alt="logo"
                class="profile__image-file profile__image-file_token profile__image-token profile__products-image_token"
                data-src="/static/img/gallery-add.svg"
            />
            <img
                class="profile__image-file profile__image-file_preview"
            />
            <input
                type="file"
                class="file-input profile__file-input"
            />
        </div>
      </div>
    `;

    const previewImage = imagesItem.querySelector(".profile__image-file_preview");
    const fileInput = imagesItem.querySelector(".file-input");

    fileInput.addEventListener("change", (event) => {
      const currentImagesItem = event.target.closest(".profile__images-item");
      const currentPreviewImage = currentImagesItem.querySelector(".profile__image-file_preview");
      handleFileSelected(event, currentPreviewImage);
    });

    const addButton = imagesItem.querySelector(".input--image");
    addButton.addEventListener("click", () => {
      fileInput.click();
    });

    profileImages.insertBefore(imagesItem, profileImagesPlus);
  });
});

function handleFileSelected(event, previewImage) {
  const selectedFile = event.target.files[0];

  if (selectedFile) {
    const fileReader = new FileReader();

    fileReader.onload = function(e) {
      previewImage.src = e.target.result;
    };

    fileReader.readAsDataURL(selectedFile);
  } else {
    previewImage.src = previewImage.getAttribute("data-src");
  }
}
