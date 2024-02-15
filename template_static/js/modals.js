// modal price
const modalPrices = document.getElementById("modal--prices");
const modalPricesConfirm = document.getElementById("modal--confirm");
const modalPricesCells = modalPrices.querySelectorAll(".table tr td");

modalPricesCells.forEach((cell) => {
  cell.setAttribute("data-bs-dismiss", "modal");
  cell.setAttribute("data-bs-toggle", "modal");
  cell.setAttribute("href", "#modal--confirm");

  cell.addEventListener("click", () => {
    console.log(cell);

    const cellElement = cell.querySelector("span");
    if (cellElement) {
      const cellPrice = cellElement.textContent.trim();
      const cellNumber = parseInt(cellPrice);
      if (!isNaN(cellNumber)) {
        console.log("Число внутри ячейки:", cellNumber);
      } else {
        console.log("Содержимое внутри ячейки не является числом:", cellPrice);
      }
    }
  });
});