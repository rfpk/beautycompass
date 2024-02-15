function handleFileSelected(event) {
    console.log('handleFileSelected')
    const file = event.target.files[0];
    if (file) {
        // Обработка загруженного файла
        let reader = new FileReader();
        reader.readAsDataURL(file);
         // Banner Images
        reader.onload = function() {
            const elem = event.srcElement.parentElement.querySelector('img');
            $(elem).attr('src', reader.result); 
        }
    }
}

