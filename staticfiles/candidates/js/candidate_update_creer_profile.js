const form = document.querySelector('.candidate-update-form')
const formInputRows = Array.from(form.querySelectorAll('p'))
const data = JSON.parse(localStorage.getItem('selectForm'))

const loadFunction = data?.dataType === 'profile' 
&& updateCandidateProfile() || data?.dataType === 'qualification' 
&& updateCandidateQualification()

window.addEventListener('DOMContentLoaded', hideFormInutUserType)


// Hide form input user_type
// if user profile.user_type has a value.
function hideFormInutUserType() {
    formInputRows.forEach((element) => {
        const user_type = localStorage.getItem('user_type')
        const select = element.querySelector('select')

        if (select && select.id ==='id_user_type' && user_type !== 'null') {
            select.parentElement.style.display = 'none'
        }
        element.setAttribute('class', 'form-input-row')
    })
}


// PROFILE FORM
// Profile form first input/profile image input
function updateCandidateProfile() {
    const profileImageInputRow = formInputRows[0]
    const children = Array.from(profileImageInputRow.querySelectorAll('*'))

    const newLabel = document.createElement('label')
    const newDiv = document.createElement('div')
    
    let label = null
    let anchor = null
    let input = null

    children.forEach((element) => {
        newDiv.setAttribute('class', 'new-input-container')

        if (element.getAttribute('for') === 'id_profile_image') {
            label = element
            label.textContent = 'Upload image'
            label.removeAttribute('for')
            label.setAttribute('class', 'image-input-wrapper')

            newLabel.setAttribute('for', 'id_profile_image')
        }
        if (Boolean(element.href)) {
            anchor = element
            anchor.textContent = `Current: ${anchor.textContent.split('/').slice(-1)[0].toLowerCase()}`
            anchor.setAttribute('target', '_blank')
            anchor.setAttribute('class', 'image-anchor')
        }
        if (element.id === 'id_profile_image') {
            input = element
            input.style.display = 'none'
            input.addEventListener('change', handleInputOnChange)
        }

        if (anchor && input) {
            label.append(input)
            
            newDiv.append(label)
            anchor && newDiv.append(anchor)

            newLabel.textContent = 'Profile image:'

            profileImageInputRow.innerHTML = ''
            profileImageInputRow.append(newLabel)
            profileImageInputRow.append(newDiv)
        }
    })
}

// END OF PROFILE FORM

// QUALIFICATION FORM
// File input/resume input
function updateCandidateQualification() {
    const resumeFormInputRow = formInputRows[2]
    const children = resumeFormInputRow.querySelectorAll('*')

    const newDiv = document.createElement('div')
    const newLabel = document.createElement('label')
    
    let label = null 
    let input = null 
    let a = null

    children.forEach((element) => {

        if (element.getAttribute('for') === 'id_resume') {
            label = element
            label.textContent = 'Upload resume'
            label.removeAttribute('for')
            label.setAttribute('class', 'image-input-wrapper')
        }
        if (element.id === 'id_resume') {
            input = element
            input.style.display = 'none'
            input.addEventListener('change', handleInputOnChange)
        }
        if (element.href) {
            a = element
            a.textContent = `Current: ${a.textContent.split('/')
                .slice(-1)[0].replaceAll(' ', '').toLowerCase()}`
            a.setAttribute('target', '_blank')
            a.setAttribute('class', 'image-anchor')
        }
    })

    label.append(input)

    newLabel.setAttribute('for', 'id_resume')
    newLabel.textContent = 'Resume:'

    newDiv.append(label)
    a && newDiv.append(a)
    newDiv.setAttribute('class', 'new-input-container')

    resumeFormInputRow.innerHTML = ''
    resumeFormInputRow.append(newLabel)
    resumeFormInputRow.append(newDiv)
}
// END OF QUALIFICATION FORM


function handleInputOnChange(e) {
    const newInputContainer = document.querySelector('.new-input-container')
    const imageAnchor = document.querySelector('.image-anchor')
    const chosenImageContainer = document.querySelector('.chosen-image-container')

    const p = document.createElement('p')
    const span = document.createElement('span')
    const i = document.createElement('i')

    p.setAttribute('class', 'chosen-image-container')
    span.setAttribute('class', 'chosen-text-content')

    i.setAttribute('class', 'fas fa-close remove-chosen-image')
    i.addEventListener('click', removeChosenImage)
    i.style.lineHeight = '0'

    span.innerHTML = `Chosen: ${e.currentTarget.files[0].name.replaceAll(' ','').toLowerCase()}`

    p.append(span)
    p.append(i)

    chosenImageContainer && chosenImageContainer.remove()

    newInputContainer.insertBefore(p, imageAnchor)
}


function removeChosenImage() {
    const imageInputWrapper = document.querySelector('.image-input-wrapper')
    const input = document.querySelector('#id_profile_image') || 
        document.querySelector('#id_resume')
    const chosenImageContainer = document.querySelector('.chosen-image-container')
    const newInput = document.createElement('input')

    newInput.addEventListener('change', handleInputOnChange)

    if (data === 'profile') {
        newInput.setAttribute('accept', 'image/*')
    }

    newInput.setAttribute('type', 'file')
    newInput.setAttribute('id', 'id_profile_image')
    newInput.style.display = 'none'

    input.remove()
    chosenImageContainer.remove()

    imageInputWrapper.append(newInput)
}