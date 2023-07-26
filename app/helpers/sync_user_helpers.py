from typing import TypeVar
from app.utils.user_utils import *
import numpy as np
import math, time
from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)



def get_education_score(user: user_account_type):
    tehsil_score = 0
    userdata = user.user_info[1]["formData"]["EducationScore"]
    for bachelors in userdata:
        if bachelors.get("bachelor") is not None:
            if bachelors['bachelor']['criterion']['criterion_type'] == 'her ikisi':
                lokal_test_weight = bachelors['bachelor']['criterion']['lokal_test']['answer_weight']
                muraciyyet = bachelors['bachelor']['criterion']['muraciyyet']
                if len(muraciyyet)>1:
                    for m in muraciyyet:
                        if m['muraciyyet_type'] == 'Atestat':            
                            atestat_weight = m['answer_weight']
                            print(atestat_weight)
                        elif m['muraciyyet_type'] == 'language':
                            m['language_type']
                                    
            break
    return 1
        
        


def get_experience_score(user: user_account_type):
        userdata = user.user_info[3]["formData"]["experiences"]
        experiance_score = 1
        if len(userdata)>0:
                workingform = {"Fiziki əmək":1, "Sənət":2, "Ali ixtisas":3, "Sahibkar":4}
                max_working_form_weight = 0
                profession_degree_weight = 0
                if len(userdata)>1:
                        max = 0
                        for data in userdata:
                                if workingform[data["workingActivityForm"]["answer"]]>max:
                                        max = workingform[data["workingActivityForm"]["answer"]]
                                        max_working_form_weight = data["workingActivityForm"]["answer_weight"]
                                        profession_degree_weight = data["degreeOfProfes"]["answer_weight"]
                                        difference = calculate_date_difference(data)

                        finnly_date = difference.days/365.25
                        finnly_date_weight = get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight
                else:
                        max_working_form_weight = userdata[0]["workingActivityForm"]["answer_weight"]
                        profession_degree_weight = userdata[0]["degreeOfProfes"]["answer_weight"]
                        difference = calculate_date_difference(userdata[0])
                        finnly_date = difference.days/365.25
                        finnly_date_weight = get_date_weight(finnly_date=finnly_date)
                        experiance_score = max_working_form_weight*profession_degree_weight* finnly_date_weight

                return experiance_score
        return experiance_score


def get_skills_score(user):

        userdata = user.user_info[4]["formData"]["specialSkills"]
        lst=[]
        heveskar_count = 0
        pesekar_count = 0

        for data in userdata:
                lst.append(data['talent_level'])
                if data['talent_level'] == 'heveskar':
                        heveskar_answer_weight = data['answer_weight']
                elif data['talent_level'] == 'pesekar':
                        pesekar_answer_weight = data['answer_weight']

        for value in lst:
                if value=='heveskar':
                        heveskar_count += 1
                elif value=='pesekar':
                        pesekar_count += 1

        formula_result = (heveskar_count**heveskar_answer_weight) * (pesekar_count**pesekar_answer_weight)
        return formula_result

def get_language_score(user):

        userdata = user.user_info[5]["formData"]["languageSkills"]
        total_language_weight = 1
        if len(userdata) > 0:
                for data in userdata:
                        total_language_weight *= data['answer_weight']
                return total_language_weight
        
        return total_language_weight