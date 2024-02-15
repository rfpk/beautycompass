$(document).ready(function() {

    jQuery.makeArray( $('.notice')).forEach(element => {
        if(Math.floor(Math.random() * 2)){
            $(element).css('display', 'block')
        }
    }) 

    // $('#techChat').on('click',function(){
    //     location.replace('chat-tech.html');
    // })

    // $('#chat').on('click',function(){
    //     location.replace('chat-persons.html');
    // })

    // $('.comment').on('click',function(){
    //     location.replace('comments.html');
    // })

    $('#form__pic').on("change", null, $('#form__pic'), handleFileSelected)
    
    $('#visPassword').on('click',function(){
        event.preventDefault()
        if($('.passw__inp')[0].type=='password'){
            $('#visPassword').css('background-image','url("/static/img/eye_hide.svg")');
            $('.passw__inp')[0].type='text'
        }
        else{
            $('.passw__inp')[0].type='password'
            $('#visPassword').css('background-image','url("/static/img/eye_show.svg")');
        } 
    })

    $('#visPasswordRep').on('click',function(){
        event.preventDefault()
        if($('.passw__inp__rep')[0].type=='password'){
            $('#visPasswordRep').css('background-image','url("/static/img/eye_hide.svg")');
            $('.passw__inp__rep')[0].type='text'
        }
        else{
            $('#visPasswordRep').css('background-image','url("/static/img/eye_show.svg")');
            $('.passw__inp__rep')[0].type='password'
        } 
    })

    $('#changeProfile').on('click', function(){
        $('#profile__confidInf').css('display','grid')
        $('#changeProfile').css('display','none')
        $('.redPrfile').css('display', 'block')
        $('.visPrfile').css('display', 'none')
        $('#ava').css('display', 'block')
        $('#ava').css('width', '90%')
        $('#avatar').css('width','100%')
        $('#avatar').css('border-radius','20%')
        if(window.innerWidth<1440)        $('#save').css('display','block')
        else        $('#saveProfile').css('display','flex')
    })

    $('#save').on('click', function(){
        $('#profile__confidInf').css('display','flex')
        $('#changeProfile').css('display','flex')
        $('.redPrfile').css('display', 'none')
        $('.visPrfile').css('display', 'block')
        $('#ava').css('display', 'block')
        if (window.innerWidth<=768) {
            $('#ava').css('width', '50%')
        }else
        $('#ava').css('width', '30%')
        $('#avatar').css('width','50%')
        $('#avatar').css('border-radius','50%')

        $('#save').css('display','none')
    })

    $('#saveProfile').on('click', function(){
        $('#profile__confidInf').css('display','flex')
        $('#changeProfile').css('display','flex')
        $('.redPrfile').css('display', 'none')
        $('.visPrfile').css('display', 'block')
        $('#ava').css('display', 'block')
        if (window.innerWidth<=768) {
            $('#ava').css('width', '50%')
        }else

        $('#ava').css('width', '30%')

        $('#avatar').css('width','50%')
        $('#avatar').css('border-radius','50%')

        $('#saveProfile').css('display','none')
    })
})

function handleFileSelected(input) {
    let file = input.data[0].files[0]
    if(file){
        let reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = function () {
        $('#avatar').css('background-image', 'url('+reader.result+')'  )
        $('#avatar').css('background-size', '100%' )
        }
    }
    
}
