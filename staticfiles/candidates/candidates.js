// Get user location
async function get_user_ip() {
    const url = `${window.location.origin}/candidates/location/`

    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()
        console.log(data)
        if (resp.ok) {
            sessionStorage.setItem('location', JSON.stringify(data))
        }
    } 
    catch (error) {
        console.log(error.message)
    }
}
get_user_ip()


const searchSubmitBtn = document.querySelector('.search-form-submit-btn')
const searchContainerForm = document.querySelector('.search-form-container')
const searchForm = document.querySelector('.search-form')
const searchInputRow = document.querySelector('.search-input-row')
const citiesInputRow = document.querySelector('.cities-input-row')
const clearTextBtns = Array.from(
    document.querySelectorAll('.search-form-clear-btn')
)
const inputRows = Array.from(
    document.querySelectorAll('.search-form-input-row')
)
const inputs = Array.from(
    document.querySelectorAll('.search-form-input')
)

const events = ['click', 'keyup']

window.addEventListener('DOMContentLoaded', getSuggestions)


async function getSuggestions(params) {
    if (searchSubmitBtn) {
        searchSubmitBtn.disabled = true
    }

    let path = '/candidates/search-form/suggestions/'

    if (params.type == 'query') {
        const data = `?${params.name}=${params.value}`
        path = `${path}${data}`
    }

    try {
        const resp = await fetch(path)
        const data = await resp.json()

        if (resp.ok) {
            createSuggestionElements(data)
        }
    } 
    catch (error) {
        console.log(error.message, error.type)
    }
}

inputs.forEach((input) => {
    events.forEach((eventType) => {
        if (eventType === 'click') {
            input.addEventListener(eventType, (e) => {

                inputRows.forEach((row) => {
                    row.classList.remove('row-focus')
                    row.lastElementChild.classList.remove('show-suggestions')
                })

                const currentItem = e.currentTarget
                currentItem.parentElement.classList.add('row-focus')
                currentItem.nextElementSibling.nextElementSibling.classList.add('show-suggestions')
            })
        }else {
            handleKeyUpEvent(eventType)
        }
    })
})


clearTextBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const previousSibling = e.currentTarget.previousElementSibling
        previousSibling.value = ''
        e.currentTarget.style.display = 'none'
        e.currentTarget.nextElementSibling.classList.remove('show-suggestions')
        searchSubmitBtn.disabled = true
    })
})


window.addEventListener('click', (e) => {
    if (searchForm && !searchForm.contains(e.target)) {
        inputRows.forEach((row) => {
            row.classList.remove('row-focus')
            row.lastElementChild.classList.remove('show-suggestions')
        })
    }
})


function createSuggestionElements(data) {
    const { cities_suggestions, search_suggestions} = data

    const searchSuggestion = search_suggestions && 
        Boolean(search_suggestions.length) && 
        createSearchSuggestion(search_suggestions)
        
    const citiesSuggestion = cities_suggestions && 
        Boolean(cities_suggestions.length) && 
        createCitiesSuggestion(cities_suggestions)
    
    if (citiesSuggestion || searchSuggestion) {
        const closeSuggestionBtns = document.querySelectorAll('.close-suggestions')
        const suggestions = Array.from(document.querySelectorAll('.suggestion'))

        handleSuggestionClickEvent(suggestions)
        handleCloseSuggestionsBtn(closeSuggestionBtns)

    }
}

function createSearchSuggestion(search_suggestions) {
    const keywordsSuggestion = document.createElement('div')
    keywordsSuggestion.setAttribute('class', 'searches-suggestions-container')

    const button = document.createElement('button')
    button.setAttribute('type', 'button')
    button.setAttribute('class', 'close-suggestions')

    const i = document.createElement('i')
    i.setAttribute('class', 'fas fa-close')

    button.append(i)
    keywordsSuggestion.append(button)

    search_suggestions.forEach((item) => {
        const span = document.createElement('span')
        span.setAttribute('class', 'suggestion')

        const textNode = document.createTextNode(item)
        span.appendChild(textNode)

        keywordsSuggestion.appendChild(span)
    })

    const searchSuggestionContainer = searchInputRow.querySelector(
        '.searches-suggestions-container'
    )

    if (searchSuggestionContainer) {
        searchSuggestionContainer.remove()
        keywordsSuggestion.classList.add('show-suggestions')
    }
    
    searchInputRow.append(keywordsSuggestion)

    return true
}


function createCitiesSuggestion(cities_suggestions) {
    const citiesSuggestions = document.createElement('div')
    citiesSuggestions.setAttribute('class', 'cities-suggestions-container')

    const button = document.createElement('button')
    button.setAttribute('type', 'button')
    button.setAttribute('class', 'close-suggestions')

    const i = document.createElement('i')
    i.setAttribute('class', 'fas fa-close')

    button.append(i)
    citiesSuggestions.append(button)

    cities_suggestions.forEach((city) => {
        const span = document.createElement('span')
        span.setAttribute('class', 'suggestion')

        const textNode = document.createTextNode(city)
        span.appendChild(textNode)

        citiesSuggestions.appendChild(span)
    })

    const citiesSuggestionContainer = citiesInputRow.querySelector(
        '.cities-suggestions-container'
    )

    if (citiesSuggestionContainer) {
        citiesSuggestionContainer.remove()
        citiesSuggestions.classList.add('show-suggestions')
    }

    citiesInputRow.append(citiesSuggestions)

    return true
}


function handleSuggestionClickEvent(suggestions) {
    suggestions.forEach((suggestion) => {
        suggestion.addEventListener('click', (e) => {
            
            const parent = e.currentTarget.parentElement
            const previousSibling = parent.previousElementSibling.previousElementSibling

            previousSibling.value = e.currentTarget.textContent

            parent.classList.remove('show-suggestions')
            parent.previousElementSibling.style.display = 'flex'
            searchSubmitBtn.disabled = false
        })
    })
}


function handleCloseSuggestionsBtn(closeSuggestionBtns) {
    closeSuggestionBtns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.currentTarget.parentElement.classList.remove('show-suggestions')
        })
    })
}


function handleKeyUpEvent(eventType) {

    function getSearchFormInputData() {
        let timeoutID;

        return (e) => {
            clearTimeout(timeoutID)
            timeoutID = setTimeout(() => {
                const {name, value} = e.target

                if (value) {
                    getSuggestions({name:name, value:value, type:'query'})
                    searchSubmitBtn.disabled = false
                }

            }, 200);
            
            if (e.target.value) {
                e.target.nextElementSibling.style.display = 'flex'
            }
            else {
                e.target.nextElementSibling.style.display = 'none'
            }
        }
    }

    inputs.forEach((input) => {
        input.addEventListener(eventType, getSearchFormInputData())
    })
}




