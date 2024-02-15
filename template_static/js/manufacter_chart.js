function templatingItem(data) {
    let html=''

    html = '<ul>';
    data.forEach(element => {

        html+='<li class="output__statistic-wrap">'
        html+='<div class="container container--bc">'
        html+='    <div class="col-xxl-10 offset-xxl-1">'
        html+='        <div class="item item__inside">'
        html+='            <div class="item__image-view">'
        html+='                <img src="../img/'+element.image+'" alt="'+element.mainTitle+'">'
        html+='            </div>'
        html+='            <div class="item__title">'
        html+='                <p class="text--15-30">'
        html+=element.mainTitle
        html+='                </p>'
        html+='                <p class="text--15-24">'
        html+=element.subTitle
        html+='                </p>'
        html+='            </div>'
        html+='            <div class="item__rating-value rating__body">'
        
        //высчитывание рейтинга

        html+='                <div class="rating__active" style="width: '+element.rating+'%;"></div>'

        html+='            </div>'
        html+='            <div class="item__statistic-number d-flex align-items-center">'
        html+='                <div class="item__statistic-number__element">'
        html+='                    <img src="../img/favorite-heart.svg" alt="Добавленией в избранное">'
        html+='                    <span>'+element.like+'</span>'
        html+='                </div>'
        html+='                <div class="item__statistic-number__element">'
        html+='                    <img src="../img/like-tag.svg" alt="Поставили нравиться">'
        html+='                    <span>'+element.positRevi+'</span>'
        html+='                </div>'
        html+='                <div class="item__statistic-number__element">'
        html+='                    <img src="../img/message-question.svg" alt="Заданные вопросы">'
        html+='                    <span>'+element.question+'</span>'
        html+='                </div>'
        html+='                <div class="item__statistic-number__element">'
        html+='                    <img src="../img/grey_eye.svg" alt="Показатель просмотров">'
        html+='                    <span>'+element.views+'</span>'
        html+='                </div>'
        html+='            </div>'
        html+='            <div class="item__btn">'

        // вывод всех магазинов где расположен товар
        element.linkShop.forEach(shop => {
            
            html+='                <a href="'+shop.link+'" class="btn">'
            html+='                    <p class="text--12-18">'
            html+=shop.name
            html+='                    </p>'
            html+='                </a>'
        });

        html+='            </div>'
        html+='        </div>'
        html+='    </div>'
        html+='</div>'
        html+='    <div class="item__chart">'
        html+='<div class="container container--bc">'
        html+='    <div class="col-xxl-10 offset-xxl-1">'
        html+='        <div class="open_chart">'
        html+='            <p class="text--15-30" >График</p>'
        html+='            <input type="hidden" name="id_item" value="'+element.id+'">'
        html+='        </div>'
        html+='        <div class="chart output_chart_id_item">'
        html+='            <input type="hidden" name="openTrig" value=false>'
        html+='        </div>'
        html+='    </div>'
        html+='        </div>'
        html+='    </div>'
        html+='</li>'
    });
    html += '</ul>';
    
    return html;
}

function fetchJSONFile(path, callback) {
    //path ссыллка на ресурс получения
    //callback что делать с полученными данными
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                var data = JSON.parse(httpRequest.responseText);
                if (callback) callback(data);
            }
        }
    };
    httpRequest.open('GET', path);
    httpRequest.send(); 
}

var countAtrrClick={
    rating:false,
    view:false,
    visit:false,
    favarite:false,
    new:false,
}

Chart.defaults.borderColor = '#fff';
Chart.defaults.color = '#fff';

