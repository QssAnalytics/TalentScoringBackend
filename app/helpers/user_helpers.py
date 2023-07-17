from typing import TypeVar
from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

def get_education_score(user_info: user_account_type, username:str):
        tehsil_score = 0
        
        user = user_info.objects.filter(username = username).first()
        
        occupation_weight = user.user_info[0]["formData"]["curOccupation"]["answer_weight"]
        education_weight = user.user_info[0]["formData"]["education"]["answer_weight"]
        grade_weight = user.user_info[0]["formData"]["educationGrant"]["answer_weight"]
        bachelors_weight = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]
        olympiad_status_weight = user.user_info[2]["formData"]["highestOlympiad"]["answer_weight"]
        olympiad_rank_weight = user.user_info[2]["formData"]["rankOlympiad"]["answer_weight"]

        tehsil_score = (occupation_weight*education_weight*(grade_weight*bachelors_weight*olympiad_status_weight*olympiad_rank_weight)**(1/3))*100
        return user, tehsil_score

def get_language_score():
        pass

def get_experience_score():
        pass