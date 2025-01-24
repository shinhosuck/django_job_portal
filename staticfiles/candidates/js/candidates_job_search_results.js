const jobSearchForm = document.querySelector('.search-form')
const searchLabel = document.querySelector('.search-label')
const locationLabel = document.querySelector('.location-label')
const searchInputs = Array.from(jobSearchForm.querySelectorAll('input'))
const jobSearchContainer = document.querySelector('.job-search-container')


window.addEventListener('DOMContentLoaded', handleFormSubmitBtn)

function handleFormSubmitBtn() {
    jobSearchForm.addEventListener('submit', (e) => {
        e.preventDefault()

        const searchFormInputError = Array.from(document.querySelectorAll('.search-form-input-error'))
        searchFormInputError.forEach((error) => {
            error && error.remove()
        })
        checkFormValid()
    })
    jobSearchContainer.scrollIntoView({'behavior':"smooth", 'block':'start'})
}

function checkFormValid() {
    let index = null
    
    searchInputs.forEach((input, element_index) => {
        index = element_index

        if (input.name === 'search') {
            searchInput = input
        }
        else if (input.name === 'location') {
            locationInput = input
        }
        checkFormInputValues(input, index)
    })
}

function checkFormInputValues(input, index) {
    let keyWords = ''
    let location = ''

    if (input.name === 'search') {
        keyWords = !input.value && 'Keyword field is required.'
    }
    else if (input.name === 'location') {
        location = !input.value && 'Location field is required.'
    }

    if (keyWords || location) {
        createErrorElement(keyWords, location, input)
    }

    if (searchInputs.length - 1 === index) {
        let input_valid = true
        let values = {}

        searchInputs.forEach((input) => {
            if (!input.value) {
                input_valid = false
                return null
            }
            else {
                values[input.name] = {value:input.value}
            }
        })
        if (input_valid) {
            submitSearchForm(values)
        }
    }
}


function createErrorElement(keyWords, location, input) {
    const span = document.createElement('span')
    const fontAwesome = document.createElement('i')
    const text = document.createTextNode(keyWords || location)

    span.addEventListener('click', (e)=> e.currentTarget.remove())

    span.setAttribute('class', 'search-form-input-error')
    fontAwesome.setAttribute('class', 'fas fa-close')

    fontAwesome.style.marginLeft = '1rem'

    span.append(text)
    span.append(fontAwesome)

    input.parentElement.insertBefore(span, keyWords?searchLabel:locationLabel)
}

async function submitSearchForm(values) {
    const {search, location} = values
    const origin = window.location.origin

    const url = `${origin}/candidates/jobs/search/?search=${search.value}&location=${location.value}`

    const resp = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const data = await resp.json()
    console.log(data)
}