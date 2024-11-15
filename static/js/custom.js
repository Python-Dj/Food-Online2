let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    let place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    let geocoder = new google.maps.Geocoder();
    let address = document.getElementById("id_address").value;

    geocoder.geocode({'address': address}, function(results, status){
        if (status == google.maps.GeocoderStatus.OK){

            let latitude = results[0].geometry.location.lat();
            let longitude = results[0].geometry.location.lng();
            console.log(longitude)
            console.log(latitude)

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address)
        }
    })
    // loop through the address component and assign other address data
    console.log(place.address_components)
    for(let i=0; i<place.address_components.length; i++){
        for(let j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name)
            }
            //get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name)
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name)
            }
            //get pin code
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name)
            }else{
                $('#id_pin_code').val("")
            }
        }
    }
}

// Ajax Request

$(document).ready(function(){
    // Add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                console.log(food_id)
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+food_id).html(response.qty)
                cartAmountDetails(response)
            }
        })
    })

    // Remove From Cart
    $('.remove_from_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id')
        cart_id = $(this).attr('cart-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url,
            data: [],
            success: function(response){
                console.log(response)
                if (response.status == 'Login-Required'){
                    swal({
                        title: "Login Required!",
                        text: response.message,
                        icon: "warning",
                        button: "Login",
                      }).then(function(){
                        window.location='/login'
                      })
                }else if(response.status == 'Failed'){
                    swal({
                        title: "Warning!",
                        text: response.message,
                        icon: "error",
                        buttons: "ok",
                      })
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    if (window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id)
                        console.log(response.qty)
                        checkEmptyCart()
                    }
                    cartAmountDetails(response)
                }
            }
        })
    })

    // Delete Cart
    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cartID = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if (response.status == 'Success'){
                    swal({
                        title: "Success",
                        text: response.message,
                        icon: "success",
                        buttons: "ok",
                      });
                      $('#cart_counter').html(response.cart_counter['cart_count'])
                      removeCartItem(0, cartID);
                      checkEmptyCart();
                      cartAmountDetails(response)
                }
            }
        })
    })

    // delete the cart element if quantity is 0
    function removeCartItem(cartItemQty, cartID){
        if (cartItemQty <= 0){
            document.getElementById('cart-item-'+cartID).remove()
        }
    }

    function checkEmptyCart(){
        let cart_count = document.getElementById('cart_counter').innerHTML
        console.log(cart_count)
        if (cart_count == 0){
            document.getElementById('empty-cart').style.display = "block";
        }
    }

    // place the cart item quantity.
    $('.item-qty').each(function(){
        let the_id = $(this).attr('id')
        let qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // Cart Amount Details
    function cartAmountDetails(response){
        if (window.location.pathname == '/cart/'){
            $('#subtotal').html(response.cart_amount['subTotal'])
            $('#total').html(response.cart_amount['grandTotal'])
            taxes = response.cart_amount.all_taxes
            console.log(taxes)
            for(tax in taxes){
                for(amount in taxes[tax]){
                    $("#tax-"+tax).html(taxes[tax][amount])
                }
            }
        }
    }

    // Add Openig Hours for Vendor
    $('.add-hours').on('click', function(e){
        e.preventDefault()
        
        let day = document.getElementById('id_day').value
        let from_hour = document.getElementById('id_from_hour').value
        let to_hour = document.getElementById('id_to_hour').value
        let is_closed = document.getElementById('id_is_closed').checked
        let url = document.getElementById('id_add_url').value
        let csrftoken = $('input[name=csrfmiddlewaretoken]').val()
        console.log(url)

        if (is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }

        if (eval(condition)){
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    "day": day,
                    "from_hour": from_hour,
                    "to_hour": to_hour,
                    "is_closed": is_closed,
                    "csrfmiddlewaretoken": csrftoken,
                },
                success: function(response){
                    if (response.status == "success"){
                        if (response.is_closed == "closed"){
                            html = '<tr id="op-hr-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" data-url="/vendor/openingHours/remove/'+response.id+'/" class="remove_hours">Remove</a></td></tr>';
                            $(".opening_hours").append(html)
                            document.getElementById("opening_hours").reset();
                        }else{
                            html = '<tr id="op-hr-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+'&nbsp;<b>to</b>&nbsp;'+response.to_hour+'</td><td><a href="#" data-url="/vendor/openingHours/remove/'+response.id+'/" class="remove_hours">Remove</a></td></tr>';
                            $(".opening_hours").append(html)
                            document.getElementById("opening_hours").reset();
                        }
                    }else{
                        swal(response.message, "", "error")
                    }
                }
            })
        }else{
           swal("please fill all fields", "", "info")
        }
    })

    // Remove Opening Hours
    $(".opening_hours").on("click", ".remove_hours", function(e){
        e.preventDefault()
        let url= $(this).attr('data-url')
        console.log(url)

        $.ajax({
            type: "GET",
            url: url,
            success: function(response){
                if (response.status == 'success'){
                    document.getElementById("op-hr-"+response.id).remove()
                }else{
                    swal(response.message, "", "error")
                }
            }
        })
    })
})