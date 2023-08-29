import base64, pandas as pd, openai, environ
import os
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import response, status as rest_status

from users import models

from users.helpers.sync_user_helpers import *
from users.serializers import user_serializers, user_account_file_serializers, certificate_serializers
from users.utils.random_unique_key_utils import generate_unique_random_key

env = environ.Env()
environ.Env.read_env()

class CertificateDesigAPIView(APIView):
    def get(self, request):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        dir = os.path.join(BASE_DIR, 'sample_df.xlsx')
        df = pd.read_excel(dir)

        openai.api_key = env("api_key")

        # def generate_input_prompt(i = 17, dataframe = df):

        #     ######################
        #     ##  Create Prompt   ##
        #     ######################

        #     prompt = ''
        #     prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
        #     prompt += f"I have education level of {df.iloc[i].level}. "
        #     to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
        #     prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
        #     prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
        #     prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
        #     prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
        #     prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
        #                             language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

        #     prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

        #     prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


        #     prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
        #     prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

        #     # print(prompt)
        #     return prompt
        
        # input_promt = generate_input_prompt()
        def generate_certificate_designation_content(i = 17, dataframe = df, temperature = 0.7):
            
            ######################
            ##  Create Prompt   ##
            ######################

            prompt = ''
            prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {df.iloc[i].level}. "
            to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
            prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
            prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
            prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
            prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                                    language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

            prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

            prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


            prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''


            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can generate certificate designation section of our Talent Score which is a tool \
                    gauges a person's talent based on his/her career and education history, as well as his/her special talents (writing/music/painting), sport skills, \
                    language and program skills, olympiad results (if participated). In TalentScore system, there is no examination, it's based on survey data provided by user.
                    like this:
                                    Future Innovator or Skillful Learner etc.
                                                    User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": """Please write certificate designation section (max 3 words) based on the information of the user. \
                                                """},

                ],
                temperature = temperature,
            )


            print(response.choices[0].message.content)
            return response.choices[0].message.content
        certificate_designation_content = generate_certificate_designation_content()
        return response.Response({"certificate_designation_content": certificate_designation_content}, status=rest_status.HTTP_200_OK)

    
class CertificateIntroAPIView(APIView):
    def get(self, request):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        dir = os.path.join(BASE_DIR, 'sample_df.xlsx')
        df = pd.read_excel(dir)

        openai.api_key = env("api_key")
        
        def generate_certificate_intro_content(i = 17, dataframe = df, temperature = 0.7):
            ######################
            ##  Create Prompt   ##
            ######################

            prompt = ''
            prompt += f'Hello, my name is {df.iloc[i].name_surname}. I am {df.iloc[i].age} years old. I am {df.iloc[i].gender}. '
            prompt += f"I have education level of {df.iloc[i].level}. "
            to_be_form =   'were' if df.iloc[i].level != 'High School' else 'are'
            prompt += f"My high school grades {to_be_form} excellent. " if df['performance'].iloc[i] == 'excellent student' else f"My high school grades {to_be_form} competent. " if df['performance'].iloc[i] == 'average student' else f"My high school grades {to_be_form} average. "
            prompt += "" if df.iloc[i].level == 'High School' else f"Here is detailed information about my education: {df.iloc[i].educations}. "
            prompt += "" if df.iloc[i].Olympics_win == 'no' else f" I have participated in {df.iloc[i]['Olympiad subject']} subject which was in {df.iloc[i].Best_stage} level and got {df.iloc[i].Result_of_olimpic}. "
            prompt += "I have had no work experience. " if df.iloc[i].work_experience == 'No' else f"Here is detailed information about my work experience: {df.iloc[i].work_experience}. "
            prompt += f"I have no other language knowledge and my native language is {df.iloc[i].native_lang}" if df.loc[i, 'language level'] == "No language knowledge" else f"""My native
                                    language is {df.iloc[i].native_lang} and here is detailed information about my language knowledge: {df.loc[i, 'language level']}. """

            prompt += "" if df.iloc[i].sport_details == {} or df.iloc[i].sport_details == '{}' else f"Here is detailed information about my sport background {df.iloc[i].sport_details}. "

            prompt += "" if df.iloc[i].special_skills == {} or df.iloc[i].special_skills == '{}' else f"Here is detailed information about my background on other skills: {df.iloc[i].special_skills}. "


            prompt += "" if df.iloc[i].programming_knowledge == {} or df.iloc[i].programming_knowledge == '{}' else f"Here is detailed information about my background on programming skills: {df['programming_knowledge'].iloc[i]}. "
            prompt = prompt.replace("'", "").replace('"', "").replace("{", "").replace("}", "").replace("_", " ").replace('\n', " ").replace('                         ', " ")

            ################################
            ##  Assign test system info   ##
            ################################
            testing_system_info = '''
                                Having excellent grades in high school means having all grades of best grades (such as A). Having competent grades in high school means having all grades of best and good grades (such as A and B).
                                Having average grades in high school means having different grades - A, B, C, D, etc.
                                DIM is an abbreviation for State Examination Center in Azerbaijan, where most students choose this center's exams to get admission for high educational institutes.
                                Bachelor's Education entrance exam points range is 0-700. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 600-700 is considered exceptionally good and only 5-10% of students can score that much. To be in this interval, students should score at least 80% in each test subjects.
                                Score range of 500-600 is considered good and only 10-15% of students can score in this interval. To be in this interval, students should score at least 60%-70% in each test subjects.
                                Score range of 350-500 is considered normal and only 20-25% of students can score in this interval.
                                Score range of 200-350 is considered bad and range of 0-200 is considered that the person has failed to demonstrate good score.

                                Master's Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 40-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-40   is considered bad and it means that the person has failed.

                                PhD Education entrance exam score range is 0-100. Having high score is associated with high level of industriousness and may signal higher level of IQ.
                                Score range of 80-100 is considered exceptionally good and only 5-10% of students can achieve this.
                                Score range of 50-80  is considered good and only 10-15% of students can score this.
                                Score range of 30-50  is considered normal and only 20-25% of students can score this.
                                Score range of 0-30   is considered bad and it means that the person has failed.'''

            score_1 = '90%'
            score_2 = '95%'
            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can generate certificate summary section of our Talent Score which is a tool \
                    gauges a person's talent and calculate peer percentile and overall percentile scores based on his/her career and education history,
                    as well as his/her special talents (writing/music/painting), sport skills, \
                    language and program skills, olympiad results (if participated). In TalentScore system, there is no examination, it's based on survey data provided by user.
                    like this:
                        With an impressive score of 90% and a peer percentile ranking of 85%, Homer Simpson stands out prominently with a versatile range of aptitudes \
                        and skills. This distinguished certificate highlights their exceptional accomplishments and showcases their readiness for roles that demand \
                        exceptional [specific strengths/traits], empowering them to thrive in [specific positions/fields]. This attests to their unwavering dedication \
                        to personal and professional advancement. This person is quite suitable for [positions].

                                                    User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into pdf file, so that do not indicate any redundant and irrelevant things
                                                    in your response. You also know that you should emphasize strong sides of the candidate, potential relevant job positions.
                                                    """},
                    {"role": "user", "content": f"""Please write certificate summary section (max 30-40 words) based on the information of the user.
                    User's peer percentile score is {score_1} and overall percentile score is {score_2}
                                            """},

                ],
                temperature = temperature,
            )


            print(response.choices[0].message.content)

            return response.choices[0].message.content

        certificate_intro_content = generate_certificate_intro_content()
        return response.Response({"certificate-intro-content":certificate_intro_content}, status=rest_status.HTTP_200_OK)
    
