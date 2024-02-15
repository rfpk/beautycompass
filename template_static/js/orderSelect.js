$(document).ready(function() {
    $('.choseSave .selectWrap').css('display','none')

    if($(window).width()>=768) $('.choseSave').css('justify-content','start')
    else $('.choseSave').css('justify-content','end')


    $(window).resize(function() {
        if($(window).width()>=768) $('.choseSave').css('justify-content','start')
        else $('.choseSave').css('justify-content','end')
    });

    $('#activeIgnore').select2({
        closeOnSelect: false,
        placeholder:"Выберите из списка",
    }
    );
    $('#selectCountry').select2({
        closeOnSelect: false,
        placeholder:"Выберите из списка",
    }
    );
    
    $('#skinProp').select2({
        closeOnSelect: false,
        placeholder:"Выберите из списка" 
    }
    );
    $('#price').select2({
        closeOnSelect: false,
        placeholder:"Выберите из списка" 
    }
    );
    $('#category').select2(
        {
            closeOnSelect: false,
            placeholder:"Выберите из списка" 
        }
    )

    $('#selectProgram').on('click',function(event){
        event.preventDefault();
        
        location.replace("programm.html");
        
    });

    $('#yes').on('click', function(){
        if(this.checked){
            $('.choseSave .selectWrap').css('display','block')
            $('.choseSave').css('justify-content','space-between')
            $('.selectWrapchoseSave').css('display','block')
            $('.selectSave').css('display', 'none')
        }
    })
    $('#no').on('click', function(){
        if(this.checked){
            $('.choseSave .selectWrap').css('display','none')
            $('.selectWrapchoseSave').css('display','none')
            if($(window).width()>=768) $('.choseSave').css('justify-content','start')
            else $('.choseSave').css('justify-content','end')
            $('.selectSave').css('display', 'block')
        }
    })

    $('#simple').on('click', ()=>{
        $('#hard')[0].checked=false
    })
    $('#hard').on('click', ()=>{
        $('#simple')[0].checked=false
    })
    
    $('select2-results__option').on('click', ()=>{
        $('select2-search').css('display','none')
    }) 
})
