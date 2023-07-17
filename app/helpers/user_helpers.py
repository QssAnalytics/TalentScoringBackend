from typing import TypeVar
import numpy as np
import math, time
from django.contrib.auth import get_user_model

UserAccount = get_user_model()
user_account_type = TypeVar('user_account_type', bound=UserAccount)

def get_education_score(user_info: user_account_type, username:str):
        # start_time = time.time()
        tehsil_score = 0
        user = user_info.objects.filter(username = username).first()
        education= user.user_info[0]["formData"]["education"]
        occupation_weight = user.user_info[0]["formData"]["curOccupation"]["answer_weight"]
        grade_weight = user.user_info[0]["formData"]["educationGrant"]["answer_weight"]
        if user.user_info[2]["formData"]["wonOlympics"] == "1":
                olympiad_status_weight = user.user_info[2]["formData"]["highestOlympiad"]["answer_weight"]
                olympiad_rank_weight = user.user_info[2]["formData"]["rankOlympiad"]["answer_weight"]
        else:
                olympiad_status_weight=1
                olympiad_rank_weight = 1
        if len(education) ==3:
                education_weight = education[0]["bachelor"]["answer_weight"]*education[1]["master"]["answer_weight"]*education[2]["phd"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]*user.user_info[1]["formData"]["masterScore"]["answer_weight"]*user.user_info[1]["formData"]["phdScore"]["answer_weight"]
                # education_weight = np.exp(np.log(education[0]["bachelor"]["answer_weight"]) + np.log(education[1]["master"]["answer_weight"]) + np.log(education[2]["phd"]["answer_weight"]))
        elif len(education) ==2:
                education_weight = education[0]["bachelor"]["answer_weight"]*education[1]["master"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]*user.user_info[1]["formData"]["masterScore"]["answer_weight"]
        elif len(education) ==1:
                education_weight = education[0]["bachelor"]["answer_weight"]
                education_score = user.user_info[1]["formData"]["bachelorsScore"]["answer_weight"]
        # end_time = time.time()
        # duration = end_time - start_time
        # print("Duration:", duration, "seconds")
        # tehsil_score = (occupation_weight*education_weight*(grade_weight*education_score*olympiad_status_weight*olympiad_rank_weight)**(1/3))*100
        tehsil_score = (
            np.exp(
                np.log(occupation_weight)
                + np.log(education_weight)
                + (1/3) * np.log(grade_weight * education_score * olympiad_status_weight * olympiad_rank_weight)
            )
        ) * 100        
        tehsil_score = np.round(tehsil_score,8)
        return user, tehsil_score

def get_language_score():
        pass

def get_experience_score():
        pass