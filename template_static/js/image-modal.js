const modal = document.getElementById("imageModal");

const images = document.querySelectorAll("[data-modal-image]");
const modalImg = document.getElementById("img01");
images.forEach((img) => {
  img.onclick = function () {
    modal.style.display = "block";
    modalImg.src = this.src;
  };
});

const closeSpan = document.getElementsByClassName("image-modal__close")[0];

closeSpan.onclick = function () {
  modal.style.display = "none";
};
