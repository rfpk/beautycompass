
$('#view_comment').pagination({
    dataSource: [
        {
            linkProfile:'#',
            avatar:'../img/image 221.png',
            nameUserComm: 'Дарья С.',
            date:'22.08.2022',
            respPost:'Какой-то пост на который был комментарий',
            commentUser:'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis ipsam labore dolor voluptate quos quas quibusdam asperiores in pariatur velit nulla illum vel, dolorem dolores dignissimos ut natus mollitia voluptatum. Rem expedita magnam ducimus odio molestias libero quas, labore laborum eligendi, numquam maiores voluptate? Illo possimus itaque consequuntur aut officia dolorum fuga quae magni, cumque ipsam. Aspernatur quidem sunt aliquid! Ducimus excepturi doloremque autem fugiat corporis praesentium? Expedita delectus nobis nesciunt, quis magnam ad. Tempora modi voluptas id eaque sequi veniam accusamus porro. Ut ratione, ipsum unde eius maiores corporis?',
            linkComm:'#',
            linkPost:'#'
        }, 
        {
            linkProfile:'#',
            avatar:'../img/image 221.png',
            nameUserComm: 'Дарья С.',
            date:'22.08.2023',
            respPost:'Какой-то пост1 на который был комментарий',
            commentUser:'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis ipsam labore dolor voluptate quos quas quibusdam asperiores in pariatur velit nulla illum vel, dolorem dolores dignissimos ut natus mollitia voluptatum. Rem expedita magnam ducimus odio molestias libero quas, labore laborum eligendi, numquam maiores voluptate? Illo possimus itaque consequuntur aut officia dolorum fuga quae magni, cumque ipsam. Aspernatur quidem sunt aliquid! Ducimus excepturi doloremque autem fugiat corporis praesentium? Expedita delectus nobis nesciunt, quis magnam ad. Tempora modi voluptas id eaque sequi veniam accusamus porro. Ut ratione, ipsum unde eius maiores corporis?',
            linkComm:'#',
            linkPost:'#'
        }, 
        {
            linkProfile:'#',
            avatar:'../img/image 221.png',
            nameUserComm: 'Дарья С.',
            date:'21.08.2022',
            respPost:'Какой-то пост2 на который был комментарий',
            commentUser:'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis ipsam labore dolor voluptate quos quas quibusdam asperiores in pariatur velit nulla illum vel, dolorem dolores dignissimos ut natus mollitia voluptatum. Rem expedita magnam ducimus odio molestias libero quas, labore laborum eligendi, numquam maiores voluptate? Illo possimus itaque consequuntur aut officia dolorum fuga quae magni, cumque ipsam. Aspernatur quidem sunt aliquid! Ducimus excepturi doloremque autem fugiat corporis praesentium? Expedita delectus nobis nesciunt, quis magnam ad. Tempora modi voluptas id eaque sequi veniam accusamus porro. Ut ratione, ipsum unde eius maiores corporis?',
            linkComm:'#',
            linkPost:'#'
        }, 
        {
            linkProfile:'#',
            avatar:'../img/image 221.png',
            nameUserComm: 'Дарья С.',
            date:'29.08.2022',
            respPost:'Какой-то пост3 на который был комментарий',
            commentUser:'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis ipsam labore dolor voluptate quos quas quibusdam asperiores in pariatur velit nulla illum vel, dolorem dolores dignissimos ut natus mollitia voluptatum. Rem expedita magnam ducimus odio molestias libero quas, labore laborum eligendi, numquam maiores voluptate? Illo possimus itaque consequuntur aut officia dolorum fuga quae magni, cumque ipsam. Aspernatur quidem sunt aliquid! Ducimus excepturi doloremque autem fugiat corporis praesentium? Expedita delectus nobis nesciunt, quis magnam ad. Tempora modi voluptas id eaque sequi veniam accusamus porro. Ut ratione, ipsum unde eius maiores corporis?',
            linkComm:'#',
            linkPost:'#'
        },
    ],
    pageSize: 10,
    pageNumber: 1,
    pageRange: 0,
    callback: function(data, pagination) {
        var html = templatingItem(data);
        $('#view_comment').prev().html(html);
    }
});


