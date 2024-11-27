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
            const spans = Array.from(row.querySelectorAll('span'))

            spans.forEach((span) => {
                if (span && !span.innerHTML) {
                    span.style.display = 'none'
                } 
                else {
                    span.textContent = span.textContent.replaceAll('Required.', '')
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
    const helpTextList = registerFormChildren[4]
    const inputRow = registerFormInputRows[2]

    helpTextList.classList.add('password-help-text-list')

    const div = document.createElement('div')
    div.setAttribute('class', 'toggle-password-requirements')
    
    div.innerHTML = `<h4>
                        <span>
                            See password requirements
                        </span>
                        <span>
                            <i class="fa-solid fa-chevron-down "></i>
                        </span>
                    </h4>`
                    
    inputRow.append(div)
    handleToggleEvent(helpTextList)
}

function handleToggleEvent(helpTextList) {
    const togglePasswordRequirements = document.querySelector('.toggle-password-requirements')

    togglePasswordRequirements.addEventListener('click', () => {
        helpTextList.classList.toggle('password-help-text-list')

        if (helpTextList.classList.contains('password-help-text-list')) {
            const element = (togglePasswordRequirements.
                lastElementChild.lastElementChild.lastElementChild)
            element.style.transform = 'rotate(0deg)'
        }
        else {
            const element = (togglePasswordRequirements.
                lastElementChild.lastElementChild.lastElementChild)
            element.style.transform = 'rotate(180deg)'
        }
    })
}
