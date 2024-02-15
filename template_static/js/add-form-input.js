const addInputBtn = document.querySelectorAll('.js-add-form-input')

addInputBtn.forEach( btn => {

    btn.addEventListener('click', function(){
        const inputName = this.parentElement.getAttribute('data-input')
        createInput(this.parentElement, this, inputName)
    })

})

const createInput = (parent, createBtn, data) => {

    const newInput = document.createElement("div");
    newInput.classList.add("input", "input--general");

    newInput.innerHTML = `
    <input class="input--regular" name="${data}" value="" type="${data}" required/>
  `;

  parent.insertBefore(newInput, createBtn);

}