
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


// Mobile navbar: toggle mobile navlinks
const mobileNavLinksToggleBtnsContainer = document.querySelector('.mobile-navlinks-toggle-btns-container')
const navLinksToggleBtns = [...mobileNavLinksToggleBtnsContainer.querySelectorAll('button')]
const mobileNavLinks = document.querySelector('.mobile-navlinks')

const openBtn = document.querySelector('.mobile-navlinks-open-btn')
const closeBtn = document.querySelector('.mobile-navlinks-close-btn')

navLinksToggleBtns.forEach((btn) => {
    btn.addEventListener('click', (e)=> {
        mobileNavLinks.classList.toggle('show-mobile-navlinks')

        if (e.currentTarget === openBtn) {
            e.currentTarget.classList.add('hide-mobile-navlinks-toggle-btn')
            closeBtn.classList.remove('hide-mobile-navlinks-toggle-btn')
        }
        else if (e.currentTarget === closeBtn) {
            e.currentTarget.classList.add('hide-mobile-navlinks-toggle-btn')
            openBtn.classList.remove('hide-mobile-navlinks-toggle-btn')
        }
    })
})