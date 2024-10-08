
// Messages from backend: success, error, warning, info, and etc.
const messages = document.querySelector('.messages')
const message = document.querySelector('.message')


function closeMessageBtn() {
    messages.classList.add('close-messages')
}

if (messages) {
    const messageWidth = message.clientWidth 
    message.style.width = `${messageWidth}px`
}


// Toggle mobile navlinks
const mobileNavlinks = document.querySelector('.mobile-navlinks')
const toggleBtnsContainer = document.querySelector('.mobile-navlinks-toggle-btns-container')
const toggleBtns = toggleBtnsContainer && 
                Array.from(toggleBtnsContainer.querySelectorAll('button'))

const mobileOpenBtn = document.querySelector('.mobile-navlinks-open-btn')
const mobileCloseBtn = document.querySelector('.mobile-navlinks-close-btn')

toggleBtns && toggleBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        mobileNavlinks.classList.toggle('show-mobile-navlinks')

        if (btn === mobileOpenBtn) {
            mobileOpenBtn.classList.add('hide-mobile-navlinks-toggle-btn')
            mobileCloseBtn.classList.remove('hide-mobile-navlinks-toggle-btn')
        }
        else if(btn === mobileCloseBtn) {
            mobileOpenBtn.classList.remove('hide-mobile-navlinks-toggle-btn')
            mobileCloseBtn.classList.add('hide-mobile-navlinks-toggle-btn')
        }
    })
})

