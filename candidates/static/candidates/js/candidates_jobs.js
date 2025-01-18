const jobsContainer = document.querySelector('.jobs')
const jobDashboardNavLinks = Array.from(document.querySelectorAll('.job-nav-link'))
const jobsMainContainer = document.querySelector('.jobs-container')
const loadMoreJobsBtn = document.querySelector('.jobs-load-more-btn')
const jobsNoMatchingJobs = document.querySelector('.jobs-no-matching-jobs')
const jobsNoMatchingJobsMessageCloseBtn = document.querySelector(
    '.jobs-no-matching-jobs-message-close-btn')

window.addEventListener('DOMContentLoaded', handlePreviousData)

// this run on initial load and every reload
function handlePreviousData() {
    const jobsExist = localStorage.getItem('jobs_exist')
    let url = localStorage.getItem('filter_url')

    if(!localStorage.getItem('filter_url')) {
        localStorage.setItem('filter_url', `${window.location.href}?q=suggested_jobs`)
    }
   
    // suggested jobs, save jobs, and applied jobs
    addClickEventsToJobsNavs(url)
    
    let location = JSON.parse(sessionStorage.getItem('location'))

    if (url) {
        // remove current active state from either:
        // Suggested Jobs, Saved Jobs or Applied Jobs
        removeActiveJobNavLinkClass()

        if (!location?.user) {
            // gets triggered if location data do not contain user.
            // sets the 'Suggested Jobs' active status.
            const suggestedJob = jobDashboardNavLinks.find((nav) => nav.classList.contains('suggested-jobs'))

            suggestedJob && suggestedJob.classList.add('active-job-nav-link')
            suggestedJob && suggestedJob.nextElementSibling.classList.add('active-border-bottom')

            // resets the url with "Suggested Jobs" href.
            url = suggestedJob && suggestedJob.href

            // sets the localStorage with filter url data with the new url
            suggestedJob && localStorage.setItem('filter_url', url)
        }
        else {
            jobDashboardNavLinks.forEach((link) => {
                if (link.href === url) {
                    link.classList.add('active-job-nav-link')
                    link.nextElementSibling.classList.add('active-border-bottom')

                    if (jobsNoMatchingJobs && !link.classList.contains('suggested-jobs')){
                        jobsNoMatchingJobs.style.display = 'none'
                    }

                    // if location?.user, fetch previous data
                    // probaly on page refresh.
                    fetchPreviousJobs(url)
                }
            })
        }
    }
    jobsMainContainer.scrollIntoView({behavior:"smooth"})
    
    if (jobsExist === 'None') {
        if(loadMoreJobsBtn) {
            loadMoreJobsBtn.parentElement.style.display = 'none'
        }
    }
}


async function fetchPreviousJobs(url) {
    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()

        if (resp.ok) {
            createHtmlElements(data)

            let index = null
            let pagination = null

            if (data?.paginate?.job_paginate) {
                index = data.paginate.job_paginate 
                pagination = {jobPaginate:index}
            }
            if(data?.paginate?.suggested_job_paginate) {
                index = data.paginate.suggested_job_paginate 
                pagination = {suggestedJobPaginate:index}
            }
            if(data?.paginate?.applied_job_paginate) {
                index = data.paginate.applied_job_paginate 
                pagination = {appliedJobPaginate:index}
            }
            if(data?.paginate?.saved_job_paginate) {
                index = data.paginate.saved_job_paginate 
                pagination = {savedJobPaginate:index}
            }

            localStorage.setItem('paginate', JSON.stringify(pagination))
        }

    } catch (error) {
        console.log(error.message)
    }
}

// Attach click events to "Suggested Jobs, Saved Jobs, Applied Jobs"
function addClickEventsToJobsNavs(url) {
    jobDashboardNavLinks.forEach((nav, index) => {
        if (!url) {
            if (index === 0) {
                nav.classList.add('active-job-nav-link')
                nav.nextElementSibling.classList.add('active-border-bottom')
            }
        }
        nav.addEventListener('click', handleJobNavClickEvent)
    })
}


function removeActiveJobNavLinkClass() {
    jobDashboardNavLinks.forEach((nav) => {
        if (nav.classList.contains('active-job-nav-link')) {
            nav.classList.remove('active-job-nav-link')
            nav.nextElementSibling.classList.remove('active-border-bottom')
        }
    })
}

