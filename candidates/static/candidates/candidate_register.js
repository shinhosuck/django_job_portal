const educationElements = `
    <p>
         <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_major">Major:</label>
        <input type="text" name="major" maxlength="255" id="id_major">
    </p>
    <p>
         <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_degree">Degree:</label>
        <input type="text" name="degree" maxlength="255" id="id_degree">
    </p>
    <p>
         <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_institution">Institution:</label>
        <input type="text" name="institution" maxlength="255" id="id_institution">
    </p>
    <p>
         <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_completion_date">Completion date:</label>
        <input type="date" name="completion_date" id="id_completion_date">
    </p>`

const experienceElements = `
    <p>
        <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_company_name">Company name:</label>
        <input type="text" name="company_name" maxlength="255" id="id_company_name">
    </p>
    <p>
        <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_position">Position:</label>
        <input type="text" name="position" maxlength="255" id="id_position">
    </p>
    <p>
        <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_start_date">Start date:</label>
        <input type="date" name="start_date" id="id_start_date"> 
    </p>
    <p>
        <span class="candidate-input-error-field">
            This field is required.
        </span>
        <label for="id_end_date">End date:</label>
        <input type="date" name="end_date" id="id_end_date">
    </p>`

const candidateRegisterForm = document.querySelector('.candidate-register-form')

const educationFormContainer = document.querySelector('.education-form-container')
const experienceFormContainer = document.querySelector('.experience-form-container')

const candidateForm = document.querySelector('.candidate-info-form')
const educationForm = document.querySelector('.education-form')
const experienceForm = document.querySelector('.experience-form')

const candidateRegisterFormBtn = document.querySelector('.candidate-register-form-btn')
const addMoreBtns = Array.from(document.querySelectorAll('.add-more'))

const candidateProfileButtonText = document.querySelector('.candidate-profile-button-text')
const candidateFormButtonSpinner = document.querySelector('.candidate-form-button-spinner')

const candidateRegisterFormError = document.querySelector('.candidate-register-form-warning')

// Froms count
let formsCount = parseInt(
    Array.from(
        document.querySelectorAll('.candidate-form')
    ).length)

const formsSent = {1:false}

window.addEventListener('DOMContentLoaded', createInputElements)

// Append input elements (on page load)
async function createInputElements(e) {
    const session = JSON.parse(sessionStorage.getItem('form_ids'))
   
    if (!session || !session.education.length 
        && !session.experience.length) {
        
        sessionStorage.setItem(
            'form_ids', JSON.stringify({education:[], experience:[]}))

        const educationInputContainer = document.createElement('div')
        const experienceInputContainer = document.createElement('div')

        const {education, experience} = await preFillFormData()

        if (!education || !education.length) {
            educationInputContainer.setAttribute('class', 'education-form candidate-form')
            educationInputContainer.setAttribute('data-form-count', `${formsCount+1}`)
            formsCount ++
            formsSent[formsCount] = false
            educationInputContainer.innerHTML = educationElements
            educationFormContainer.append(educationInputContainer)
        }
        if (!experience || !experience.length) {
            experienceInputContainer.setAttribute('class', 'experience-form candidate-form')
            experienceInputContainer.setAttribute('data-form-count', `${formsCount+1}`)
            formsCount ++
            formsSent[formsCount] = false
            experienceInputContainer.innerHTML = experienceElements
            experienceFormContainer.append(experienceInputContainer)
        }

        if (education?.length && experience?.length) {
            const data = {education:education, experience:experience}
            renderPreviousFormInputs(data)
        }
        if (education?.length && !experience?.length) {
            formatEducationInputTemplate(education)
        }
        if (experience?.length && !education?.length) {
            formatExperienceInputTemplate(experience)
        }
    }
    else{
        fetchPreviousFormData()
    }
}


