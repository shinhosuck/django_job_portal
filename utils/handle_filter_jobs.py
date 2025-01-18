from django.db.models import Q
from employers.models import Job


def get_filter_jobs(jobs):
    job_list = []

    for job in jobs:
        job_obj = {
            'id': job.id,
            'employer_url': job.employer.get_absolute_url(),
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
            'job_description': job.job_description,
            'qualification': job.qualification,
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
                Q(employer__country__iexact=country, job_title__iexact=quali.job_title) | 
                Q(employer__city__iexact=city, job_title__iexact=quali.job_title))
            
            if not filter_jobs:
                filter_jobs = jobs.filter(
                    Q(employer__country__iexact=country) | 
                    Q(employer__city__iexact=city))
                if filter_jobs:
                    message = '''
                    Sorry! Based on your job title, there aren't any jobs available, 
                    but you might like these alternative jobs.
                    '''
                else:
                    message = '''
                    Sorry! Based on your location, there aren't any jobs available.
                    Please try using different location.
                    '''
    else:
        filter_jobs = jobs.filter(
            Q(employer__country__iexact=country) | 
            Q(employer__city__iexact=city))
        
        if not filter_jobs:
            message = '''
                    Sorry! Based on your location, there aren't any jobs available.
                    Please try using different location.
                    '''
    return filter_jobs, message


def search_filter_job(search_query, search_location, user_location):
    country = user_location.get('country_code')

    # User queries
    searches = [i for i in search_query.replace(' ', ',').split(',') if i]
    locations = [i for i in search_location.replace(' ', ',').split(',') if i]

    # Fields
    employer_fields = ['employer__city', 'employer__state_or_province']
    job_fields = ['job_title', 'industry']

    jobs = None
    
    for location in locations:
        for field in employer_fields:
            filtered_by_location = Job.objects.filter(iexact_or_icontains(field, location))
           
            if filtered_by_location:
                for search in searches:
                    for field in job_fields:
                        filtered_jobs = filtered_by_location.filter(iexact_or_icontains(field, search))
                       
                        if filtered_jobs:
                            if country:
                                filtered_by_country = filtered_jobs.filter(currency__iexact=country)
                          
                                if not jobs:
                                    jobs = filtered_by_country
                                else:
                                    jobs = jobs.union(filtered_by_country)
    return jobs


def iexact_or_icontains(field, value):
        return Q(**{f'{field}__iexact':value}) | Q(**{f'{field}__icontains':value})


def convert_queryset_to_json_data(context):
    jobs_json = []

    for job in context['jobs']:
        jobs_json.append(
            {
                'id': job.id,
                'employer_id': job.employer.id,
                'employer_url': job.employer.get_absolute_url(),
                'employer_name': job.employer.employer_name,
                'employer_city': job.employer.city,
                'employer_state_or_province': job.employer.state_or_province,
                'industry': job.industry,
                'job_title': job.job_title,
                'experience_level': job.experience_level,
                'work_location': job.work_location,
                'slug': job.slug,
                'payment_type': job.payment_type,
                'currency': job.currency.code,
                'salary': str(job.salary),
                'currency_code': job.currency_code,
                'job_description': job.job_description,
                'qualification': job.qualification,
                'created': job.created.strftime("%b %d %Y")
            }
        )
    context['jobs'] = jobs_json

    return context