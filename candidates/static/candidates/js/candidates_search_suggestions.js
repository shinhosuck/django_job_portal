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

window.addEventListener('DOMContentLoaded', getUserIP)

/* 
    -fetches user location from backend:
    - see django urls.py in back-end,
    - end point: /candidates/location/,
    - django views: fetch_user_location_view()
*/
async function getUserIP(params) {
    
    const url = `${window.location.origin}/candidates/location/`
    let location = JSON.parse(sessionStorage.getItem('location'))
    const locationFlags = Array.from(document.querySelectorAll('.location-flag'))

    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()

        if (resp.ok) {
            if (data?.user !== location?.user || !data?.user || 
                !location?.user || !location) {
                
                sessionStorage.setItem('location', JSON.stringify(data))
                location = JSON.parse(sessionStorage.getItem('location'))
            }

            const offset = 127397

            const flag = Array.from(location.country_code)
            .map((char)=>String.fromCodePoint(char.charCodeAt(0)+offset)).join('')

            locationFlags.forEach((item) => {
                item.innerHTML = `
                    <div>
                        <span>${flag}</span>
                        <span>
                            ${location.country_code}
                        </span>
                    </div>`
            })
        }
    } 
    catch (error) {
        console.log(error.message)
    }
    getSuggestions(params)
}

/*
    - This async function gets called on window load.
    - Fetches suggestions from the back-end
    - Calls "handleSuggestionsAndCitiesData()" function 
        to create suggestions elements
*/
async function getSuggestions(params) {
    
    let url = `${window.location.origin}/candidates/search-form/suggestions/`

    if (params.type == 'query') {
        const data = `?${params.name}=${params.value}`
        url = `${url}${data}`
    }
    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()
 
        if (resp.ok) {
            handleSuggestionsAndCitiesData(data)
        }
    } 
    catch (error) {
        console.log(error.message, error.type)
    }
}

/*
    - Attaches eventListeners to the inputs on load.
    - Loops through "events" array.
    - Appropriate event is added to the form input.
    - removes previous input focus and suggestion container.
*/
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
                currentItem.nextElementSibling.nextElementSibling?.classList.add('show-suggestions')
            })
        }else {
            // if event is "keyup", this function gets called
            handleKeyUpEvent(eventType)
        }
    })
})


/*
    - This function gets called from "getSuggestions()"
    - Destructures the data and calls appropriate functions
*/
function handleSuggestionsAndCitiesData(data) {
    const { 
        search,
        searched_location,
        cities_suggestions, 
        search_suggestions, 
        city, state_or_province } = data

    const searchSuggestion = search_suggestions && 
        Boolean(search_suggestions.length) && 
        createSearchSuggestion(search_suggestions, search)
    
    const citiesSuggestion = cities_suggestions && 
        Boolean(cities_suggestions.length) && 
        createCitiesSuggestion(cities_suggestions, city, state_or_province, searched_location)
    
    // searchSuggestion or citiesSuggestion return true,
    // this block will run
    if (citiesSuggestion || searchSuggestion) {
        const closeSuggestionBtns = document.querySelectorAll('.close-suggestions')
        const suggestions = Array.from(document.querySelectorAll('.suggestion'))

        handleSuggestionClickEvent(suggestions)
        handleCloseSuggestionsBtn(closeSuggestionBtns)

    }
}

/*
    - This function gets called from "handleSuggestionsAndCitiesData".
    - Creates keyword/suggestion elements.
    - Appends suggestions elements to "searchInputRow".
*/
function createSearchSuggestion(search_suggestions, search) {
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
        search && keywordsSuggestion.classList.add('show-suggestions')
    }
    
    searchInputRow.append(keywordsSuggestion)

    return true
}


/*
    - This function gets called from "handleSuggestionsAndCitiesData".
    - Creates cities suggestion elements.
    - Appends cities elements to "citiesInputRow".
*/
function createCitiesSuggestion(cities_suggestions, city, state_or_province, searched_location) {
    const citiesSuggestions = document.createElement('div')
    citiesSuggestions.setAttribute('class', 'cities-suggestions-container')

    const button = document.createElement('button')
    button.setAttribute('type', 'button')
    button.setAttribute('class', 'close-suggestions')

    const i = document.createElement('i')
    i.setAttribute('class', 'fas fa-close')

    button.append(i)
    citiesSuggestions.append(button)

    cities_suggestions.forEach((suggested_city) => {
        const span = document.createElement('span')
        span.setAttribute('class', 'suggestion')

        const textNode = document.createTextNode(suggested_city)
        span.appendChild(textNode)

        citiesSuggestions.appendChild(span)
    })

    const citiesSuggestionContainer = citiesInputRow.querySelector(
        '.cities-suggestions-container'
    )

    if (citiesSuggestionContainer) {
        citiesSuggestionContainer.remove()
        searched_location && citiesSuggestions.classList.add('show-suggestions')
    }

    citiesInputRow.append(citiesSuggestions)

    return true
}


/*
    - This function gets called from "handleSuggestionsAndCitiesData"
    - Adds click events to suggetion elements
    - Suggestion on click, adds suggestion to input value
*/
function handleSuggestionClickEvent(suggestions) {
    suggestions.forEach((suggestion) => {
        suggestion.addEventListener('click', (e) => {
            
            const parent = e.currentTarget.parentElement
            const previousSibling = parent.previousElementSibling.previousElementSibling

            previousSibling.value = e.currentTarget.textContent

            parent.classList.remove('show-suggestions')
            parent.previousElementSibling.style.display = 'flex'
        })
    })
}


/*
    - This function gets called from "handleSuggestionsAndCitiesData".
    - Adds click event to "remove suggesion button".
    - Button on click, removes the suggestions.
*/
function handleCloseSuggestionsBtn(closeSuggestionBtns) {
    closeSuggestionBtns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.currentTarget.parentElement.classList.remove('show-suggestions')
        })
    })
}

/*
    - Adds "keyup" event to form input
    - Implemented "debounce" functionality
        to reduce excessive API calls.
*/
function handleKeyUpEvent(eventType) {
    function wrapper() {
        let timeoutID;

        return (e) => {
            clearTimeout(timeoutID)
            const {name, value} = e.target

            timeoutID = setTimeout(() => {
                if (value) {
                    getSuggestions({name:name, value:value, type:'query'})
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
        input.addEventListener(eventType, wrapper())
    })
}


/*
    - click event that listens for button 
        click within the search and city input.
    - on click, clears out the text in the input.
    - also removes suggestion container
*/
clearTextBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const previousSibling = e.currentTarget.previousElementSibling
        previousSibling.value = ''
        e.currentTarget.style.display = 'none'
        e.currentTarget.nextElementSibling?.classList.remove('show-suggestions')
    })
})


/*
    - window listens for target which is not within search form
    - if not within search form, input focus 
        and suggestion container get removed
*/
window.addEventListener('click', (e) => {
    if (searchForm && !searchForm.contains(e.target)) {
        inputRows.forEach((row) => {
            row.classList.remove('row-focus')
            row.lastElementChild.classList.remove('show-suggestions')
        })
    }
})

