from candidates.models import (
    Candidate,
    Education,
    Experience
)


def create_or_update_candidate_info(data, resume, user, profile, data_type):
    industry = data['industry']
    first_name = profile.first_name
    last_name = profile.last_name
    city = data['city']
    state_or_province = data['state_or_province']
    country = data['country']
    job_title = data['job_title']
    skills = data['skills']
    social_link = data['social_link']

    try:
        candidate = Candidate.objects.get(user=user)
    except Candidate.DoesNotExist:
        candidate = None
    
    if candidate:
        candidate.industry = industry
        candidate.first_name = first_name
        candidate.last_name = last_name
        candidate.city = city
        candidate.state_or_province = state_or_province
        candidate.country = country 
        candidate.job_title = job_title
        candidate.skills = skills
        candidate.social_link = social_link
        candidate.save()

    if not candidate:
        candidate = Candidate.objects.create(
            user = user,
            industry = industry,
            first_name = first_name,
            last_name = last_name,
            city = city,
            state_or_province = state_or_province,
            country = country,
            job_title = job_title,
            resume = resume,
            skills = skills,
            social_link = social_link
        )
    
    context = {
        'candidate_id': candidate.id,
        'data_type': data_type,
        'resume': candidate.resume and candidate.get_resume_url(),
        'message': 'success'
    }

    return context


def create_or_update_candidate_education(data, request, data_type):
    id = data.get('id')
    candidate = request.user.candidate
    major = data['major']
    degree = data['degree']
    institution = data['institution']
    completion_date = data['completion_date']

    try:
        instance = Education.objects.get(id=id)
    except Education.DoesNotExist:
        instance = None
    
    if instance:
        instance.major = major
        instance.degree = degree
        instance.institution = institution
        instance.completion_date = completion_date 
        instance.save()

    else:
        instance = Education.objects.create(
            candidate = candidate,
            major = major,
            degree = degree,
            institution = institution,
            completion_date = completion_date
        )

    context = {
        'education_id':instance.id, 
        'data_type': data_type, 
        'message': 'success'
    }

    return context


def create_or_update_candidate_experience(data, request, data_type):
    id = data.get('id')
    candidate = request.user.candidate
    company_name = data['company_name']
    position = data['position']
    start_date = data['start_date']
    end_date = data['end_date']

    try:
        instance = Experience.objects.get(id=id)
    except Experience.DoesNotExist:
        instance = None 


    if instance:
        instance.company_name = company_name
        instance.position = position
        instance.start_date = start_date
        instance.end_date = end_date 
    
    else:
        instance = Experience.objects.create(
            candidate = candidate,
            company_name = company_name,
            position = position,
            start_date = start_date,
            end_date = end_date
        )

    context = {
        'experience_id': instance.id,
        'data_type': data_type,
        'message': 'success'
    }

    return context


def fetch_previous_form_data(education, experience):
    context = {
        'education': [],
        'experience': []
    }

    if education:
        for index in education:
            try:
                instance = Education.objects.get(id=index)
            except Education.DoesNotExist:
                instance = None
            
            if instance:
                obj = {
                    'id': instance.id,
                    'major': instance.major,
                    'degree': instance.degree,
                    'institution': instance.institution,
                    'completion_date': instance.completion_date
                }

                context['education'].append(obj)
            
    if experience:
        for index in experience:
            try:
                instance = Experience.objects.get(id=index)
            except Experience.DoesNotExist:
                instance = None

            if instance:
                obj = {
                    'id': index,
                    'company_name': instance.company_name,
                    'position': instance.position,
                    'start_date': instance.start_date,
                    'end_date': instance.end_date
                }

                context['experience'].append(obj)

    return context


def prefetch_form_data(user):
    context = {
        'education': [],
        'experience': []
    }

    try:
        candidate = user.candidate
    except Candidate.DoesNotExist:
        candidate = None
    
    if candidate:
        education = Education.objects.filter(candidate=candidate)
        experience = Experience.objects.filter(candidate=candidate)

        for edu in education:
            obj = {
                'id': edu.id,
                'major': edu.major,
                'degree': edu.degree,
                'institution': edu.institution,
                'completion_date': edu.completion_date
            }
            context['education'].append(obj)

        for exp in experience:
            obj = {
                'id': exp.id,
                'company_name': exp.company_name,
                'position': exp.position,
                'position': exp.position,
                'start_date': exp.start_date,
                'end_date': exp.end_date
            }
            context['experience'].append(obj)

    return context