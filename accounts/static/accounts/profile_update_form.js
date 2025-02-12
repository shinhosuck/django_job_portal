const profileInputContainer = document.querySelector('.profile-input-container')
const profileInputRows = Array.from(document.querySelectorAll('.profile-input-row'))
const firstProfileInputRow = profileInputRows[0]
const label = firstProfileInputRow.querySelector('label')
let input = firstProfileInputRow.querySelector('input')
const anchor = firstProfileInputRow.querySelector('a')

let selectedProfileImage = null


window.addEventListener('DOMContentLoaded', formatFileInput)

// Create custom file input
function formatFileInput() {
    const div = document.createElement('div')
    const newLabel = document.createElement('label')

    input.addEventListener('change', handleProfileImageInput)

    div.setAttribute('class', 'profile-image-input-container')
    newLabel.textContent = 'Profile image:'
    newLabel.setAttribute('for', 'id_profile_image')

    label.textContent = 'Upload image'
    label.classList.add('label-image-input-wrapper')
    label.removeAttribute('for')

    anchor.textContent = `Current: ${anchor.textContent.split('/').slice(-1)}`
    anchor.classList.add('current-image-url')

    label.append(input)
    div.append(label)
    div.append(anchor)

    firstProfileInputRow.innerHTML = ''

    firstProfileInputRow.append(newLabel)
    firstProfileInputRow.append(div)
    // splitForm()
}

// Handles file input change
function handleProfileImageInput() {

    if (selectedProfileImage) {
        selectedProfileImage.remove()
    }

    const file = input.files[0]?.name
    const p = document.createElement('p')
    const tags = `
        <span>Selected: ${file}</span>
        <i class="fas fa-close remove-selected-profile-image-btn"></i>
    `
    p.innerHTML = tags
    p.setAttribute('class', 'selected-profile-image')
    insertSelectedImageTag(p)
}


// Insert selected file/image
function insertSelectedImageTag(p) {
    const profileInputContainer = document.querySelector(
        '.profile-image-input-container')
    const currentImageURL = document.querySelector(
        '.current-image-url')

    profileInputContainer.insertBefore(p, currentImageURL)

    selectedProfileImage = document.querySelector(
        '.selected-profile-image')


    const span = selectedProfileImage.querySelector('span')
    span.style.overflow = 'hidden'
    span.style.whiteSpace = 'nowrap'
    span.style.textOverflow = 'ellipsis'
    span.style.fontSize = '0.95rem'


    const removeSelectedProfileImageBtn = document.querySelector(
        '.remove-selected-profile-image-btn')

    removeSelectedProfileImageBtn.addEventListener('click', (e) => {
        
        selectedProfileImage.remove()

        input = document.querySelector('#id_profile_image')
        input.remove()

        const newInput = document.createElement('input')

        newInput.setAttribute('type', 'file')
        newInput.setAttribute('name', 'profile_image')
        newInput.setAttribute('accept', 'image/*')
        newInput.setAttribute('id', 'id_profile_image')
        newInput.addEventListener('change', handleProfileImageInput)

        label.append(newInput)
        input = document.querySelector('#id_profile_image')
    })
}

const notRequired = ['Profile image:', 'Phone number:', 'Social link:', 'Personal Website:']
const profileForm = document.querySelector('.profile-form')
const profileFormLabels = Array.from(profileForm.querySelectorAll('label'))

profileFormLabels.forEach((label) => {
    if (label.textContent !== 'Upload image' && notRequired.includes(label.textContent)) {
        label.innerHTML = `
            <span>${label.textContent.slice(0, -1)}</span>
        `
    }else if (label.textContent !== 'Upload image' && !notRequired.includes(label.textContent)) {
        label.innerHTML = `
            <span>${label.textContent.slice(0, -1)}</span>
            <span style="color: red;">*</span>
        `
    }
})
  
  