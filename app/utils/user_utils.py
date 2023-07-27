from datetime import datetime
import numpy as np



def get_date_weight(finnly_date):
        if 0 <= finnly_date < 1:
                finnly_date_weight = 0.9
        elif 1 <= finnly_date < 3:
                finnly_date_weight = 0.7
        elif 3 <= finnly_date < 5:
                finnly_date_weight = 0.5
        elif 5 <= finnly_date <10:
                finnly_date_weight = 0.3
        elif 10 <= finnly_date <20:
                finnly_date_weight = 0.1
        elif 20 <= finnly_date:
                finnly_date_weight = 0.01

        return finnly_date_weight

def calculate_date_difference(data):
        if data["endDate"] == "":
            current_date = datetime.now()
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            difference = current_date - start_date
        else:
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            end_date = datetime.strptime(data["endDate"], "%Y-%m-%d")
            difference = end_date - start_date
        return difference

def get_bachelor_weight(user):
        language_weight = 1
        total_muraciyyet_weight = 1
        power_count = 0
        userdata = user.user_info[1]["formData"]["EducationScore"]
        for bachelors in userdata:
                if bachelors.get("bachelor") is not None:
                        if bachelors['bachelor']['criterion']['criterion_type'] == 'her ikisi':
                                lokal_test_weight = bachelors['bachelor']['criterion']['lokal_test']['answer_weight']
                                muraciyyet = bachelors['bachelor']['criterion']['muraciyyet']
                                for m in muraciyyet:
                                        if m['muraciyyet_type'] == 'Atestat':
                                                power_count+=1     
                                                atestat_weight = m['answer_weight']
                                                total_muraciyyet_weight *= atestat_weight
                                        elif m['muraciyyet_type'] == 'language':
                                                for lang in m['language_type']:
                                                    power_count+=1
                                                    language_weight *= lang['answer_weight']
                                                language_weight = np.round(language_weight,3)
                                                total_muraciyyet_weight *= language_weight
                                        elif m['muraciyyet_type'] == 'SAT':
                                               sat_weight = m['answer_weight']
                                               total_muraciyyet_weight*=sat_weight
                                total_muraciyyet_weight = (total_muraciyyet_weight)**(1/power_count) 
                                total_muraciyyet_weight = np.round(total_muraciyyet_weight,3)
                                total_bachelors_weight = np.round((lokal_test_weight*total_muraciyyet_weight)**(1/2),3)    
                                return total_bachelors_weight
                        elif bachelors['bachelor']['criterion']['criterion_type'] == 'Lokal imtahan': 
                               pass
                        
                        elif bachelors['bachelor']['criterion']['criterion_type'] == 'Müraciyyət': 
                               pass


                        