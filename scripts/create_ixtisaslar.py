from app.models import Question, Answer
import pandas as pd
import locale

def azerbaijani_locale_sort(list):
    # Sort the country names using the Azerbaijani locale
    locale.setlocale(locale.LC_COLLATE, 'az_AZ.UTF-8')
    sorted_list = sorted(list, key=locale.strxfrm)
    return sorted_list

def find_duplicates(lst):
    count_dict = {}
    duplicates = []

    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    for item, count in count_dict.items():
        if count > 1:
            duplicates.append(item)

    return duplicates

def run():
    q = Question.objects.filter(question_title="İxtisas").first()

    path = "C:/Users/Nazim/Downloads/cleaned_ixtisaslar(new).xlsx"
    df = pd.read_excel(path)
    ixtisaslar = set()
    ixtisaslar = []
    
    for id, ixtisas in df.iterrows():
        if ixtisas.ixtisasv1 != None and ixtisas.ixtisasv1 != '' and isinstance(ixtisas.ixtisasv1, str):
            ixtisaslar.append(ixtisas.ixtisasv1)
    
    sorted_ixtisaslar = azerbaijani_locale_sort(ixtisaslar)

    print(f"len: {len(sorted_ixtisaslar)}, duplicates: {find_duplicates(sorted_ixtisaslar)}")

    for ixtisas in sorted_ixtisaslar:
        if not Answer.objects.filter(questionIdd=q, answer_title=ixtisas).exists():
            Answer.objects.create(answer_title=ixtisas, questionIdd=q)
