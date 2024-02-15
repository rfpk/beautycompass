function handleFileSelected(input) {

    let file = input.files[0]

    let reader = new FileReader()
    reader.readAsDataURL(file)
    
    reader.onload = function () {
        let wrapper = document.createElement('div')

        wrapper.addEventListener('click', function() {
            input.value = ""
            this.remove()
        })

        wrapper.classList.add("preload-wrap");
        let img = document.createElement('img')
        img.src = reader.result  
        img.classList.add("preload-img");
        img.style.width = '100%';
        img.style.height = '100%';

        wrapper.appendChild(img)

        input.insertAdjacentElement("afterend", wrapper)
    }
}