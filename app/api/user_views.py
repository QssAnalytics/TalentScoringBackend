import math, pandas as pd, openai
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from app import models
from app.helpers.user_helpers import *
from pprint import pprint

from app.serializers import user_serializers
# Create your views here.

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

@swagger_auto_schema(method='POST', request_body=user_serializers.LoginSerializer)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = user_serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    password = serializer.validated_data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        tokens=get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        res.data = tokens
        
        res["X-CSRFToken"] = csrf.get_token(request)

        return res
    raise rest_exceptions.AuthenticationFailed(
        "Username or Password is incorrect!")

@swagger_auto_schema(method='POST', request_body=user_serializers.RegistrationSerializer)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    serializer = user_serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")


@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"]=None
        
        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")



class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")

        return super().finalize_response(request, response, *args, **kwargs)   
    
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.UserAccount.objects.get(id=request.user.id)
    except models.UserAccount.DoesNotExist:
        return response.Response(status_code=404)

    serializer = user_serializers.UserAccountSerializer(user)
    return response.Response(serializer.data)



# class UserEducationScoreApiView(APIView):
#     def get(self, request, username):
#         user = models.UserAccount.objects.filter(username = username).first()
#         tehsil_score_exists = any("tehsil_score" in item for item in user.user_info)
#         if not tehsil_score_exists:
#             user, tehsil_score = get_education_score(user)
#             user.user_info.append({"tehsil_score":tehsil_score})
#             user.save()
#             return response.Response({"user-info":user.user_info})
#         return response.Response({"user-info":user.user_info})


# class UserScoreApiView(APIView):
#     async def get(self, request, username):
#         user = await models.UserAccount.objects.afilter(username = username).aonly("username", "user_info").afirst()
#         tehsil_score = await get_education_score(user)
#         experiance_score = await get_experience_score(user)
#         # user.user_info.append({"tehsil_score":tehsil_score})
#         # user.save()
#         return response.Response({})
#         return response.Response({"user-info":user.user_info, "tehsil_score":tehsil_score, "experiance_score":experiance_score})
    
class UserScoreApiView(APIView):
    def get(self, request, username):
        user = models.UserAccount.objects.filter(username=username).only("username", "user_info").first()

        tehsil_score = get_education_score(user)
        experiance_score = get_experience_score(user)
        skills_weight = get_skills_weight(user)

        # user.user_info.append({"tehsil_score":tehsil_score})
        # user.save()

        return response.Response({"user-info":user.user_info, "tehsil_score":tehsil_score, "experiance_score":experiance_score, "special_skills_weight":skills_weight})
    

class SummryPromptApiView(APIView):
    def get(self, request):
        df = pd.read_excel('sample_df.xlsx')
        a = df.iloc[17]["work_experience"]
        openai.api_key = "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"
        def generate_cv_summary(i = 17, dataframe = df, save_pdf = True, pdf_file_name = 'sample_CV.pdf', print_response = True, temperature = 0.7):
    
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
            resp = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"""You are a helpful AI tool which can create only summary part of CV professionally. User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": """Please create me a short summary (max 100 words) part for the CV based on the information of me professionally and in a formal way. 
                                                 Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                                 Write it in first personal singular"""},

                ],
                temperature = temperature,
                # max_tokens = 100
            )
            
            return resp.choices[0].message.content
        sample_summary = generate_cv_summary()
        sample_summary.replace('\n\n', '\n')
        
        return response.Response({"sample_summary":sample_summary})
    
class ExperiancePromptApiView(APIView):
    def get(self, request):
        df = pd.read_excel('sample_df.xlsx')
        openai.api_key = "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"
        def generate_summary_job_experience(i = 17, dataframe = df, job_no = 1, temperature = 0.7):

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
                    {"role": "system", "content": f"""You are a helpful AI tool which can create summary and details part of job experience parts of CV professionally. 
                                                    User data is this: {prompt}. You may also need to know that {testing_system_info}.
                                                    The response you give will be written into CV pdf file, so that do not indicate any redundant and irrelevant things in your response.
                                                    """},
                    {"role": "user", "content": f"""Please create me a short summary (max 3 bullet points, each no more than 10 words) part of my job experience {job_no} based on the information of me professionally and in a formal way. 
                                                 Add some extra explanations as needed. Do not indicate something like 'Summary:' etc. The response  will be automatically written to CV.
                                                 Use bullet points as needed. Do not indicate job name, positions, date range, only some info about job.
                                                 """},
                       ],
                temperature = temperature,
                # max_tokens = 100
            )

            # response.choices[0].message.content


            return response.choices[0].message.content

        job_experience1 = generate_summary_job_experience()
        job_experience1 = job_experience1.replace("•",'').split('\n')
        job_experience1 = list(map(lambda x: x.strip(), job_experience1))
        job_experience1 = list(map(lambda x: x[1:] if x[0] == '-' else x, job_experience1))
        return response.Response({"job_experience":job_experience1})