async function preFillFormData() {
    const url = `${window.location.origin}/prefetch/formdata/`

    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Data-Type': 'application/json'
            }
        });
        const data = await resp.json()
        
        if (data?.error) {
            console.log(data.error)
        }
        return data

    } catch (error) {
        console.log(error.message, error.type)
    }
}

// Listen for addMoreBtns click event
candidateRegisterForm && addMoreBtns.forEach((btn) => {
    btn.addEventListener('click', addExtraFormElement)
})

// Add Extra forms
function addExtraFormElement(e) {
    e.preventDefault()

    if (e.currentTarget.classList.contains('education')) {
        const div = document.createElement('div')
        div.setAttribute('class', 'education-form')
        div.setAttribute('data-form-count', `${formsCount + 1}`)
        formsCount ++

        formsSent[formsCount] = false

        div.innerHTML = educationElements
        educationFormContainer.append(div)
    }
    else if (e.currentTarget.classList.contains('experience')){
        const div = document.createElement('div')
        div.setAttribute('class', 'experience-form')
        div.setAttribute('data-form-count', `${formsCount + 1}`)
        formsCount ++
        
        formsSent[formsCount] = false

        div.innerHTML = experienceElements
        experienceFormContainer.append(div)
    }
}

// Trigger Functions
candidateRegisterFormBtn.addEventListener('click', (e) => {
    e.preventDefault()

    candidateProfileButtonText.style.display = 'none'
    candidateFormButtonSpinner.style.display = 'block'

    const candidateFormChildren = Array.from(candidateForm.querySelectorAll('p > *'))
    .filter((ele) => ele.type !== undefined)
    handlecandidateFormData(candidateFormChildren)

    const educationFormChildren = Array.from(educationFormContainer.querySelectorAll('.education-form'))
    handleEducationFormData(educationFormChildren)

    const experienceFormChildren = Array.from(experienceFormContainer.querySelectorAll('.experience-form'))
    handleExperienceFormData(experienceFormChildren)
})

// Candidate info form
function handlecandidateFormData(data) {
    let formData = new FormData()
    let allFieldsValid = true

    const formIndex = parseInt(candidateForm.getAttribute('data-form-count'))
       
    data.forEach((item) => {
        const fieldError = item.previousElementSibling
        .previousElementSibling

        if (!item.value && item.name !== 'resume') {
            fieldError.style.display = 'grid'
            allFieldsValid = false
            formData = new FormData()

            candidateProfileButtonText.style.display = 'flex'
            candidateFormButtonSpinner.style.display = 'none'
        }
        else {
            fieldError.style.display = 'none'
        }

        if (item.name === 'resume') {
            formData.append(item.name, item.files[0])
        }
        else {
            formData.append(item.name, item.value)
        }
       
    })

    if (allFieldsValid) {
        registerCandidate(formData, 'candidate_info', candidateForm, formIndex)
        formData = new FormData()
    }
}

// Candidate Education
function handleEducationFormData(data) {
    const dataContainer = Array.from(data)
    let formData = new FormData()
    let allFieldsValid = true

    dataContainer.forEach((item) => {

        const formIndex = parseInt(item.getAttribute('data-form-count'))
        const formID = parseInt(item.getAttribute('id'))

        const dataInputs = Array.from(item.querySelectorAll('p > *'))
        .filter((ele) => ele.name)

        dataInputs.forEach((input) => {
            const fieldError = input.previousElementSibling
            .previousElementSibling

            if (!input.value) {
                fieldError.style.display = 'grid'
                allFieldsValid = false
                formData = new FormData()
                formsSent[formIndex] = false

                candidateProfileButtonText.style.display = 'flex'
                candidateFormButtonSpinner.style.display = 'none'

            }
            else {
                fieldError.style.display = 'none'
            }

            formData.append(input.name, input.value)
        })

        if (allFieldsValid) {
            if (formID) {
                formData.append('id', formID)
            }
            registerCandidate(formData, 'education', item, formIndex)
            formData = new FormData()
        }
    })
}

