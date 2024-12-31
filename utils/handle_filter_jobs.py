from django.db.models import Q


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


def filter_jobs_by_user_location(country, city, jobs, quali):
    filter_jobs = None
    message = None
    
    if quali and quali.job_title:
        filter_jobs = jobs.filter(Q(
                employer__country__iexact=country, 
                employer__city__iexact=city, 
                job_title__iexact=quali.job_title
            ))
        
        if not filter_jobs:
            filter_jobs = jobs.filter(
                Q(employer__country__iexact=country,job_title__iexact=quali.job_title) | 
                Q(employer__city__iexact=city,job_title__iexact=quali.job_title))
            
            if not filter_jobs:
                filter_jobs = jobs.filter(
                    Q(employer__country__iexact=country) | 
                    Q(employer__city__iexact=city))
                if filter_jobs:
                    message = '''
                    Based on your job title, there are no jobs available, 
                    but you might like these alternative jobs.
                    '''
                else:
                    message = '''
                    Based on your location and  job title, there are no jobs available.
                    Please enter a job tititle and location for jobs.
                    '''
    else:
        filter_jobs = jobs.filter(
            Q(employer__country__iexact=country) | 
            Q(employer__city__iexact=city))
    
    return filter_jobs, message