const contactForm = Array.from(document.querySelectorAll('.contact-form > p'))
                    
contactForm.forEach((p)=> {
    p.setAttribute('class', 'contact-form-row')
})