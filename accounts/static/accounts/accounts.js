// From navbar and navlinks

const formNavlinksToggleBtns = Array.from(
    document.querySelectorAll('.form-navlinks-toggle-btn')
)

formNavlinksToggleBtns.forEach((btn) => {
    const btnChildren = Array.from(btn.children) 

    btn.addEventListener('click', () => {
        btn.nextElementSibling.classList.toggle('show-form-navlinks')

        btnChildren.forEach((child) => {
            if (child.classList.contains(
                'remove-form-navlinks-toggle-btn-child'
            )) {
                child.classList.remove(
                    'remove-form-navlinks-toggle-btn-child'
                )
            }else {
                child.classList.add(
                    'remove-form-navlinks-toggle-btn-child'
                )
            }
        })

    })  
})


// FORMS

// Register form
const userRegisterForm = document.querySelector('.register-from')

if (userRegisterForm) {
    const inputRows = Array.from(userRegisterForm.querySelectorAll('p'))
    const uls = Array.from(userRegisterForm.querySelectorAll('ul'))
    const inputs = Array.from(userRegisterForm.querySelectorAll('input'))
    const select = userRegisterForm.querySelector('select')
    const options = Array.from(select.querySelectorAll('option'))

    const text = document.createTextNode('Please select an item in the list')
    options[0].appendChild(text)


    inputs.forEach((input) => {
        input.setAttribute('required', '')
    })

    inputRows.forEach((row) => {
        if (row.children.length === 0) {
            row.setAttribute('class', 'empty-input-row')
        }
        else {
            row.setAttribute('class', 'register-input-row')
        }
    })

    uls.forEach((ul) => {
        if (ul.classList.length === 0) {
            ul.setAttribute('class', 'help-text-list')
        }
    })
}