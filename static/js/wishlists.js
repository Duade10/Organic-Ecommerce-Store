const handleWishlistAlert = (status) => {
    let message;
    switch (status) {
        case 201:
            message = "Added to Wishlist";
            successAlert(message)
            break;
        case 204:
            message = "Removed from Wishlist";
            successAlert(message)
            break;
        case 400:
            message = "Failed to add to Wishlist";
            errorAlert(message)
            break;
        case 401:
            message = "Please Login";
            errorAlert(message)
            break;
        case 500:
            message = "Bad Request";
            errorAlert(message)
            break;

    }
}


function wishlistRequest(product_id) {
    // todo: add befored send 
    const productId = product_id
    const method = 'POST'
    const requestUrl = '/wishlists/toggle/'
    const responseType = "json"
    const data = JSON.stringify({ product_id: productId })
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie("csrftoken")
    xhr.open(method, requestUrl)
    xhr.responseType = responseType
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = function () {
        const status = xhr.status
        console.log(url)
        if (url === '/wishlists/') {
            if (status === 204) {
                console.log("removed")
                const productCol = document.getElementById(`product-${productId}`)
                productCol.classList.add("d-none")
            }
        }
        handleWishlistAlert(status)
        getCartData()
    }
    xhr.send(data)
}
