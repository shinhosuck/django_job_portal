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


def filter_jobs_by_user_location(country_code, state, city, jobs, quali):
    filter_jobs = None
    message = None
    
    if quali and quali.job_title:
        filter_jobs = jobs.filter(create_q_objects(country_code, state, city, 4, quali))
       
        if not filter_jobs:
            filter_jobs = jobs.filter(create_q_objects(country_code, state, city, 3, quali))
           
            if not filter_jobs:
                filter_jobs = jobs.filter(Q(employer__country__iexact=country_code))
                message = '''
                Based on your job title and state/province or city, we could\'t 
                find any jobs tailered for you. How about these alternative jobs?'''
                
                if not filtered_qs:
                    warning_message = '''
                    Based on your country, state/province or city, we could\'t find any jobs.'''
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
            warning_message = '''
            Based on your state/province or city, we could\'t 
            find any jobs tailered for you. How about these alternative jobs?'''
            
            if not filtered_qs:
                warning_message = '''
                Based on your country, state/province or city, we could\'t find any jobs.'''
        
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