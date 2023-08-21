from app.models import Question, Answer
import pandas as pd

import locale

def azerbaijani_locale_sort(country_names):
    # Set the locale to Azerbaijani (az_AZ)
    locale.setlocale(locale.LC_COLLATE, 'az_AZ.UTF-8')
    # Sort the country names using the Azerbaijani locale
    sorted_country_names = sorted(country_names, key=locale.strxfrm)
    return sorted_country_names


def run():
    q = Question.objects.filter(question_title="təhsilinizlə bağlı detalları qeyd edin:").first()
    print(q)

    country_names = lst
    sorted_country_names = azerbaijani_locale_sort(country_names)

    for country in sorted_country_names:
        # print(country)
        if not Answer.objects.filter(questionIdd=q, answer_title=country).exists():
            Answer.objects.create(answer_title=country,questionIdd=q)
    
    
    
    
    # url = 'https://az.wikipedia.org/wiki/D%C3%BCnya_%C3%B6lk%C9%99l%C9%99rinin_siyah%C4%B1s%C4%B1'
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # target_table = soup.find('table', {'class': 'wikitable'})
    # column_index = 1 

    # for row in target_table.find_all('tr'):
    #     columns = row.find_all('td')
    #     if columns:
    #         column_data = columns[column_index].get_text(strip=True)
    #         print(column_data)


    # pdf_path = 'C:/Users/Nazim/Downloads/Documents/Dunya_tes.pdf'
    # start_page = 7
    # end_page = 14
    # headers_text = extract_headers_from_pdf(pdf_path, start_page, end_page)
    # headers = extract_columns(headers_text)
    # print(headers)



    # df = create_dataframe(column_data)
    # print(df['Ölkə və ya regionun adı'])
    # q = Question.objects.filter(question_title = "pilləsi barədə məlumatları qeyd edin:").first()
    # print(q)

    # path = "C:/Users/Nazim/Downloads/Ölkələr (1).csv"
    # df = pd.read_csv(path)
    
    # new_answers = []
    # for id, country in df.iterrows():
    #     new_answers.append(country.Country)
    # new_answers = sorted(new_answers, key=lambda x: [azerbaijani_alphabet_order(c) for c in x])
    
    # for country in new_answers:
    #     # print(country)
    #     if not Answer.objects.filter(questionIdd=q, answer_title=country).exists():
    #         Answer.objects.create(answer_title=country,questionIdd=q)

    # a = []
    # for i in Answer.objects.filter(questionIdd=q):
    #     a.append(i)
    # print(a)
    

