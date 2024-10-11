const contactForm = Array.from(document.querySelectorAll('.contact-form > p'))
                    
contactForm.forEach((p)=> {
    p.setAttribute('class', 'contact-form-row')
})

// Mobile navbar: toggle mobile navlinks
const mobileNavLinksToggleBtnsContainer = document.querySelector('.landing-page-mobile-navlinks-toggle-btns-container')
const navLinksToggleBtns = [...mobileNavLinksToggleBtnsContainer.querySelectorAll('button')]
const mobileNavLinks = document.querySelector('.landing-page-mobile-navlinks')

const openBtn = document.querySelector('.landing-page-mobile-navlinks-open-btn')
const closeBtn = document.querySelector('.landing-page-mobile-navlinks-close-btn')

navLinksToggleBtns.forEach((btn) => {
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