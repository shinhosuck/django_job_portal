from candidates.models import (
    CandidateQualification,
    Education,
    Experience
)


def create_or_update_qualification(data, resume, user, data_type):
    id = data.get('id')
    industry = data['industry']
    job_title = data['job_title']
    skills = data['skills']

    print(data_type)
    print(data)
    print(resume)


    try:
        qualification = CandidateQualification.\
            objects.get(profile__user=user, id=id)
    except CandidateQualification.DoesNotExist:
        qualification = None
    
    if qualification:
        qualification.industry = industry
        qualification.job_title = job_title
        qualification.skills = skills
        qualification.save()

        if resume:
            qualification.resume = resume
            qualification.save()

    elif not qualification:
        qualification = CandidateQualification.objects.create(
            profile = user.profile,
            industry = industry,
            job_title = job_title,
            resume = resume,
            skills = skills,
        )
    
    context = {
        'qualification_id': qualification.id,
        'data_type': data_type,
        'resume': qualification.resume and qualification.get_resume_url(),
        'message': 'success'
    }

    return context


def create_or_update_education(data, user, data_type):
    id = data.get('id')
    qualification = user.profile.candidate_qualification
    major = data['major']
    degree = data['degree']
    institution = data['institution']
    start_date = data['start_date']
    completion_date = data['completion_date']

    try:
        education = Education.objects.get(id=id)
    except Education.DoesNotExist:
        education = None
    
    if education:
        education.major = major
        education.degree = degree
        education.institution = institution
        education.completion_date = completion_date
        education.start_date = start_date 
        education.save()

    else:
        education = Education.objects.create(
            qualification = qualification,
            major = major,
            degree = degree,
            institution = institution,
            start_date = start_date, 
            completion_date = completion_date
        )

    context = {
        'education_id':education.id, 
        'data_type': data_type, 
        'message': 'success'
    }

    return context


def create_or_update_experience(data, user, data_type):
    id = data.get('id')
    qualification = user.profile.candidate_qualification
    company_name = data['company_name']
    position = data['position']
    start_date = data['start_date']
    end_date = data['end_date']

    try:
        experience = Experience.objects.get(id=id)
    except Experience.DoesNotExist:
        experience = None 


    if experience:
        experience.company_name = company_name
        experience.position = position
        experience.start_date = start_date
        experience.end_date = end_date 
    
    else:
        experience = Experience.objects.create(
            qualification = qualification,
            company_name = company_name,
            position = position,
            start_date = start_date,
            end_date = end_date
        )

    context = {
        'experience_id': experience.id,
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
        'qualification': [],
        'education': [],
        'experience': []
    }

    qualification = user.profile.candidatequalification
    education = Education.objects.filter(qualification=qualification)
    experience = Experience.objects.filter(qualification=qualification)

    if qualification:
        obj = {
            'id': qualification.id,
            'industry': qualification.industry,
            'job_title': qualification.job_title,
            'resume': qualification.get_resume_url(),
            'skills': qualification.skills
        }

        context['qualification'].append(obj)

    if education:
        for edu in education:
            obj = {
                'id': edu.id,
                'major': edu.major,
                'degree': edu.degree,
                'institution': edu.institution,
                'completion_date': edu.completion_date
            }
            context['education'].append(obj)

    if experience:
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