function templatingItem(data) {
    html = '<ul>';
    data.forEach(element => {
        html+='<a href="'+element.linkPost+'" class="mb-2 text--15-24 dark-lighter">'
        html+=element.respPost
        html+='</a>'
        html+='<a class="navbar-brand col-11 col-xxl-4 d-none d-xl-block" href="#"><img src="../img/logo-blue.svg" alt=""></a>'
        html+='<div class="feed__row mt-3">'
        html+='<div class="feed__user align-items-center">'
        html+='<a href="'+element.linkProfile+'" class="feed__avatar">'
        html+='<img src="'+element.avatar+'" alt="avatar">'
        html+='</a>'
        html+='<div class="feed__info">'
        html+='<a href="'+element.linkProfile+'" class="feed__name">'+element.nameUserComm+'</a>'
        html+='<div class="d-flex align-items-center gap-2">'
        html+='<div class="feed__date">'+element.date+'</div>'
        html+='</div></div></div>'
        html+='<div class="feed__text d-flex flex-column align-items-start gap-1 gap-lg-2 dark-semi mt-2 mb-3">'
        html+='<span class="feed__text feed__text--preview">'+element.commentUser+'</span>'
        html+='</div>'
        html+='<div class="feed__actions justify-content-between">'
        html+='<button type="button" class="feed__action social-count__icon social-count__icon--small social-count__icon--like" onclick="onLike(this)">'
        html+='    <svg xmlns="http://www.w3.org/2000/svg" width="18px" height="19px" viewBox="0 0 22.2825 21.6998">'
        html+='        <path fill="#1560BD" d="M15.736 21.6998l-4.08184 0c-0.601234,0 -1.91179,-0.182397 -2.60994,-0.880805l-2.29113 -1.76914c-0.392855,0.984735 -1.29445,1.46905 -2.72504,1.46905l-1.07411 0c-1.9874,0 -2.95394,-0.934589 -2.95394,-2.84664l0 -10.5263c0,-1.91205 0.966547,-2.84638 2.95394,-2.84638l1.07411 0c1.52595,0 2.44988,0.551347 2.79675,1.67301l3.19688 -4.75635c0.676843,-1.00968 2.15888,-1.49321 3.31874,-1.05281 1.34277,0.440402 2.20201,1.9227 1.9014,3.29769l-0.526404 3.38369c-0.0106528,0.0750893 -0.0106528,0.182397 0.0644365,0.268399 0.0537837,0.0537837 0.128873,0.0860019 0.214875,0.0860019l4.29672 0c1.05255,0 1.96557,0.440402 2.50263,1.20299 0.526404,0.741019 0.633712,1.71874 0.289964,2.66398l-2.56707 7.81942c-0.397531,1.55739 -2.05183,2.81416 -3.78097,2.81416zm-8.75427 -4.51445l3.12595 2.42c0.268399,0.257746 0.945241,0.472621 1.54648,0.472621l4.08184 0c0.966547,0 2.00844,-0.773497 2.22332,-1.64339l2.59954 -7.89477c0.171744,-0.472621 0.139526,-0.90237 -0.0860019,-1.2139 -0.23618,-0.332835 -0.66593,-0.526145 -1.19233,-0.526145l-4.29646 0c-0.558623,0 -1.07437,-0.23644 -1.42877,-0.644624 -0.365053,-0.418837 -0.526145,-0.97746 -0.440402,-1.55739l0.537057 -3.44813c0.129133,-0.601494 -0.279051,-1.27808 -0.859239,-1.47139 -0.526404,-0.193569 -1.20299,0.0857421 -1.43943,0.42949l-4.37155 6.50471 0 8.57291zm-4.0278 -11.2746c-1.17103,0 -1.34277,0.279311 -1.34277,1.23521l0 10.5263c0,0.956154 0.171744,1.23547 1.34277,1.23547l1.07411 0c1.17077,0 1.34251,-0.279311 1.34251,-1.23547l0 -10.5263c0,-0.955894 -0.171744,-1.23521 -1.34251,-1.23521l-1.07411 0z"></path>'
        html+='        <path class="icon-inner" fill="none" d="M2.77908 5.68106c-1.31289,0 -1.50542,0.289185 -1.50542,1.2786l0 10.8963c0,0.989671 0.19253,1.27886 1.50542,1.27886l1.20455 0c1.31263,0 1.50516,-0.289185 1.50516,-1.27886l0 -10.8963c0,-0.989412 -0.19253,-1.2786 -1.50516,-1.2786l-1.20455 0z"></path>'
        html+='        <path class="icon-inner" fill="none" d="M6.98174 17.1853l3.23378 2.56083c0.270477,0.261124 0.953036,0.479116 1.55921,0.479116l4.11536 -0.000259824c0.974342,0.000259824 2.02481,-0.78415 2.24177,-1.66625l2.62085 -8.00623c0.173043,-0.479376 0.140825,-0.915102 -0.0865215,-1.23105 -0.238259,-0.337252 -0.671646,-0.533679 -1.20221,-0.533679l-4.33205 0c-0.563299,0 -1.08321,-0.239818 -1.44047,-0.653718 -0.368171,-0.424553 -0.530302,-0.99123 -0.44404,-1.57921l0.541474 -3.49698c0.130172,-0.609808 -0.28139,-1.296 -0.866255,-1.49217 -0.530821,-0.196167 -1.29964,0.151737 -1.53816,0.500162l-3.5188 5.23053 -0.883923 1.31601c0,2.08379 0,3.2899 0,1.50724l0 4.21903c0,0.782591 0,1.33758 0,2.84664z"></path>'
        html+='    </svg> '
        html+='    <span class="dark-semi">15</span>'
        html+='</button>'
        html+='<a href="'+element.linkComm+'" class="main-color text--15-20">Перейти к комментарию</a>'
        html+='</div>'
        html+='<a href="#" class="feed__mark" type="button" data-bs-toggle="modal" data-bs-target="#modal-petition">'
        html+='<svg width="39" height="38" viewBox="0 0 39 38" fill="none" xmlns="http://www.w3.org/2000/svg">'
        html+='    <path d="M19.4886 23.5222C18.8478 23.5222 18.3164 22.9914 18.3164 22.3512V14.5441C18.3164 13.9039 18.8478 13.373 19.4886 13.373C20.1293 13.373 20.6607 13.9039 20.6607 14.5441V22.3512C20.6607 22.9914 20.1293 23.5222 19.4886 23.5222Z" fill="#E31E24"></path>'
        html+='    <path d="M19.4886 28.5974C19.3949 28.5974 19.2855 28.5818 19.1761 28.5662C19.0823 28.5506 18.9885 28.5194 18.8948 28.4725C18.801 28.4413 18.7072 28.3945 18.6134 28.332C18.5353 28.2695 18.4572 28.2071 18.379 28.1446C18.0977 27.848 17.9258 27.442 17.9258 27.036C17.9258 26.6301 18.0977 26.2241 18.379 25.9274C18.4572 25.865 18.5353 25.8025 18.6134 25.74C18.7072 25.6776 18.801 25.6307 18.8948 25.5995C18.9885 25.5527 19.0823 25.5214 19.1761 25.5058C19.3792 25.459 19.598 25.459 19.7856 25.5058C19.895 25.5214 19.9888 25.5527 20.0825 25.5995C20.1763 25.6307 20.2701 25.6776 20.3638 25.74C20.442 25.8025 20.5201 25.865 20.5983 25.9274C20.8796 26.2241 21.0515 26.6301 21.0515 27.036C21.0515 27.442 20.8796 27.848 20.5983 28.1446C20.5201 28.2071 20.442 28.2695 20.3638 28.332C20.2701 28.3945 20.1763 28.4413 20.0825 28.4725C19.9888 28.5194 19.895 28.5506 19.7856 28.5662C19.6918 28.5818 19.5824 28.5974 19.4886 28.5974Z" fill="#E31E24"></path>'
        html+='    <path d="M28.9613 35.0932H10.0194C6.97181 35.0932 4.64315 33.9846 3.45537 31.986C2.28323 29.9874 2.43951 27.411 3.92423 24.741L13.3952 7.72158C14.958 4.91104 17.1148 3.36523 19.4903 3.36523C21.8659 3.36523 24.0226 4.91104 25.5855 7.72158L35.0565 24.7566C36.5412 27.4266 36.7131 29.9874 35.5253 32.0016C34.3375 33.9846 32.0089 35.0932 28.9613 35.0932ZM19.4903 5.70736C18.0213 5.70736 16.5834 6.83158 15.4425 8.86142L5.98721 25.8965C4.92446 27.8014 4.75255 29.5502 5.48709 30.8149C6.22164 32.0797 7.84702 32.7667 10.035 32.7667H28.9769C31.1649 32.7667 32.7747 32.0797 33.5249 30.8149C34.275 29.5502 34.0875 27.817 33.0247 25.8965L23.5382 8.86142C22.3973 6.83158 20.9594 5.70736 19.4903 5.70736Z" fill="#E31E24"></path>'
        html+='</svg>'
        html+='</a>'

        html+='</div>'
    });

    html += '</ul>';


    
    return html;
}

function onLike(element) {
    if(element.children[0].children[0].attributes.fill.nodeValue=="#1560BD"){
        element.children[1].innerText=Number(element.children[1].innerText)+1
    }
    else{
        element.children[1].innerText=Number(element.children[1].innerText)-1
    }
    for (let index = 0; index < element.children[0].children.length; index++) {
        const path = element.children[0].children[index];
        if(path.attributes.fill.nodeValue=="#1560BD"){
            path.attributes.fill.nodeValue='none'
        }else if(path.attributes.fill.nodeValue=='none'){
            path.attributes.fill.nodeValue="#1560BD"
        }
    }
}
