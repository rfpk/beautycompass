document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("question-form-btn");
  const form = document.getElementById("question-form");
  const questionInput = document.getElementById("question-input");
  const charCount = document.getElementById("char-count");

  if (openBtn) {
   openBtn.addEventListener("click", () => {
    openBtn.hidden = true;
    form.hidden = false;
    questionInput.focus();
  });
  }

  if (questionInput) {
    questionInput.addEventListener("input", () => {
    const currentLength = questionInput.value.length;
    charCount.textContent = `${currentLength}/500`;
  });
  }
});
