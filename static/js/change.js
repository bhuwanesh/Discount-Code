let subcategory_select = document.getElementById('subcategory');
let product_select = document.getElementById('product');

subcategory_select.onchange = function(){
    subcategory = subcategory_select.value;

    fetch('/product/' + subcategory).then(function(response){
        response.json().then(function(data){
            let optionHTML='';
            for(let product of data.products){
                optionHTML+='<option value="' + product.id + '">' + product.name +'</option>';
            }

            product_select.innerHTML = optionHTML;

        });
    });
}