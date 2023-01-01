function afterRequestContact(status) {
    if (status === 201) {
        const message = "Message Submitted Successfully"
        successAlert(message)
    } else if (status === 401) {
        const message = "Couldn't submit review"
        successAlert(message)
    }
}


function handleContactForm(event) {
    event.preventDefault()
    const csrftoken = getCookie("csrftoken")
    const contactForm = event.target
    const contactFormData = new FormData(contactForm)
    const url = contactForm.getAttribute("action")
    const method = contactForm.getAttribute("method")
    const xhr = new XMLHttpRequest()
    const responseType = "json"
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = () => {
        const status = xhr.status
        afterRequestContact(status)
        contactForm.reset()
    }
    xhr.send(contactFormData)
}


const contactFormCreateEl = document.getElementById("contact-form")
console.log(contactFormCreateEl)
contactFormCreateEl.addEventListener("submit", handleContactForm)