class UploadCertificateAPIView(APIView):
    def post(self, request):
        req_data = request.data.get('cert-file')
        format, imgstr = req_data.split(';base64,')
        ext = format.split('/')[-1] 
        data_file = ContentFile(base64.b64decode(imgstr), name='cert.' + ext)
        try:
          email = request.data.get('email')
          user = models.UserAccount.objects.get(email=email)

        except models.UserAccount.DoesNotExist:
            return response.Response({'error': 'User not found with the provided email.'}, status=rest_status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            file_data = {'user': user.id, 'file': data_file, "file_category": "CERTIFICATE"}
            user_accout_serializer = user_account_file_serializers.UserAccountFilePageSerializer(data=file_data)
            certificate_data = {
                "file_key": request.data.get("file_key"),
                "date_created": request.data.get("date_created")
            }
            cert_serializer = certificate_serializers.CertificateFileSerializer(data=certificate_data)
            if user_accout_serializer.is_valid() and cert_serializer.is_valid():
                user_accout_file = user_accout_serializer.save()
                cert_serializer.validated_data['certificate_file'] = user_accout_file
                cert_serializer.save()
                return response.Response({'message': f"Certificate of user with email: {user.email} uploaded."}, status=rest_status.HTTP_201_CREATED)
            else:
                return response.Response(user_accout_serializer.errors or cert_serializer.errors, status=rest_status.HTTP_400_BAD_REQUEST)


class CreateUniqueCertificateValue(APIView):
    def get(self, request):
        code = generate_unique_random_key()
        print(code)
        d = models.UniqueRandom.objects.filter(unique_value=code).exists()
        MAX_TRIES = 31
        loop_count = 0
        while d:
            loop_count+=1
            code = generate_unique_random_key()
            d = models.UniqueRandom.objects.filter(unique_value=code).exists()
            if loop_count > MAX_TRIES:
                return response.Response("REQUEST_TIMEOUT", status=rest_status.HTTP_408_REQUEST_TIMEOUT)
        
        return response.Response({'code': code, 'unique':not d})