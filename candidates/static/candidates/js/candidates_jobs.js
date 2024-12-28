const jobsContainer = document.querySelector('.jobs')
const jobNavLinks = Array.from(document.querySelectorAll('.job-nav-link'))
const jobsMainContainer = document.querySelector('.jobs-container')
const loadMoreJobsBtn = document.querySelector('.jobs-load-more-btn')

window.addEventListener('DOMContentLoaded', handlePreviousData)


function handlePreviousData() {
    let url = localStorage.getItem('filter_url')
    loadJobNavs(url)
    
    let location = JSON.parse(localStorage.getItem('location'))

    if (url) {
        removeJobNavLinkClass()
    
        if (!location?.user) {
            const suggestedJob = jobNavLinks.
            find((nav) => nav.classList.contains('suggested-jobs'))

            suggestedJob && suggestedJob.classList.add('active-job-nav-link')
            suggestedJob && suggestedJob.nextElementSibling.classList.add('active-border-bottom')
            jobsMainContainer.scrollIntoView({behavior:"smooth"})

            url = suggestedJob && suggestedJob.href
            suggestedJob && localStorage.setItem('filter_url', url)
        }
        else {
            jobNavLinks.forEach((link) => {
                if (link.href === url) {
                    link.classList.add('active-job-nav-link')
                    link.nextElementSibling.classList.add('active-border-bottom')

                    jobsMainContainer.scrollIntoView({behavior:"smooth"})
                    fetchPreviousJobs(url)
                }
            })
        }
    }else {
        jobsMainContainer.scrollIntoView({behavior:"smooth"})
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


function loadJobNavs(url) {
    jobNavLinks.forEach((nav, index) => {
        if (!url) {
            if (index === 0) {
                nav.classList.add('active-job-nav-link')
                nav.nextElementSibling.classList.add('active-border-bottom')
            }
        }
        nav.addEventListener('click', handleJobNavClickEvent)
    })
}


function removeJobNavLinkClass() {
    jobNavLinks.forEach((nav) => {
        if (nav.classList.contains('active-job-nav-link')) {
            nav.classList.remove('active-job-nav-link')
            nav.nextElementSibling.classList.remove('active-border-bottom')
        }
    })
}


async function handleJobNavClickEvent(e) {
    e.preventDefault()
    removeJobNavLinkClass()
    e.currentTarget.classList.add('active-job-nav-link')
    e.currentTarget.nextElementSibling.classList.add('active-border-bottom')
    
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
            <p class='jobs-do-not-exist'>
                <span>You don't have any "${data.q_param.split('_').join(' ')}".</span>
                <i class="far fa-frown"></i>
            </p>
        `

        div.innerHTML = element 
        jobsContainer.innerHTML = ''
        jobsContainer.append(div)
        jobsContainer.style.height = '80svh'
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
                        <a href="" class="job-employer-name">${job.employer_name}</a>
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
                        ${job.currency_code}${job.salary.split('.')[0]}/${job.payment_type}
                    </p>
                    <div class="job-description-wrapper">
                        <h4>Job Description</h4>
                        <p>${job.job_description} ...</p>
                    </div>
                    <div class="job-qualification-wrapper">
                        <h4>Qualification</h4>
                        <p>${job.qualification} ...</p>
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