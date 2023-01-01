function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleCartItemContainer(singleCartItem) {
    return `<tr>
        <td class="shoping__cart__item">
            <img src="${singleCartItem.product.image}" width="125" alt="${singleCartItem.product.name}">
            <h5>${singleCartItem.product.name}</h5>
        </td>
        <td class="shoping__cart__price">
            #${singleCartItem.product.price}
        </td>
        <td class="shoping__cart__quantity">
            <div class="quantity">
                <div class="pro-qty">
                <button onclick="handleCartRequest(${singleCartItem.product.id}, 'remove')" class="border-0">-</button>
                 <input type="text" id="cart-item-${singleCartItem.product.id}" onchange="handleCartRequest(${singleCartItem.product.id}, 'value')" value="${singleCartItem.quantity}">
                <button onclick="handleCartRequest(${singleCartItem.product.id}, 'add')" class="border-0">+</button>
                </div>
            </div>
        </td>
        <td class="shoping__cart__total">
            #${singleCartItem.sub_total}
        </td>
        <td class="shoping__cart__item__close">
            <span onclick="handleCartRequest(${singleCartItem.product.id}, 'delete')" class="icon_close"></span>
        </td>
    </tr>`
}


const handleCartAlert = (status, action) => {
    if (action === 'remove') {
        status = 204
    } else if (action === 'delete') {
        status = 205
    }
    let message;
    switch (status) {
        case 201:
            message = "Added to Cart";
            successAlert(message)
            break;
        case 202:
            message = "Cart Updated";
            successAlert(message)
            break;
        case 204:
            message = "Removed from Cart";
            successAlert(message)
            break;
        case 205:
            message = "Deleted";
            successAlert(message)
            break;
        case 400:
            message = "Failed to add to cart";
            errorAlert(message)
            break;
        case 500:
            message = "Bad Request";
            errorAlert(message)
            break;
        case "Empty Cart":
            message = "No item in Cart";
            errorAlert(message)
            break;
        case "loading":
            message = "Loading";
            infoAlert(message)
            break;

    }
}


function handleCartsPage(cartItem) {
    console.log("handleCartsPage")
    if (cartItem.length > 0) {
        console.log("cartItem.length > 0")
        var finalCartItem = "";
        for (var i = 0; i < cartItem.length; i++) {
            var singleCartItem = cartItem[i]
            var cartItemContainer = document.getElementById("cart-item")
            const finishedCartItem = handleCartItemContainer(singleCartItem)
            finalCartItem += finishedCartItem;
            cartItemContainer.innerHTML = finalCartItem;
        }
    } else if (cartItem.length === 0) {
        var status = "Empty Cart"
        handleCartAlert(status)
        var cartItemContainer = document.getElementById("cart-item")
        cartItemContainer.innerHTML = `<h4>No product in cart</h4>`
        console.log('cartItem.length === 0')
    }
}



function handleCartRequest(product_id, action) {
    let inputValue;
    let method = "POST"
    let csrftoken = getCookie("csrftoken")

    if (action === "value") {
        const input = document.getElementById(`cart-item-${product_id}`)
        inputValue = input.value
    }

    if (action === null) {
        console.log(action)
        method = "GET"
        csrftoken = null
    }

    const responseType = "json"
    const productId = parseInt(product_id)
    const value = inputValue

    var data = JSON.stringify({
        product_id: productId,
        action: action,
        value: value,
    })
    if (action !== null) {
        handleCartAlert("loading")
    }
    const xhr = new XMLHttpRequest()
    xhr.open(method, '/carts/')
    xhr.responseType = responseType
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    if (method === "POST") {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }

    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = xhr.response
            console.log(response)
            const status = xhr.status
            console.log(status)
            if (url === '/carts/') {
                handleCartsPage(response)
            }
            handleCartAlert(status, action)
            getCartData()

        }
    }

    if (method === 'GET') {
        xhr.send()
    } else if (method === 'POST') {
        xhr.send(data)
    }
}

if (url === '/carts/') {
    handleCartRequest(null, null)
}