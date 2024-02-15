//test 3-5 quest
var form=document.forms[1];
var outPut = document.getElementById('anserText');
let listInpu=document.querySelectorAll("div.radioInp.respOpt.skinType input");

listInpu.forEach(element => {
    element.addEventListener('click', function(){
        let formData = new FormData(form);

        outPut.innerText=    typeSens(formData.get("skinSens"), formData.get("pore"), formData.get("poreInflam"))
            
    })
});

function typeSens(water, pore, flam){

    let dry = 0;
    let normal = 0;
    let combined = 0;
    let fat = 0;

    if(water!=undefined && pore!=undefined && flam!=undefined){
        let array = [water, pore, flam];

        array.forEach(element => {
            if(element == 1 ){
                dry++
            }else if(element == 2 ){
                normal++
            }else if(element == 3 ){
                combined++
            }else if(element == 4 ){
                fat++
            }
        });
        
        if(dry>normal && dry>combined && dry>fat){
            return "сухая"
        }else if(normal>dry && normal>combined && normal>fat){
            return "нормальная"
        }else if(combined>dry && combined>normal && combined>fat){
            return "комбинированная"
        }else if(fat>dry && fat>normal && fat>combined){
            return "жирная"
        }else{
            return "комбинированная"
        }
    }  
    else return "комбинированная"
}
