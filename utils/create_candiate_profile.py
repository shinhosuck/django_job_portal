from candidates.models import (
    CandidateQualification,
    Education,
    Experience
)
from django.contrib.auth import get_user_model
User = get_user_model()

def create_or_update_qualification(data, resume, user, data_type):
    id = data.get('id')
    industry = data['industry']
    job_title = data['job_title']
    skills = data['skills']
    
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
        'resume': qualification.get_resume_url() or None,
        'message': 'success'
    }

    return context


def create_or_update_education(data, user, data_type):
    id = data.get('id')
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
        education.start_date = start_date 
        education.completion_date = completion_date
        education.save()

    else:
        education = Education.objects.create(
            major = major,
            degree = degree,
            institution = institution,
            start_date = start_date, 
            completion_date = completion_date
        )

        user = User.objects.get(username = user.username)
       
        try:
            qualification = user.profile.candidatequalification 
        except CandidateQualification.DoesNotExist:
            qualification = None 
 
        if qualification:
            if not education.qualification:
                education.qualification = qualification
                education.save()

    # print('DATA:',data)

    context = {
        'education_id':education.id, 
        'data_type': data_type, 
        'message': 'success'
    }

    return context


def create_or_update_experience(data, user, data_type):
    id = data.get('id')
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
        experience.save() 
    
    else:
        experience = Experience.objects.create(
            company_name = company_name,
            position = position,
            start_date = start_date,
            end_date = end_date
        )

        user = User.objects.get(username = user.username)

        try:
            qualification = user.profile.candidatequalification 
        except CandidateQualification.DoesNotExist:
            qualification = None 
 
        if qualification:
            if not experience.qualification:
                experience.qualification = qualification
                experience.save()

    context = {
        'experience_id': experience.id,
        'data_type': data_type,
        'message': 'success'
    }

    return context


def fetch_previous_form_data(qualification, education, experience):
    context = {
        'qualification': [],
        'education': [],
        'experience': []
    }

    if qualification:
        for index in qualification:
            try:
                instance = CandidateQualification.objects.get(id=index)
            except CandidateQualification.DoesNotExist:
                instance = None 
            
            if instance:
                obj = {
                    'id': instance.id,
                    'industry': instance.industry,
                    'job_title': instance.job_title,
                    'resume': instance.get_absolute_url(),
                    'skills': instance.skills,
                }

                context['qualification'].append(obj)

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
                    'start_date': instance.start_date,
                    'completion_date': instance.completion_date
                }

                context['education'].append(obj)
    print(context)
            
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
    qualification = None
    education = None 
    experience = None

    context = {
        'qualification': [],
        'education': [],
        'experience': []
    }

    try:
        qualification = user.profile.candidatequalification
    except CandidateQualification.DoesNotExist:
        qualification = None

    if qualification:
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
                'start_date': edu.start_date,
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