// Candidate Experience
function handleExperienceFormData(data) {
    const dataContainer = Array.from(data)
    let formData = new FormData()
    let allFieldsValid = true

    dataContainer.forEach((item) => {
        
        const formIndex = parseInt(item.getAttribute('data-form-count'))
        const formID = parseInt(item.getAttribute('id'))
        
        const dataInputs = Array.from(item.querySelectorAll('p > *'))
        .filter((ele) => ele.name)

        dataInputs.forEach((input) => {
            const fieldError = input.previousElementSibling
            .previousElementSibling

            if (!input.value) {
                fieldError.style.display = 'grid'
                allFieldsValid = false
                formData = new FormData()
                formsSent[formIndex] = false

                candidateProfileButtonText.style.display = 'flex'
                candidateFormButtonSpinner.style.display = 'none'
            }
            else {
                fieldError.style.display = 'none'
            }

            formData.append(input.name, input.value)
        })

        if (allFieldsValid) {
            if (formID) {
                formData.append('id', formID)
            }

            registerCandidate(formData, 'experience', item, formIndex)
            formData = new FormData()
        }
    })
}

async function registerCandidate(formData, type, item, formIndex) {
    const url = `${window.location.origin}/candidates/register/?type=${type}`
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        const data = await resp.json()

        if (data?.warning || data?.error) {
            handleFormErrorAndWarning(data)
        }
        else {
            saveObjectIDs(data, item)

            console.log(item)
            console.log(data)

            if (!formsSent[formIndex]) {
                formsSent[formIndex] = true
            }
        }

        const allSubmitted = checkAllFormsSubmitted()
        console.log('LAST FROM:', allSubmitted)
        
        if (allSubmitted) {
            window.location.href = `${window.location.origin}/candidates/jobs/`
        }
    } 
    catch (error) {
        console.log(error.message, error.type)
    }

}


function checkAllFormsSubmitted() {
    let isLastForm = true

    const keys = Object.keys(formsSent)

    keys.forEach((key) => {
        if (!formsSent[key]) {
            isLastForm = false
        }
    })

    if (isLastForm) {
        keys.forEach((key) => {
            formsSent[key]=false
        })
    }

    return isLastForm
}

function saveObjectIDs(data, item) {
    candidateProfileButtonText.style.display = 'flex'
    candidateFormButtonSpinner.style.display = 'none'

    form_ids = JSON.parse(sessionStorage.getItem('form_ids'))

    if (data?.candidate_id) {
        sessionStorage.setItem('candidate_id', JSON.stringify(data))
    }
    if (data?.education_id) {
        if(!form_ids.education.includes(parseInt(data.education_id))) {
            form_ids.education.push(data.education_id)
        }
        item.setAttribute('id', data.education_id)
    }
    if (data?.experience_id){
        if (!form_ids.experience.includes(parseInt(data.experience_id))) {
            form_ids.experience.push(data.experience_id)
        }
        item.setAttribute('id', data.experience_id)
    }

    sessionStorage.setItem('form_ids', JSON.stringify(form_ids))
}


function handleFormErrorAndWarning(data) {
    window.scrollTo({top:0, left:0, behavior:"smooth"})

    data?.error && candidateRegisterFormError.classList
    .add('candidate-register-form-error')

    candidateRegisterFormError.style.display = 'flex'
    candidateRegisterFormError.innerHTML = `
        <span>
            ${data?.warning || data?.error}
        </span>
        <i 
            class="
                fas fa-close 
                close-candidate-register-form-error
            "
        ></i>
    `
    // Close candidate register form warning
    const closeCandidateRegisterFormError = document.querySelector(
        '.close-candidate-register-form-error')

    closeCandidateRegisterFormError.addEventListener('click', () => {
        candidateRegisterFormError.style.display = 'none'
    })
}

/* ===============================================================================
THIS SECTION OF FUNCTIONS WILL BE CALLED IF THERE IS A DATA IN THE SESSION STORAGE
================================================================================== */

