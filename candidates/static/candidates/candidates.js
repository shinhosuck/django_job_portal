
const jobSearchFormContainer = document.querySelector('.job-search-form-container')
const jobSearchForm = document.querySelector('.job-search-form')
const searchInput = document.querySelector('.search-input')
const searchFormCloseIcon = document.querySelector('.search-form-close-icon')


if (jobSearchFormContainer) {

    jobSearchForm.addEventListener('click', (e) => {
        jobSearchForm.style.outline = '3px solid var(--green-60)'
    })

    searchInput.addEventListener('keyup', (e) => {
        if (!searchInput.value) {
            searchFormCloseIcon.style.display = 'none'
        }
        else {
            searchFormCloseIcon.style.display = 'flex'
        }
    })

    searchFormCloseIcon.addEventListener('click', () => {
        jobSearchForm.reset()
        searchFormCloseIcon.style.display = 'none'
    })

    window.addEventListener('click', (e) => {
        if (!jobSearchFormContainer.contains(e.target)) {
            jobSearchForm.style.outline = 'none'
        }
    })

}