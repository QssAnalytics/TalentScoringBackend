import numpy as np
import math, time
from typing import TypeVar
from app.utils.user_utils import *

from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

def check(data, key):
        if data.get(key) is not None:
                if data[key] !={}:
                        return float(data[key]["answer_weight"])
        return 1

def get_education_score(user: user_account_type):
        user_info =  user.user_info
        work_activite_weight = check(data = user_info[0]["formData"], key = "curOccupation")
        education_weight = check(user_info[0]["formData"]["education"], key = "master")
        education_grand_weight = check(data = user_info[0]["formData"], key = "educationGrant")
        olimp_highest_weight = check(data = user_info[2]["formData"], key = "highestOlympiad")
        olimp_rank_weight = check(data = user_info[2]["formData"], key = "rankOlympiad")
        max_bachelor_weight = 1
        max_master_weight = 1
        max_phd_weight = 1
        userdata = user_info[1]["formData"]["EducationScore"]
        bachelor_weight_list = []
        master_weight_list = []
        phd_weight_list = []
        for edu in userdata:
                if edu.get("bachelor") is not None:
                        if edu["bachelor"] != {}:
                                bachelor_weight = get_bachelor_weight(edu)
                                bachelor_weight_list.append(bachelor_weight)
                if edu.get("master") is not None:
                        if edu["master"] != {}:
                                master_weight = get_master_weight(edu)
                                master_weight_list.append(master_weight)
                                
                if edu.get("phd") is not None:
                        if edu["phd"] != {}:
                                phd_weight = get_phd_weight(edu)
                                phd_weight_list.append(phd_weight)                           
        if bachelor_weight_list!=[]:
                max_bachelor_weight = max(bachelor_weight_list)
        if  master_weight_list != []:
                max_master_weight = max(master_weight_list)
        if phd_weight_list != []:
                max_phd_weight = max(master_weight_list)
        education_degree_weight = np.round(max_bachelor_weight*max_master_weight*max_phd_weight,3)
        total_education_weight = work_activite_weight*education_weight*(education_grand_weight*education_degree_weight*olimp_highest_weight*olimp_rank_weight)**(1/3)
        total_education_weight = np.round(total_education_weight,7)
        
        return total_education_weight
        
        


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