function viewsItems(linkToBD, sort='') {

    var answerJson=[]
    
    fetchJSONFile(linkToBD, function(data){
    
        if (sort!='') {
            switch (sort) {
                case 'rating':
                    (countAtrrClick.rating ) ? answerJson=data.cosmetics.sort((x,y)=>x.rating-y.rating) : answerJson=data.cosmetics.sort((x,y)=>y.rating-x.rating)
                    countAtrrClick.rating=!countAtrrClick.rating

                    break;
                case 'view':
                    (countAtrrClick.view ) ? answerJson=data.cosmetics.sort((x,y)=>x.views-y.views) : answerJson=data.cosmetics.sort((x,y)=>y.views-x.views)
                    countAtrrClick.view=!countAtrrClick.view

                    break;
                case 'visit':
                    (countAtrrClick.visit ) ? answerJson=data.cosmetics.sort((x,y)=>x.visitAll-y.visitAll) : answerJson=data.cosmetics.sort((x,y)=>y.visitAll-x.visitAll)
                    countAtrrClick.visit=!countAtrrClick.visit

                    break;
                case 'favarite':
                    (countAtrrClick.favarite ) ? answerJson=data.cosmetics.sort((x,y)=>x.like-y.like) : answerJson=data.cosmetics.sort((x,y)=>y.like-x.like)
                    countAtrrClick.favarite=!countAtrrClick.favarite

                    break;
                case 'new':
                    (countAtrrClick.new ) ? answerJson=data.cosmetics.sort((x,y)=>new Date(x.dateCreate)-new Date(y.dateCreate)) : answerJson=data.cosmetics.sort((x,y)=>new Date(y.dateCreate)-new Date(x.dateCreate))
                    countAtrrClick.new=!countAtrrClick.new

                    break;
            }
        }else answerJson=data.cosmetics
    
        if($('#viewCosmeticChart').length){
            $('#viewCosmeticChart').pagination({
                dataSource:answerJson,
                pageSize: 5,
                pageNumber: 1,
                pageRange: 1,
                formatGoInput: 'go to <%= input %> st/rd/th',
                callback: function(item, pagination) {
                    var html = templatingItem(item);
                    $('#viewCosmeticChart').prev().html(html);
                    
                    $(".open_chart").click(function (elem) { 

                        $(elem.currentTarget.parentElement.parentElement.parentElement).toggleClass("item__chart-open");

                        $(elem.currentTarget.nextElementSibling).toggleClass("chart-open")


                        let idElem=elem.currentTarget.children[1].value

                        let charts = item[idElem].chart
                        
                        let canvas = document.createElement('canvas')

                        var ctx = canvas.getContext('2d')

                        const gradient = ctx.createLinearGradient(20, 0, 220, 0);

                        // Add three color stops
                        gradient.addColorStop(0, "green");
                        gradient.addColorStop(0.5, "cyan");
                        gradient.addColorStop(1, "green");


                        let dataOutpChart={
                            labels:charts[0].data.map(el=>el.x),
                            datasets:[
                                {
                                    label: 'Просмотры',
                                    data: charts[0].data.map(el=>el.y),
                                },
                                {
                                    label: 'Отзывы',
                                    data: charts[1].data.map(el=>el.y),
                                },
                                {
                                    label: 'Избранное',
                                    data: charts[2].data.map(el=>el.y),
                                },
                                {
                                    label: 'Переходы на маркетплейсы',
                                    data: charts[3].data.map(el=>el.y),
                                },
                                {
                                    label: 'Переходы на страницу бренда',
                                    data: charts[4].data.map(el=>el.y),
                                },
                            ]
                        }

                        if (elem.currentTarget.nextElementSibling.firstElementChild.value=="false") {
                            elem.currentTarget.nextElementSibling.append(canvas);
                            const chart=new Chart(canvas,{
                                type:'line',
                                data:dataOutpChart,
                                borderColor: '#fff',
                                color:'#fff'
                            })

                            elem.currentTarget.nextElementSibling.firstElementChild.value=true
                        } else {
                            $(elem.currentTarget.nextElementSibling.children[1]).remove();
                            elem.currentTarget.nextElementSibling.firstElementChild.value=false
                        }
                    });
                }
            })
        }
    });
}

$('#rating').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json",'rating')

})
$('#view').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json",'view')

})
$('#visit').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json",'visit')

})
$('#favarite').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json",'favarite')

})
$('#new').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json",'new')

})
$('#default').click(function(el) {
    el.preventDefault();
    viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json")

})

viewsItems("../manufacturer-lk__charts/all_cosmetics_manufacter.json")