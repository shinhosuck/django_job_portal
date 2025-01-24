from django.db.models import Q
from employers.models import Job
from textwrap import dedent

def get_filter_jobs(jobs):
    job_list = []

    for job in jobs:
        job_obj = {
            'id': job.id,
            'employer_url': job.employer.get_absolute_url(),
            'employer_logo': job.employer.logo.url,
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


def filter_jobs_by_user_location(country_code, state, city, jobs, quali):
    filter_jobs = None
    message = None
    
    if quali and quali.job_title:
        filter_jobs = jobs.filter(create_q_objects(country_code, state, city, 4, quali))
       
        if not filter_jobs:
            filter_jobs = jobs.filter(create_q_objects(country_code, state, city, 3, quali))
           
            if not filter_jobs:
                filter_jobs = jobs.filter(Q(employer__country__iexact=country_code))
                message = dedent('''Based on your "job title and state/province or city," 
                        we couldn't find any jobs tailored for you. But we found jobs that you might like.''')
                
                if not filter_jobs:
                    message = dedent('''Based on your "country, state/province or city", 
                        we couldn't find any jobs.''')
    else:
        filtered_qs, warning_message = filter_jobs_without_qualifiction(country_code, state, city, jobs, quali)
        
        filter_jobs = filtered_qs
        message = warning_message

    return filter_jobs, message


def filter_jobs_without_qualifiction(country_code, state, city, jobs, quali):
    filtered_qs = None
    warning_message = None 

    filtered_qs = jobs.filter(create_q_objects(country_code, state, city, 3, quali))

    if not filtered_qs:
        filtered_qs = jobs.filter(create_q_objects(country_code, state, city, 2, quali))
    
        if not filtered_qs:
            filtered_qs = jobs.filter(Q(employer__country__iexact=country_code))
            warning_message = dedent('''Based on your "state/province or city," 
                    we couldn't find any jobs tailored for you. But we found jobs that you might like.''')
            
            if not filtered_qs:
                warning_message = dedent('''
                Based on your "country, state/province or city", we couldn't find any jobs.''')
        
    return filtered_qs, warning_message


def create_q_objects(country_code, state, city, num_of_args, quali):
    qs = None

    if quali:
        if num_of_args == 4:
            qs = Q(employer__country__iexact=country_code, employer__state_or_province__iexact=state, \
                   employer__city__iexact=city, job_title__iexact=quali.job_title)
        elif num_of_args == 3:
            qs = (Q(employer__country__iexact=country_code, \
                    employer__city__iexact=city, job_title__iexact=quali.job_title) | 
                Q(employer__country__iexact=country_code, \
                  employer__state_or_province__iexact=state, job_title__iexact=quali.job_title))
    else:
        if num_of_args == 3:
            qs = Q(employer__country__iexact=country_code, \
                employer__state_or_province__iexact=state, \
                employer__city__iexact=city)
            
        elif num_of_args == 2:
            qs = (Q(employer__country__iexact=country_code, employer__state_or_province__iexact=state) |
                Q(employer__country__iexact=country_code, employer__city__iexact=city))  
        
    return qs

def search_filter_job(search_query, search_location, user_location):
    country = user_location.get('country_code')

    # User queries
    searches = [i for i in search_query.replace(' ', ',').split(',') if i]
    locations = [i for i in search_location.replace(' ', ',').split(',') if i]

    # Fields
    employer_fields = ['employer__city', 'employer__state_or_province']
    job_fields = ['job_title', 'industry']

    filter_by_location = None 
    filter_by_keyword = None 
    jobs = None
    message = None
    
    for location in locations:
        for field in employer_fields:
            by_location = Job.objects.filter(iexact_or_icontains(field, location))
    
            if by_location:
                if not filter_by_location:
                    filter_by_location = by_location
                else:
                    filter_by_location = filter_by_location.union(by_location)

                for search in searches:
                    for field in job_fields:
                        by_keyword = by_location.filter(iexact_or_icontains(field, search))

                        if by_keyword:
                            filter_by_location = None

                            if not filter_by_keyword:
                                filter_by_keyword = by_keyword
                            else:
                                filter_by_keyword = filter_by_keyword.union(by_keyword)

                            by_country = by_keyword.filter(currency__iexact=country)

                            if by_country:
                                filter_by_keyword = None

                                if not jobs:
                                    jobs = by_country 
                                else:
                                    jobs = jobs.union(by_country)
    if jobs:
        message = dedent('We found jobs based on your "country, search keyword and location".')
    if not jobs and filter_by_keyword and not filter_by_location:
        message = dedent('We could only find jobs based on "search keyword and location".')
    if not jobs and not filter_by_keyword and filter_by_location:
        message = dedent('We could only find jobs based on your search "location".')
    if not jobs and not filter_by_keyword and not filter_by_location:
        message = dedent('We did not find any jobs based on your location.')

    return jobs or filter_by_keyword or filter_by_location, message


def iexact_or_icontains(field, value):
    iexact = {f'{field}__iexact':value}
    icontains = {f'{field}__icontains':value}

    return Q(**iexact)| Q(**icontains)


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