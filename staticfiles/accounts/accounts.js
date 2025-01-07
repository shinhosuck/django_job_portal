// FORM NAVBAR AND NAVLINKS

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
const helpText = (userRegisterForm && 
    Array.from(userRegisterForm.querySelectorAll('p > .helptext')))
const registerFormInputRows = (userRegisterForm && 
    Array.from(userRegisterForm.querySelectorAll('p')))
const uls = userRegisterForm && Array.from(userRegisterForm.querySelectorAll('ul'))
const labels = userRegisterForm && Array.from(userRegisterForm.querySelectorAll('label'))

function formatRegisterForm() {
    labels.forEach((label) => {
        label.innerHTML = `
            ${label.textContent.slice(0, -1)}
            <span style='color: red;'>*</span>
        `
    })

    registerFormInputRows.forEach((row) => {
        if (row.children.length === 0) {
            row.setAttribute('class', 'empty-input-row')
        }
        else {
            row.setAttribute('class', 'register-input-row')

            const input = row.querySelector('input')

            if (input.id === 'id_username' || input.id === 'id_password2') {
                const span = input.nextElementSibling
                input.placeholder = span.textContent.replaceAll('Required.', '')
                span.remove()
            }

            const spans = Array.from(row.querySelectorAll('span'))

            spans.forEach((span) => {
                if (span && !span.innerHTML) {
                    span.style.display = 'none'
                } 
            })
        }
    })

    uls.forEach((ul) => {
        if (ul.classList.length === 0) {
            ul.setAttribute('class', 'help-text-list')
        }
    })

    togglePasswordRequirements()
}
    
userRegisterForm && formatRegisterForm()


function togglePasswordRequirements() {
    const registerFormChildren = Array.from(userRegisterForm.children)
    let helpTextList = null
    let inputRow = null
    
    registerFormChildren.forEach((row) => {
        let input = null 
        if (row.classList.contains('register-input-row')) {
            if (row.querySelector('input').id === 'id_password1') {
                inputRow = row
                helpTextList = inputRow.nextElementSibling
            }
        }
    })

    helpTextList.classList.add('password-help-text-list')

    const div = document.createElement('div')
    div.setAttribute('class', 'toggle-password-requirements')
    
    div.innerHTML = `
        <span>
            Password requirements
        </span>
        <i class="fa-solid fa-chevron-down "></i>
    `
                    
    inputRow.append(div)
    handleToggleEvent(helpTextList)
}

function handleToggleEvent(helpTextList) {
    const togglePasswordRequirements = document
    .querySelector('.toggle-password-requirements')

    togglePasswordRequirements.addEventListener('click', (e) => {
        helpTextList.classList.toggle('password-help-text-list')

        if (helpTextList.classList.contains('password-help-text-list')) {
            const element = togglePasswordRequirements.lastElementChild
            element.style.transform = 'rotate(0deg)'
        }
        else {
            const element = togglePasswordRequirements.lastElementChild
            element.style.transform = 'rotate(180deg)'
        }
    })
}
