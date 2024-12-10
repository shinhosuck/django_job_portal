// EMPLOYER REGISTER
const employerRegisterForm = document.querySelector('.employer-register-form')

employerRegisterForm && formatEmployerRegisterForm()

function formatEmployerRegisterForm() {
    const formInputWrappers = employerRegisterForm && 
    Array.from(employerRegisterForm.querySelectorAll('p'))
    .map((p) => {
        p.setAttribute('class', 'employer-register-input-row')
        return p
    })

    const logoInputRow = formInputWrappers[1]
    const children = Array.from(logoInputRow.querySelectorAll('*'))
    const newDiv = document.createElement('div')
    const newLabel = document.createElement('label')
    
    newDiv.setAttribute('class', 'employer-image-input-container')

    newLabel.setAttribute('for', 'id_logo')
    newLabel.textContent = 'Logo:'

    let label = null
    let anchor = null
    let input = null 

    children.forEach((element) => {
        if(element.getAttribute('for') === 'id_logo') {
            label = element
            label.textContent = 'Upload logo'
            label.setAttribute('class', 'employer-logo-image-wrapper')
            label.removeAttribute('for')
        }
        if (element.id === 'id_logo') {
            input = element
            input.style.display = 'none'
            input.addEventListener(
                'change',
                 handleProfileImageChange
            )
        }
        if(element.href) {
            anchor = element
            anchor.setAttribute('class', 'employer-log-url')
            anchor.textContent = `${anchor.textContent.split('/')
                .slice(-1)[0].replaceAll(' ', '').toLowerCase()}`
        }
    })
    
    label.append(input)

    newDiv.append(label)
    anchor && newDiv.append(anchor) 

    logoInputRow.innerHTML = ''
    logoInputRow.append(newLabel)
    logoInputRow.append(newDiv)

}

function handleProfileImageChange() {
    const chosenLogo = document.querySelector('.chosen-company-logo')
    const employerImageInputContainer = document.querySelector('.employer-image-input-container')
    const employerLogoUrl = document.querySelector('.employer-log-url')
    const idLogo= document.querySelector('#id_logo')

    chosenLogo && chosenLogo.remove()

    const newChosenLogo = document.createElement('p')

    newChosenLogo.setAttribute('class', 'chosen-company-logo')
    newChosenLogo.innerHTML = `
        <span>Selected: ${idLogo.files[0].name.replaceAll(' ', '').toLowerCase()}</span>
        <i class="fas fa-close remove-company-logo"></i>
    `

    if (employerLogoUrl) {
        employerImageInputContainer.insertBefore(newChosenLogo, employerLogoUrl)
    }
    else {
        employerImageInputContainer.append(newChosenLogo)
    }

    const removeCompanyLogoBtn = document.querySelector('.remove-company-logo')
    removeCompanyLogoBtn.addEventListener('click', removeChosenCompanyLogo)
}


function removeChosenCompanyLogo(e) {
    const chosenLogo = document.querySelector('.chosen-company-logo')
    const idLogo = document.querySelector('#id_logo')
    const employerLogoContainer = document.querySelector('.employer-logo-image-wrapper')
    const newInput = document.createElement('input')

    newInput.setAttribute('type', 'file')
    newInput.setAttribute('name', 'logo')
    newInput.setAttribute('accept', 'image/*')
    newInput.setAttribute('id', 'id_logo')
    newInput.addEventListener(
        'change', 
        handleProfileImageChange
    )
    newInput.style.display = 'none'
    
    chosenLogo.remove()
    idLogo.remove()

    employerLogoContainer.append(newInput)
}
// END


// EMPLOYER DASHBOARD
const JobApplicationHeaders = Array.from(document.querySelectorAll(
    '.employer-dashboard-employer-job-applicants-header'
))

JobApplicationHeaders && formatJobApplicationHeader()

function formatJobApplicationHeader() {
    JobApplicationHeaders.forEach((header) => {
        const span = header.querySelector('span')
        const chevronBtn = header.querySelector('i')

        if (span.textContent !== 'No applicant') {
            header.addEventListener('click', (e) => {
                header.nextElementSibling.classList.toggle(
                    'show-employer-dashboard-employer-job-applicants'
                )
                
                if (header.nextElementSibling.classList.contains(
                    'show-employer-dashboard-employer-job-applicants')) {
                        chevronBtn.style.transform = 'rotate(180deg)'
                    }
                else {
                    chevronBtn.style.transform = 'rotate(0deg)'
                }
            })
        }
        else {
            header.style.cursor = 'auto'
        }
    })
}
// END
