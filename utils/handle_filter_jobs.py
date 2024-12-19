def get_filter_jobs(jobs):
    job_list = []

    for job in jobs:
        job_obj = {
            'id': job.id,
            'employer_name': job.employer.employer_name,
            'employer_city': job.employer.city,
            'employer_state_or_province': job.employer.state_or_province,
            'employer_country': job.employer.country.code,
            'employer_zip_code_or_postal_code': job.employer.zip_code_or_postal_code,
            'industry': job.industry,
            'job_title': job.job_title,
            'job_type': job.job_type,
            'experience_level': job.experience_level,
            'work_location': job.work_location,
            'slug': job.slug,
            'payment_type': job.payment_type,
            'currency': job.currency.code,
            'salary': job.salary,
            'currency_code': job.currency_code,
            'job_description': job.job_description[0:50],
            'qualification': job.qualification[0:50],
            'applicants': job.applicants.count(),
            'created': job.created.strftime("%b %d %Y")
        }
        job_list.append(job_obj)

    return job_list