// fetch data based off 'Suggested Jobs, Saved Jobs, or Applied Jobs'
async function handleJobNavClickEvent(e) {
    e.preventDefault()
    removeActiveJobNavLinkClass()
    e.currentTarget.classList.add('active-job-nav-link')
    e.currentTarget.nextElementSibling.classList.add('active-border-bottom')

    jobsNoMatchingJobs && removeNoMatchingJobsMessage()
    
    localStorage.setItem('filter_url', e.currentTarget.href)

    const url = localStorage.getItem('filter_url')

    try {
        const resp = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()
        createHtmlElements(data)

        if (loadMoreJobsBtn.disabled === true) {
            loadMoreJobsBtn.disabled = false
            loadMoreJobsBtn.textContent = 'Load More'
            loadMoreJobsBtn.style.background = 'var(--green-30)'
        }
       
        // Set pagination starting index
        if(data?.paginate?.job_paginate) {
            localStorage.setItem('paginate', JSON.stringify({
                jobPaginate:data.paginate.job_paginate
            }))
        }
        if(data?.paginate?.applied_job_paginate) {
            localStorage.setItem('paginate', JSON.stringify({
                appliedJobPaginate:data.paginate.applied_job_paginate
            }))
        }
        if(data?.paginate.saved_job_paginate) {
            localStorage.setItem('paginate', JSON.stringify({
                savedJobPaginate:data.paginate.saved_job_paginate
            }))
        }
    } catch (error) {
        console.log(error.message)
    }
}

 
function createHtmlElements(data) {
    let div = document.createElement('div')
    div.setAttribute('class', 'job')

    if (data?.jobs === 'No jobs') {
        div.classList.add('job-no-job')
        const element = `
           
            <div class='jobs-do-not-exist-container'>
                <p class='jobs-do-not-exist' style="font-weight:500;color:var(--black-40);font-size:1.1rem">
                    You don't have any "${data.q_param.split('_').join(' ')}"!
                </p>
            </div>
        `

        div.innerHTML = element 
        jobsContainer.innerHTML = ''
        jobsContainer.append(div)
        jobsContainer.style.minHeight = '80svh'
    }
    else {
        jobsContainer.innerHTML = ''
        data.jobs.forEach((job) => {
            const element = `
                <div class="job-contents">
                    <div class="job-tags">
                        <a href="" class="job-industry">${job.industry}</a>
                        <a href="" class="job-job-type">${job.job_type}</a>
                        <a href="" class="job-work-location">${job.work_location}</a>
                    </div>
                    <div class="job-title-container">
                        <h3 class="job-title-header">${job.job_title}</h3>
                        <p class="job-created">Posted ${job.created}</p>
                    </div>
                    <div class="job-employer-address">
                        <p class="job-employer-name">${job.employer_name}</p>
                        <p class="job-employer-city-state">
                            <span>${job.employer_city},</span>
                            <span>${job.employer_state_or_province}</span>
                        </p>
                        <p class="job-employer-country">
                            <span>${job.employer_country}</span>
                            <span>${job.employer_zip_code_or_postal_code}</span>
                        </p>
                    </div>
                    <p class="job-salary">
                        <span>${job.currency_code}${job.salary.split('.')[0]}</span>
                        <span>/</span>
                        <span>${job.payment_type}</span>
                    </p>
                    <div class="job-description-wrapper">
                        <h4>Job Description</h4>
                        <p>${job.job_description.length > 80 ? job.job_description.substring(0, 80) + '...':job.job_description}</p>
                    </div>
                    <div class="job-qualification-wrapper">
                        <h4>Qualification</h4>
                        <p>${job.qualification.length > 80 ? job.qualification.substring(0, 80) + '...':job.qualification}</p>
                    </div>
                </div>
                <a class="see-job-detail-btn" href="/employers/jobs/${job.slug}/detail/?redirect=/candidates/jobs/">Job Detail</a>
            `
            div.innerHTML = element
            jobsContainer.append(div)
            
            div = document.createElement('div')
            div.setAttribute('class', 'job')
        })
    }
}


function removeNoMatchingJobsMessage() {
    jobsNoMatchingJobs.remove()
}
jobsNoMatchingJobsMessageCloseBtn &&jobsNoMatchingJobsMessageCloseBtn
.addEventListener('click', removeNoMatchingJobsMessage)