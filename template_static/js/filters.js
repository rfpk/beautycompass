document.addEventListener("DOMContentLoaded", function () {
  const filterBtn = document.querySelector(".filter__mobile-btn");
  const filters = document.querySelector(".filter");

  filterBtn.addEventListener("click", function () {
    if (filters.classList.contains("filter--active")) {
      filters.classList.remove("filter--active");
    } else {
      filters.classList.add("filter--active");
    }
  });
});
