
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


// Navbar logout button
const logoutModalContainer = document.querySelector('.logout-modal-container')
const logoutBtn = document.querySelector('.logout-btn')
const mobileLogoutBtn = document.querySelector('.mobile-logout-btn')

logoutBtn && logoutBtn.addEventListener('click', () => {
    logoutModalContainer.classList.toggle('show-logout-modal')
})

mobileLogoutBtn && mobileLogoutBtn.addEventListener('click', () => {
    logoutModalContainer.classList.toggle('show-logout-modal')

    // close mobile navlinks
    mobileNavlinks.classList.toggle('show-mobile-navlinks')
    mobileOpenBtn.classList.remove('hide-mobile-navlinks-toggle-btn')
    mobileCloseBtn.classList.add('hide-mobile-navlinks-toggle-btn')
})


// close logout modal 
const logoutModalCloseBtn = document.querySelector('.logout-modal-close-btn')

logoutModalCloseBtn && logoutModalCloseBtn.addEventListener('click', () => {
    logoutModalContainer.classList.toggle('show-logout-modal')
})


// Contact form on contact page
const contactForm = Array.from(document.querySelectorAll('.contact-form > p'))
                    
contactForm.forEach((p)=> {
    p.setAttribute('class', 'contact-form-row')
})

// Landing page Mobile navbar: toggle mobile navlinks
const mobileNavLinksToggleBtnsContainer = document.querySelector('.landing-page-mobile-navlinks-toggle-btns-container')
const navLinksToggleBtns = mobileNavLinksToggleBtnsContainer && 
                            Array.from(mobileNavLinksToggleBtnsContainer.querySelectorAll('button'))
const mobileNavLinks = document.querySelector('.landing-page-mobile-navlinks')
const openBtn = document.querySelector('.landing-page-mobile-navlinks-open-btn')
const closeBtn = document.querySelector('.landing-page-mobile-navlinks-close-btn')

navLinksToggleBtns && navLinksToggleBtns.forEach((btn) => {
    btn.addEventListener('click', (e)=> {
        mobileNavLinks.classList.toggle('landing-page-show-mobile-navlinks')

        if (e.currentTarget === openBtn) {
            e.currentTarget.classList.add('landing-page-hide-mobile-navlinks-toggle-btn')
            closeBtn.classList.remove('landing-page-hide-mobile-navlinks-toggle-btn')
        }
        else if (e.currentTarget === closeBtn) {
            e.currentTarget.classList.add('landing-page-hide-mobile-navlinks-toggle-btn')
            openBtn.classList.remove('landing-page-hide-mobile-navlinks-toggle-btn')
        }
    })
})