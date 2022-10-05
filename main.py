import os
import logging
from pprint import pprint

import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def fetch_vacancies_page_hh(language, page, area_id, period):
    """Returns certain page with vacancies"""

    hh_base_api_url = "https://api.hh.ru/"
    hh_vacancies_url = hh_base_api_url + "vacancies/"
    logging.debug(hh_vacancies_url)
    if period:
        params = {
            "text": f"Программист {language}",
            "area": area_id,
            "page": page,
            "per_page": 100,    # Number of vacancy per page
            "period": period,
        }
    else:
        params = {
            "text": "Программист",
            "page": page,
            "per_page": 100,
            "area": area_id,
        }

    response = requests.get(hh_vacancies_url, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def fetch_vacancies_by_language(language, area_id=113, period=None):
    """
    Returns dict with all pages with vacancies accordingly language
    In:
    language - programming language,
    area_id - area_id from hh.ru API's list of area(default 113 - Russia)
    period - period for vacancies
    Out:
    Dict with vacancies data
    """

    vacancies = fetch_vacancies_page_hh(language, 0, area_id, period)
    page = 0
    pages = vacancies['pages']
    vacancies = []
    while page < pages:
        vacancies.append(fetch_vacancies_page_hh(language, page, area_id,
                                                 period))
        page += 1
    return vacancies


def get_vacancies_quantity(vacancies):
    """Returns number founded vacancies"""

    return vacancies[0]['found']


def get_average_salary_from_vacancies_hh(vacancies_pages):
    """Returns processed vacancies and average salary"""

    salaries = []
    for vacancy_page in vacancies_pages:
        for vacancy in vacancy_page["items"]:
            salaries.append(
                predict_rub_salary_hh(vacancy['salary'])
            )

    # Filtering salaries from None elements
    salaries = [salary for salary in salaries if salary]
    return len(salaries), sum(salaries) // len(salaries)


def predict_salary(from_, to_):
    """Takes range from_ and to_ and returns average salary"""
    if not from_ and not to_:
        return None
    if from_ and not to_:
        return int(from_ * 1.2)
    if not from_ and to_:
        return int(to_ * 0.8)
    return (from_ + to_) // 2


def predict_rub_salary_hh(vacancy_salary):
    """Returns average salary by vacance_salary dict"""

    if not vacancy_salary:
        return None
    if vacancy_salary['currency'] != 'RUR':
        return None
    from_, to_ = vacancy_salary['from'], vacancy_salary['to']
    return predict_salary(from_, to_)


def fetch_langs_info_hh(area_id, period):
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Objective-C',
        'Scala',
        'Swift',
        'TypeScript'
    ]
    languages_info = {}

    # По каждому языку получаем кол-во найденных вакансий, обработанных
    # вакансий и среднюю зарплату
    for language in languages:
        # Загружаем вакансии по конкретному языку в vacancies
        try:
            vacancies = fetch_vacancies_by_language(language, area_id, period)
        except requests.exceptions.HTTPError:
            logging.warning('Не удалось получить список вакансий с hh.ru')
        # Расчёт средней зп и обработанных вакансий из vacancies
        vacancies_processed, average_salary = \
            get_average_salary_from_vacancies_hh(vacancies)
        # Добавление информации по языку в список информации по языкам
        languages_info[language] = {
            "vacancies_found": get_vacancies_quantity(vacancies),
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return languages_info


def predict_rub_salary_from_sj(vacancy):
    #currency - rub
    #payment_from
    #payment_to
    if not vacancy:
        return None
    if vacancy['currency'] != 'rub':
        return None

    from_, to_ = vacancy['payment_from'], vacancy['payment_to']
    return predict_salary(from_, to_)


def fetch_vacancies_page_sj(api_key, lang, town=4, page=0):
    headers = {
        'X-Api-App-Id': api_key,
    }

    vacancies_per_page = 100
    params = {
        'keyword': f'Программист {lang}',
        'town': town,   # 4 - id of Moscow
        'page': page,
        'count': vacancies_per_page
    }

    url = 'https://api.superjob.ru/2.0/vacancies/'

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies_page = response.json()
    return vacancies_page


def fetch_vacancies_by_language_sj(api_key, language, area_id=4):
    """
    Returns dict with vacancies accordingly language
    In:
    language - programming language,
    area_id - town from superjob.ru API's list of area(default 4 - Moscow)
    Out:
    Dict with vacancies data
    """

    vacancies_by_lang = []
    page = 0
    while True:
        vacancies_page = fetch_vacancies_page_sj(api_key, language, area_id,
                                                 page)
        vacancies_by_lang.append(vacancies_page)
        if not vacancies_page['more']:
            break
        page += 1

    return vacancies_by_lang


def get_average_salary_from_vacancies_sj(vacancies_pages):
    """Returns processed vacancies from superjob.ru and average salary"""

    salaries = []
    for vacancy_page in vacancies_pages:
        for vacancy in vacancy_page["objects"]:
            salaries.append(
                predict_rub_salary_from_sj(vacancy)
            )

    # Filtering salaries from None elements
    salaries = [salary for salary in salaries if salary]
    # Checking for empty salaries if salaries contains before only None
    if not salaries:
        return 0, 0
    return len(salaries), sum(salaries) // len(salaries)


def fetch_langs_info_sj(api_key, area_id):
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Objective-C',
        'Scala',
        'Swift',
        'TypeScript'
    ]

    languages_info = {}

    # По каждому языку получаем кол-во найденных вакансий, обработанных
    # вакансий и среднюю зарплату
    for language in languages:
        # Загружаем вакансии по конкретному языку в vacancies
        vacancies ={}
        try:
            vacancies = fetch_vacancies_by_language_sj(api_key,language,
                                                       area_id)
        except requests.exceptions.HTTPError:
            logging.warning('Не удалось получить список вакансий с '
                            'superjob.ru')
        # Расчёт средней зп и обработанных вакансий из vacancies
        vacancies_processed, average_salary = \
            get_average_salary_from_vacancies_sj(vacancies)
        # Добавление информации по языку в список информации по языкам
        languages_info[language] = {
            "vacancies_found": vacancies[0]["total"],
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return languages_info


def print_ascii_table(title, languages_info):
    data = []
    data.append(
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    )

    for language, info in languages_info.items():
        data.append(
            [
                language,
                info['vacancies_found'],
                info['vacancies_processed'],
                info['average_salary']
            ]
        )
    table = AsciiTable(data, title)
    print(table.table)

def print_table_of_avg_salaries_hh(languages_info):
    title = 'HeadHunter Moscow'
    print_ascii_table(title, languages_info)


def print_table_of_avg_salaries_sj(languages_info):
    title = 'SuperJob Moscow'
    print_ascii_table(title, languages_info)


def main():
    load_dotenv()
    hh_moscow_id = os.getenv('MOSCOW_CITY_ID')
    superjob_api_key = os.getenv('SUPERJOB_API_KEY')
    sj_moscow_id = os.getenv('SJ_MOSCOW_CITY_ID')

    print_table_of_avg_salaries_hh(fetch_langs_info_hh(hh_moscow_id, 30))
    print_table_of_avg_salaries_sj(
        fetch_langs_info_sj(superjob_api_key, sj_moscow_id)
    )

if __name__ == "__main__":
    main()