async function fetchPreviousFormData() {
    const {education, experience} = JSON.parse(sessionStorage.getItem('form_ids'))
    const url = `${window.location.origin}/fetch/form-data/`
    const csrfToken = getCsrfToken('csrftoken')

    const body = {
        'education': Boolean(education.length) ? education : null,
        'experience': Boolean(experience.length) ? experience : null
    }

    const resp = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(body)
    })
    const data = await resp.json()
    renderPreviousFormInputs(data)
}


function renderPreviousFormInputs(data) {
    const {education, experience} = data 

    if (education) {
        formatEducationInputTemplate(education)
    }
    if (experience) {
        formatExperienceInputTemplate(experience)
    }
}


function formatEducationInputTemplate(education) {
    if (!Boolean(education.length)) {
        handleEmptyArray('education')
    }
    else{
        education.forEach((edu) => {
            formsCount ++
            formsSent[formsCount] = false
            const educationInputContainer = document.createElement('div')

            educationInputContainer.setAttribute('class', 'education-form candidate-form')
            educationInputContainer.setAttribute('data-form-count', `${formsCount}`)
            educationInputContainer.setAttribute('id', `${edu.id}`)

            const education = `
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_major">Major:</label>
                    <input type="text" name="major" value='${edu.major}' maxlength="255" id="id_major">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_degree">Degree:</label>
                    <input type="text" name="degree" value='${edu.degree}' maxlength="255" id="id_degree">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_institution">Institution:</label>
                    <input type="text" name="institution"value='${edu.institution}' maxlength="255" id="id_institution">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_completion_date">Completion date:</label>
                    <input type="date" name="completion_date" value='${edu.completion_date}'id="id_completion_date">
                </p>`
            
            educationInputContainer.innerHTML = education
            educationFormContainer.append(educationInputContainer)
        })
    }
}

function formatExperienceInputTemplate(experience) {
    if (!Boolean(experience.length)) {  
      handleEmptyArray('experience')
    }
    else {
        experience.forEach((ex) => {
            formsCount ++
            formsSent[formsCount] = false
            const experienceInputContainer = document.createElement('div')

            experienceInputContainer.setAttribute('class', 'experience-form candidate-form')
            experienceInputContainer.setAttribute('data-form-count', `${formsCount}`)
            experienceInputContainer.setAttribute('id', `${ex.id}`)

            const experience = `
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_company_name">Company name:</label>
                    <input type="text" name="company_name" value='${ex.company_name}' maxlength="255" id="id_company_name">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_position">Position:</label>
                    <input type="text" name="position" value='${ex.position}'  maxlength="255" id="id_position">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_start_date">Start date:</label>
                    <input type="date" name="start_date" value='${ex.start_date}' id="id_start_date"> 
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_end_date">End date:</label>
                    <input type="date" name="end_date" value='${ex.end_date}' id="id_end_date">
                </p>`

            experienceInputContainer.innerHTML = experience
            experienceFormContainer.append(experienceInputContainer)
        })
    }
}


function handleEmptyArray(dataType) {
    formsCount ++
    formsSent[formsCount] = false
    const div = document.createElement('div')

    if (dataType === 'education') {
        div.setAttribute('class', 'education-form candidate-form')
        div.setAttribute('data-form-count', `${formsCount}`)
    }

    else if (dataType === 'experience') {
        div.setAttribute('class', 'experience-form candidate-form')
        div.setAttribute('data-form-count', `${formsCount}`)
    }

    if (div.classList.contains('experience-form')) {
        div.innerHTML = experienceElements
        experienceFormContainer.append(div)
    }
    else if(div.classList.contains('education-form')) {
        div.innerHTML = educationElements
        educationFormContainer.append(div)
    }
}


function getCsrfToken(csrftoken) {
    const cookie = document.cookie.split(';')
    .find((item)=>item.startsWith(csrftoken))
    .split('=').slice(-1)[0].trim()
    
    return cookie || null
}
