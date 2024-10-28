const navbarRow = document.querySelector('.nav-row')

// Messages from backend: success, error, warning, info, and etc.
const messages = document.querySelector('.messages')
const messageCloseBtn = document.querySelector('.message-close-btn')

if (messages) {

    if (!navbarRow) {
        messages.style.top = '10px'
    }
    
    function closeMessageBtn() {
        messages.classList.add('close-messages')
    }
    
    messageCloseBtn.addEventListener('click',closeMessageBtn)
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

// Nabar user drop down menu
const navlinkUser = document.querySelector('.navlink-user')
const navlinkDropDownMenu = document.querySelector('.navlink-drop-down-link')
const navlinkChevronDown = document.querySelector('.navlink-chevron-down > i')

navlinkUser && navlinkUser.addEventListener('click', ()=> {
    navlinkDropDownMenu.classList.toggle('show-navlink-drop-down-link')

    if(navlinkDropDownMenu.classList.contains('show-navlink-drop-down-link'))
        navlinkChevronDown.style.transform = 'rotate(180deg)'
    else{
        navlinkChevronDown.style.transform = 'rotate(0deg)'
    }
})


// Remove drop down nav menu 
const navlinkUserContainer = document.querySelector('.navlink-user-container')
let navlinks = [...document.querySelectorAll('.navlink')]
const landingPagenavlink = [...document.querySelectorAll('.landing-page-navlink')]
navlinks = [...navlinks, ...landingPagenavlink]

navlinks.forEach((link) => {
    link.addEventListener('click', (e)=> {
        navlinkDropDownMenu.classList.remove('show-navlink-drop-down-link')
        navlinkChevronDown.style.transform = 'rotate(0deg)'
    })
})

// Remove drop down nav menu when clicked outside of the navlinkUserContainer
navlinkUserContainer && window.addEventListener('click', (e)=> {
    if (!navlinkUserContainer.contains(e.target)) {
        navlinkDropDownMenu.classList.remove('show-navlink-drop-down-link')
        navlinkChevronDown.style.transform = 'rotate(0deg)'
    }
    
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