const jobsWrapper = document.querySelector('.jobs')
const jobsLoadMoreBtn = document.querySelector('.jobs-load-more-btn')


jobsLoadMoreBtn && jobsLoadMoreBtn.addEventListener('click', (e) => {
    const pagination = JSON.parse(localStorage.getItem('paginate'))
    const jobsExist = localStorage.getItem('jobs_exist')
    setPagination(pagination)
})


async function setPagination(pagination) {
    const filterUrl = localStorage.getItem('filter_url')
    const type = Object.keys(pagination)[0]
    const value = pagination[type]

    const url = filterUrl && filterUrl + `&${type}=${value}`
    
    try {
        const resp = await fetch(url, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await resp.json()

        if (resp.ok) {
            if (data?.jobs_exist && data.jobs_exist === 'None') {
                jobsLoadMoreBtn.style.display = 'none'
            }

            data?.jobs && appendPaginateJobObject(data.jobs)

            pagination = JSON.parse(localStorage.getItem('paginate'))
            let index = null

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


function appendPaginateJobObject(jobs) {
    let div = document.createElement('div')
    div.setAttribute('class', 'job')

    jobs.forEach((job) => {
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
        jobsWrapper.append(div)

        div.scrollIntoView({behavior:'smooth', block:'end'})
        
        div = document.createElement('div')
        div.setAttribute('class', 'job')
    })
}