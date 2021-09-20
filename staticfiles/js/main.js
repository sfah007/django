
function vr(text){
    return document.querySelector(text)
}

function vt(text){
    return document.querySelectorAll(text)
}


function cral(text){
    return document.createElement(text);
}


function crtx(text){
    return document.createTextNode(text);
}

document.body.addEventListener('click', bodyClick)

var def = null

function bodyClick(e){
    

    if (e.target.classList == 'btn btn-default dropdown-toggle'){

        btn = e.target
        if (def != null && btn != def){
            def.nextElementSibling.classList.remove('dropdown-menu-custom')
        }      

        btn.nextElementSibling.classList.toggle('dropdown-menu-custom')       
        
        def = btn
    }

    vr('.search-out').classList.add('ds-none')

    
}

vr('#label-search-navbar').onclick = function (){
    vr('#search-navbar').classList.toggle('ds-none-2')      
}


    
vr('#search-input-navbar').onkeyup = function(){
    inp = vr('#search-input-navbar');
    value = inp.value.toLowerCase()
    
    p = vt('.search-text')
    v = vr('.search-out')

    
   

    if (value.length > 1){
        v.classList.remove('ds-none')
        for(i=0; i<p.length;i++){
            if (p[i].innerHTML.toLowerCase().indexOf(value) == -1){
                p[i].classList.add('ds-none')
            }
            else{
                p[i].classList.remove('ds-none')
            }
        }
    }
    else{
        v.classList.add('ds-none')
    }
}





