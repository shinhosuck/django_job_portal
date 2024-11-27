const qualificationElements = `
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_industry">Industry:</label>
            <select name="industry" autofocus="" required="" id="id_industry">
                <option value="" selected="">---------</option>
                <option value="technology">Technology</option>
                <option value="finance">Finance</option>
                <option value="healthcare">Healthcare</option>
                <option value="education">Education</option>
                <option value="marketing &amp; advertising">Marketing &amp; Advertising</option>
                <option value="engineering">Engineering</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="retail &amp; sales">Retail &amp; Sales</option>
                <option value="hospitality">Hospitality</option>
                <option value="construction">Construction</option>
                <option value="telecommunications">Telecommunications</option>
                <option value="real estate">Real Estate</option>
                <option value="nonprofit">Nonprofit</option>
                <option value="food and beverage">Food and Beverage</option>
                <option value="government">Government</option>
                <option value="arts &amp; entertainment">Arts &amp; Entertainment</option>
                <option value="other">Other</option>
            </select>
        </p>
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_job_title">Job title:</label>
            <input type="text" name="job_title" maxlength="200" required="" id="id_job_title">
        </p>
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_resume">Resume:</label>
            <input type="file" name="resume" id="id_resume">
        </p>
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_skills">Skills:</label>
            <input type="text" name="skills" maxlength="200" id="id_skills">
        </p>`

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
            <label for="id_start_date">Start date:</label>
            <input type="date" name="start_date" onkeydown="return false" id="id_start_date">
        </p>
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_completion_date">Completion date:</label>
            <input type="date" name="completion_date" onkeydown="return false" id="id_completion_date">
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
            <input type="date" name="start_date" onkeydown="return false" id="id_start_date"> 
        </p>
        <p>
            <span class="candidate-input-error-field">
                This field is required.
            </span>
            <label for="id_end_date">End date:</label>
            <input type="date" name="end_date" onkeydown="return false" id="id_end_date">
        </p>`

const inputsNotRequired = [
    'resume', 'skills', 'major', 'degree', 'institution', 'start_date',
    'completion_date', 'company_name', 'position', 'start_date', 'end_date'
]

const candidateRegisterForm = document.querySelector('.candidate-register-form')

const qualificationFormContainer = document.querySelector('.qualification-form-container')
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

let resumeInput = null
let parentFormSubmited = false

// Froms count
let formsCount = 0
const formsSent = {}

window.addEventListener('DOMContentLoaded', createInputElements)


// APPEND FORM INPUT ELEMENTS -> THIS WILL RUN ON RELOAD, INITIAL LOAD
async function createInputElements(e) {
    const session = JSON.parse(sessionStorage.getItem('form_ids'))
    
    if (!session || !session.qualification.length && !session.education.length 
        && !session.experience.length) {

        window.sessionStorage.setItem(
            'form_ids', 
            JSON.stringify({
                qualification:[], 
                education:[], 
                experience:[]
            })
        )

        const qualificationInputContainer = document.createElement('div')
        const educationInputContainer = document.createElement('div')
        const experienceInputContainer = document.createElement('div')

        // Pre fetch form data on reload and session storage does not have form_ids: 
        // form_ids = {"qualification": [],"education": [],"experience": []}

        const {qualification, education, experience} = await preFillFormData()
        
        if (!qualification || !qualification.length) {
            formsCount++
            qualificationInputContainer.setAttribute('class', 'qualification-form candidate-form')
            qualificationInputContainer.setAttribute('data-form-count', `${formsCount}`)
            formsSent[formsCount] = false
            qualificationInputContainer.innerHTML = qualificationElements
            qualificationFormContainer.append(qualificationInputContainer)
            createCustomFileUplodInput()
        }

        if (!education || !education.length) {
            formsCount++
            educationInputContainer.setAttribute('class', 'education-form candidate-form')
            educationInputContainer.setAttribute('data-form-count', `${formsCount}`)
            formsSent[formsCount] = false
            educationInputContainer.innerHTML = educationElements
            educationFormContainer.append(educationInputContainer)
        }
        if (!experience || !experience.length) {
            formsCount++
            experienceInputContainer.setAttribute('class', 'experience-form candidate-form')
            experienceInputContainer.setAttribute('data-form-count', `${formsCount}`)
            formsSent[formsCount] = false
            experienceInputContainer.innerHTML = experienceElements
            experienceFormContainer.append(experienceInputContainer)
        }
       
        if (qualification?.length || education?.length || experience?.length) {
        
            if (qualification?.length) {
                formatQualificationInputTemplate(qualification)
            }
            if (education?.length) {
                formatEducationInputTemplate(education)
            }
            if (experience?.length) {
                formatExperienceInputTemplate(experience)
            }
        }
    }
    else{
        // If data in session storage: form_ids = {"qualification": [1],"education": [22, 33],"experience": [44]}
        fetchPreviousFormData()
    }

    resumeInput = document.querySelector('#id_resume')
    resumeInput.setAttribute('onchange', 'handleResumeFileInput()')
}

async function preFillFormData() {
    const url = `${window.location.origin}/candidates/prefetch/formdata/`

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

    const div = document.createElement('div')

    if (e.currentTarget.classList.contains('qualification')) {
        formsCount ++
        div.setAttribute('class', 'qualification-form')
        div.setAttribute('data-form-count', `${formsCount}`)
        
        formsSent[formsCount] = false

        div.innerHTML = qualificationElements
        qualificationFormContainer.append(div)
    }
    else if (e.currentTarget.classList.contains('education')) {
        formsCount ++
        div.setAttribute('class', 'education-form')
        div.setAttribute('data-form-count', `${formsCount}`)
       
        formsSent[formsCount] = false

        div.innerHTML = educationElements
        educationFormContainer.append(div)
    }
    else if (e.currentTarget.classList.contains('experience')){
        formsCount ++
        div.setAttribute('class', 'experience-form')
        div.setAttribute('data-form-count', `${formsCount}`)
        
        formsSent[formsCount] = false

        div.innerHTML = experienceElements
        experienceFormContainer.append(div)
    }
}

// Trigger Functions
candidateRegisterFormBtn.addEventListener('click', (e) => {
    e.preventDefault()
    const location = JSON.parse(sessionStorage.getItem('location'))

    candidateProfileButtonText.style.display = 'none'
    candidateFormButtonSpinner.style.display = 'block'

    const qualificationFormChildren = Array.from(
        qualificationFormContainer.querySelectorAll('.qualification-form'))

    submitQualificationFormData(qualificationFormChildren, location.user)
})


function submitChildForms() {
    const location = JSON.parse(sessionStorage.getItem('location'))

    const educationFormChildren = Array.from(
        educationFormContainer.querySelectorAll('.education-form'))

    const experienceFormChildren = Array.from(
        experienceFormContainer.querySelectorAll('.experience-form'))

    submitEducationFormData(educationFormChildren, location.user)
    submitExperienceFormData(experienceFormChildren, location.user)
}


// Candidate info form
function submitQualificationFormData(data, user) {
    let formData = new FormData()
    let allFieldsValid = true

    data.forEach(async(item) => {

        const formIndex = parseInt(item.getAttribute('data-form-count'))
        const formID = parseInt(item.getAttribute('id'))

        const dataInputs = Array.from(item.querySelectorAll('p > *'))
        .filter((ele) => ele.name)

        dataInputs.push(resumeInput)

        dataInputs.forEach((input) => {
            let fieldError = null

            if (input.name !== 'resume') {
                fieldError = input.previousElementSibling.previousElementSibling
            }

            if (!input.value && input.name !== 'resume') {
                fieldError.style.display = 'grid'
                allFieldsValid = false
                formData = new FormData()

                candidateProfileButtonText.style.display = 'flex'
                candidateFormButtonSpinner.style.display = 'none'
            }
            else {
                if (fieldError) {
                    fieldError.style.display = 'none'
                }
            }

            
            if (input.name === 'resume') {
                formData.append(input.name, input.files[0])
            }
            else {
                formData.append(input.name, input.value)
            }
        })

        if (allFieldsValid) {
            formData.append('user', user)

            if (formID) {
                formData.append('id', formID)
            }

            const value = await registerCandidate(formData, 'qualification', item, formIndex)
            formData = new FormData()
        }
    })
}

// Candidate Education
function submitEducationFormData(data, user) {
    let formData = new FormData()
    let allFieldsValid = true

    data.forEach(async(item) => {
        const formIndex = parseInt(item.getAttribute('data-form-count'))
        const formID = item?.getAttribute('id') && parseInt(item.getAttribute('id')) || null

        formData = new FormData()
    
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
                formData.append(input.name, input.value)
            }
        })

        if (formID) {
            formData.append('id', formID)
        }

        if (allFieldsValid) {
            formData.append('user', user)
            const value = await registerCandidate(formData, 'education', item, formIndex)
        }
    })
}

// Candidate Experience
function submitExperienceFormData(data, user) {
    let formData = new FormData()
    let allFieldsValid = true
   
    data.forEach(async(item) => {
        const formIndex = parseInt(item.getAttribute('data-form-count'))
        const formID = parseInt(item.getAttribute('id'))

        formData = new FormData()
        
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
                formData.append(input.name, input.value)
            }
        })

        if (formID) {
            formData.append('id', formID)
        }

        if (allFieldsValid) {
            formData.append('user', user)
            const value = await registerCandidate(formData, 'experience', item, formIndex)
        }
    })
}


async function registerCandidate(formData, type, item, formIndex) {
    const url = `${window.location.origin}/candidates/add/career/detail/?type=${type}`
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
        
        if (data?.data_type === 'qualification') {
            submitChildForms()
        }
        
        if (data?.warning || data?.error) {
            handleFormErrorAndWarning(data)
        }
        else {
            saveObjectIDs(data, item)

            if (!formsSent[formIndex]) {
                formsSent[formIndex] = true
            }
        }

        const allSubmitted = checkAllFormsSubmitted()
        
        // if (allSubmitted) {
        //     window.location.href = `${window.location.origin}/profile/`
        // }
       
        return data
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

    if (data?.qualification_id) {
        if(!form_ids.qualification.includes(parseInt(data.qualification_id))) {
            form_ids.qualification.push(data.qualification_id)
        }
        item.setAttribute('id', data.qualification_id)
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


async function fetchPreviousFormData() {
    const {qualification, education, experience} = JSON.parse(sessionStorage.getItem('form_ids'))
    const url = `${window.location.origin}/candidates/fetch/form-data/`
    const csrfToken = getCsrfToken('csrftoken')

    const body = {
        'qualification': qualification.length ? qualification : null,
        'education': education.length ? education : null,
        'experience': experience.length ? experience : null
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
    const {qualification, education, experience} = data 

    if (qualification) {
        formatQualificationInputTemplate(qualification)
    }

    if (education) {
        formatEducationInputTemplate(education)
    }
    if (experience) {
        formatExperienceInputTemplate(experience)
    }
}


function formatQualificationInputTemplate(qualification) {
    if (!Boolean(qualification.length)) {
        handleEmptyArray('qualification')
    }
    else {
        qualification.forEach((qua) => {
            formsCount ++
            formsSent[formsCount] = false
            const qualificationInputContainer = document.createElement('div')

            qualificationInputContainer.setAttribute('class', 'qualification-form candidate-form')
            qualificationInputContainer.setAttribute('data-form-count', `${formsCount}`)
            qualificationInputContainer.setAttribute('id', `${qua.id}`)

            const qualification = `
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_industry">Industry:</label>
                    <select name="industry" autofocus="" required=true id="id_industry">
                        <option value="" selected="">-------</option>
                        <option value="technology">Technology</option>
                        <option value="finance">Finance</option>
                        <option value="healthcare">Healthcare</option>
                        <option value="education">Education</option>
                        <option value="marketing &amp; advertising">Marketing &amp; Advertising</option>
                        <option value="engineering">Engineering</option>
                        <option value="manufacturing">Manufacturing</option>
                        <option value="retail &amp; sales">Retail &amp; Sales</option>
                        <option value="hospitality">Hospitality</option>
                        <option value="construction">Construction</option>
                        <option value="telecommunications">Telecommunications</option>
                        <option value="real estate">Real Estate</option>
                        <option value="nonprofit">Nonprofit</option>
                        <option value="food and beverage">Food and Beverage</option>
                        <option value="government">Government</option>
                        <option value="arts &amp; entertainment">Arts &amp; Entertainment</option>
                        <option value="other">Other</option>
                    </select>
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_job_title">Job title:</label>
                    <input type="text" name="job_title" maxlength="200" value="${qua.job_title}" required="" id="id_job_title">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_resume">Resume:</label>
                    <input type="file" name="resume" id="id_resume">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_skills">Skills:</label>
                    <input type="text" name="skills" value="${qua.skills}" maxlength="200" id="id_skills">
                </p>`

            qualificationInputContainer.innerHTML = qualification
            qualificationFormContainer.append(qualificationInputContainer)

            const option = Array.from(qualificationFormContainer.querySelectorAll('.qualification-form > p > select > option'))
            .find((element) => element.value == qua.industry.toLowerCase())

            option.value = qua.industry.toLowerCase()
            option.setAttribute('selected', 'selected')

            createCustomFileUplodInput()
            resumeInput = document.querySelector('#id_resume')
            resumeInput.setAttribute('onchange', 'handleResumeFileInput()')
        })
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
                    <input type="text" name="institution" value='${edu.institution}' maxlength="255" id="id_institution">
                </p>
                 <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_start_date">Start date:</label>
                    <input type="date" name="start_date" onkeydown="return false" value='${edu.start_date}' id="id_start_date">
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_completion_date">Completion date:</label>
                    <input type="date" name="completion_date" onkeydown="return false" value='${edu.completion_date}' id="id_completion_date">
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
                    <input type="date" name="start_date" onkeydown="return false" value='${ex.start_date}' id="id_start_date"> 
                </p>
                <p>
                    <span class="candidate-input-error-field">
                        This field is required.
                    </span>
                    <label for="id_end_date">End date:</label>
                    <input type="date" name="end_date" onkeydown="return false" value='${ex.end_date}' id="id_end_date">
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

    if (dataType === 'qualification') {
        div.setAttribute('class', 'qualification-form candidate-form')
        div.setAttribute('data-form-count', `${formsCount}`)
    }

    else if (dataType === 'education') {
        div.setAttribute('class', 'education-form candidate-form')
        div.setAttribute('data-form-count', `${formsCount}`)
    }

    else if (dataType === 'experience') {
        div.setAttribute('class', 'experience-form candidate-form')
        div.setAttribute('data-form-count', `${formsCount}`)
    }

    if (div.classList.contains('qualification-form')) {
        div.innerHTML = qualificationElements
        qualificationFormContainer.append(div)
    }
    else if (div.classList.contains('experience-form')) {
        div.innerHTML = experienceElements
        experienceFormContainer.append(div)
    }
    else if(div.classList.contains('education-form')) {
        div.innerHTML = educationElements
        educationFormContainer.append(div)
    }

    createCustomFileUplodInput()
    resumeInput = document.querySelector('#id_resume')
    resumeInput.setAttribute('onchange', 'handleResumeFileInput()')
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


function createCustomFileUplodInput() {
    const resumePath = JSON.parse(localStorage.getItem('resume'))

    const div = document.createElement('div')
    let a = null
    const newLabel = document.createElement('label')

    div.setAttribute('class', 'resume-input-wrapper')


    if (resumePath?.resume) {
        a = document.createElement('a')
        a.setAttribute('href', resumePath.resume)
        a.setAttribute('target', '_blank')
        a.setAttribute('class', 'resume-url')
        a.textContent = `Current: ${resumePath.resume.split('/').slice(-1)}`
    }

    newLabel.setAttribute('form', 'id_resume')
    newLabel.textContent = 'Resume:'

    const qualiForm = document.querySelector('.qualification-form')
    const pTags = Array.from(qualiForm.querySelectorAll('p'))
    const p2 = pTags[2]
    const p3 = pTags[3]

    const label = p2.querySelector('label')
    const input = p2.querySelector('input')

    label.textContent = 'Upload resume'
    label.removeAttribute('for')
    label.setAttribute('class', 'resume-input-wrapper-label')
    label.append(input)
    
    div.append(label)
    a && div.append(a)

    p2.innerHTML = ''
    p2.append(newLabel)
    p2.append(div)

    // candidate register form help text
    const span = document.createElement('span')
    const helpText = 'Skills must be separated by commas.'

    span.setAttribute('class', 'candidate-register-form-help-text')
   
    span.innerHTML = helpText
    p3.append(span)
}


function getCsrfToken(csrftoken) {
    const cookie = document.cookie.split(';')
    .find((item)=>item.startsWith(csrftoken))
    .split('=').slice(-1)[0].trim()
    
    return cookie || null
}

function handleResumeFileInput() {
    const resumeInputWrapperLabel = document.querySelector('.resume-input-wrapper-label')
    const resumeInputWrapper = document.querySelector('.resume-input-wrapper')
    const resumeUrl = document.querySelector('.resume-url')
    let selectedResume = document.querySelector('.selected-resume')

    const p = document.createElement('p')
    const value = resumeInput.value.split('\\').slice(-1)[0]

    const elements = `
        <span>Selected: ${value}</span>
        <i class='fas fa-close remove-selected-resume'></i>`

    p.style.overflow = 'hidden'
    p.style.whiteSpace = 'nowrap'
    p.style.textOverflow = 'ellipsis'
    p.style.color = 'var(--black-30)'
    p.style.display = 'flex'
    p.style.gap = '1rem'
    p.style.alignItems = 'center'

    p.setAttribute('class', 'selected-resume')

    if (value) {
        
        if (selectedResume) {
            selectedResume.remove()
        }
        p.innerHTML = elements
        resumeInputWrapper.insertBefore(p, resumeUrl)
    }

    const removeSelectedResume = document.querySelector('.remove-selected-resume')

    
    removeSelectedResume.addEventListener('click', (e) => {
        selectedResume = document.querySelector('.selected-resume')
        selectedResume.remove()
        resumeInput.remove()

        const input = document.createElement('input')
        input.setAttribute('type', 'file')
        input.setAttribute('name', 'resume')
        input.setAttribute('accept', 'img/*')
        input.setAttribute('id', 'id_resume')
        input.setAttribute('onchange', 'handleResumeFileInput()')
        
        resumeInputWrapperLabel.append(input)
        resumeInput = document.querySelector('#id_resume')
    })
}