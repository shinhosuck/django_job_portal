const JobApplicationHeaders = Array.from(document.querySelectorAll(
    '.employer-dashboard-employer-job-applicants-header'
))

if (JobApplicationHeaders) {
    JobApplicationHeaders.forEach((header) => {
        const span = header.querySelector('span')
        const chevronBtn = header.querySelector('i')

        if (span.textContent !== 'No applicant') {
            header.addEventListener('click', (e) => {
                header.nextElementSibling.classList.toggle(
                    'show-employer-dashboard-employer-job-applicants'
                )
                
                if (header.nextElementSibling.classList.contains(
                    'show-employer-dashboard-employer-job-applicants')) {
                        chevronBtn.style.transform = 'rotate(180deg)'
                    }
                else {
                    chevronBtn.style.transform = 'rotate(0deg)'
                }
            })
        }
        else {
            header.style.cursor = 'auto'
        }
    })
}
