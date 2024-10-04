const messages = document.querySelector('.messages')
const message = document.querySelector('.message')


function closeMessageBtn() {
    messages.classList.add('close-messages')
}

if (messages) {
    const messageWidth = message.clientWidth 
    message.style.width = `${messageWidth}px`
}