const handleHamburgerHeader = (response) => {
    const cartItemsCount = response.cart_items_count
    const wishlistCount = response.wishlist_count
    const grandTotal = response.grand_total
    const cartContainer = document.getElementById("hamburger-menu-cart")
    const grandTotalContainer = document.getElementById("hamburger-menu-grand-total")
    const wishlistContainer = document.getElementById("hamburger-menu-wishlist")
    cartContainer.textContent = cartItemsCount
    grandTotalContainer.textContent = grandTotal
    wishlistContainer.textContent = wishlistCount
}

const handleMainHeader = (response) => {
    const cartItemsCount = response.cart_items_count
    const wishlistCount = response.wishlist_count
    const grandTotal = response.grand_total
    const cartContainer = document.getElementById("main-header-cart")
    const grandTotalContainer = document.getElementById("main-header-grand-total")
    const wishlistContainer = document.getElementById("main-header-wishlist")
    cartContainer.textContent = cartItemsCount
    grandTotalContainer.textContent = grandTotal
    wishlistContainer.textContent = wishlistCount
}

const handleCartCheckout = (response) => {
    console.log(response.tax)
    const tax = response.tax
    const totalPrice = response.sub_total
    const grandTotal = response.grand_total
    const taxContainer = document.getElementById("tax")
    const totalPriceContainer = document.getElementById("total-price")
    const grandTotalContainer = document.getElementById("total")
    taxContainer.textContent = tax
    totalPriceContainer.textContent = totalPrice
    grandTotalContainer.textContent = grandTotal
}


const getCartData = () => {
    const method = "GET"
    const xhr = new XMLHttpRequest()
    const responseType = "json"
    const request_url = '/api/carts/carts-data/'
    xhr.open(method, request_url, true)
    xhr.responseType = responseType
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = () => {
        const response = xhr.response
        handleHamburgerHeader(response)
        handleMainHeader(response)
        if (url.includes('/carts/')) {
            handleCartCheckout(response)
        }
    }
    xhr.send()
}
getCartData()




setTimeout(function () {
    document.getElementsByClassName('alert').fadeOut('slow')
}, 3000)