lst = ['Əfqanıstan', 'Albaniya', 'Əlcəzair', 'Anqola',
        'Antiqua və Barbuda', 'Argentina', 'Ermənistan', 'Avstraliya',
        'Avstriya', 'Azərbaycan', 'Baham adaları', 'Banqladeş', 'Barbados',
        'Belarus', 'Belçika', 'Beliz', 'Benin', 'Butan', 'Boliviya',
        "Bosniya və Herseqovina", "Botsvana", "Braziliya", "Bruney",
        'Bolqarıstan', 'Burkina Faso', 'Burundi', 'Kamboca', 'Kamerun',
        'Kanada', 'Kabo Verde', 'Mərkəzi Afrika Respublikası', 'Çad',
        'Çili', 'Çin', 'Kolumbiya', 'Komor', 'Kosta Rika', 'Xorvatiya',
        'Kipr', 'Çexiya', 'Danimarka', 'Cibuti', 'Ekvador', 'Misir',
        'El Salvador', 'Ekvatorial Qvineya', 'Estoniya', 'Efiopiya', 'Fici',
        'Finlandiya', 'Fransa', 'Qabon', 'Qambiya', 'Gürcüstan', 'Almaniya',
        'Qana', 'Yunanıstan', 'Qrenada', 'Qvineya', 'Qvineya-Bisau', 'Qayana',
        'Honduras', 'Çin, P.R.: Honq Konq', 'Macarıstan', 'İslandiya',
        'Hindistan', 'İndoneziya', 'İran', 'İraq', 'İrlandiya', 'İsrail', 'İtaliya',
        'Fildişi Sahili', 'Yamayka', 'Yaponiya', 'İordaniya', 'Qazaxıstan', 
'Keniya', 'Küveyt', 'Qırğızıstan', 'Laos', 'Latviya', 'Livan', 'Lesoto',
        'Liberiya', 'Liviya', 'Litva', 'Lüksemburq',
        'Çin, P.R.: Makao', 'Madaqaskar', 'Malavi', 'Malayziya',
        'Maldiv adaları', 'Mali', 'Malta', 'Mavritaniya', 'Meksika', 'Mikroneziya',
        'Moldova', 'Monqolustan', 'Monteneqro', 'Mərakeş', 'Mozambik',
        'Namibiya', 'Hollandiya', 'Yeni Zelandiya', 'Nikaraqua', 'Niger',
        'Nigeriya', 'Şimali Makedoniya', 'Norveç', 'Oman', 'Pakistan',
        "Palau", "Fələstin", "Panama", "Papua Yeni Qvineya", "Paraqvay",
        'Peru', 'Filippin', 'Polşa', 'Portuqaliya', 'Qətər', 'Rumıniya',
        "Rusiya", "Ruanda", "St. Lucia", 'St. Vinsent və Qrenadinlər',
        'Samoa', 'San Marino', 'Səudiyyə Ərəbistanı', 'Seneqal', 'Serbiya',
        'Seyşel adaları', 'Sierra Leone', 'Sinqapur', 'Slovakiya', 'Sloveniya',
        "Solomon adaları", "Cənubi Afrika", "Cənubi Koreya", "İspaniya",
        'Şri Lanka', 'Sudan', 'Surinam', 'Esvatini', 'İsveç',
        'İsveçrə', 'Suriya', 'Tacikistan', 'Tanzaniya', 'Tayland',
        'Toqo', 'Tonqa', 'Trinidad və Tobaqo', 'Tunis', 'Türkiyə',
        'Uqanda', 'Ukrayna', 'Birləşmiş Ərəb Əmirlikləri', 'Birləşmiş Krallıq',
        "Uruqvay", "Özbəkistan", "Vanuatu", "Venesuela", "Vyetnam",
        'Yəmən', 'Zambiya', 'Zimbabve', 'Aruba', 'Qvatemala', 'Kiribati',
        'Nepal', 'Sao Tome və Prinsipi', 'Birma (Myanma)', 'Haiti',
        'Konqo Respublikası', 'Andorra', 'Bəhreyn', 'Bermuda', 'Eritreya',
        'Farer adaları', 'Cəbəllütariq', 'Lixtenşteyn', 'Monako',
        'Yeni Kaledoniya', 'Puerto Riko', 'Amerika Birləşmiş Ştatları', 'Somali',
        'Türkmənistan', 'Tuvalu', 'Şimali Koreya', 'Dominikan Respublikası',
        'Tayvan', 'İnsan Adası', 'Kuba', 'Kayman Adaları', 'Mavrikiy',
        'Amerika Birləşmiş Ştatları Virgin Adaları', 'Qrenlandiya',
        'St. Martin (Fransız hissəsi)', 'Quam', 'Myanma', 'Kosovo',
        'Fransız Polinezyası', 'Timor-Leste', 'Konqo Dem. Rep.',
        'Cənubi Sudan', 'St. Kitts və Nevis', 'Dominika',
        'Marşal Adaları', 'Sint Maarten (Hollandiya hissəsi)', 'Kurasao',
        'Amerika Samoası', 'Şimali Mariana Adaları',
        'Britaniya Virgin Adaları', 'Turks və Kaykos Adaları', 'Nauru',
        'Montserrat', 'Norfolk Island', 'Anguilla',
        'Müqəddəs Taxt (Vatikan)', 'Kanal Adaları']