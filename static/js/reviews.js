function handleReviewForm(event) {
    console.log("Submitted")
    console.log(event.outerHTML)
    event.preventDefault()
    const csrftoken = getCookie("csrftoken")
    const responseType = "json"
    const reviewForm = event.target
    const reviewFormData = new FormData(reviewForm)
    const url = reviewForm.getAttribute("action")
    const method = reviewForm.getAttribute("method")
    infoAlert("Loading")
    const xhr = new XMLHttpRequest()
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const status = xhr.status
            console.log(xhr.response)
            if (status === 201) {
                const message = "Review Submitted Successfully"
                successAlert(message)
                reviewForm.reset()
            }
        }
    }
    xhr.send(reviewFormData)
}

const reviewFormCreateEl = document.getElementById("review-form")
console.log(reviewFormCreateEl)
reviewFormCreateEl.addEventListener("submit", handleReviewForm)