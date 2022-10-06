import os
import logging

import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def fetch_vacancies_page_hh(language, page, area_id, period):
    """Returns certain page with vacancies"""

    base_api_url = "https://api.hh.ru/"
    hh_vacancies_url = base_api_url + "vacancies/"

    params = {
            "text": f"Программист {language}",
            "area": area_id,
            "page": page,
            "per_page": 100,    # Number of vacancy per page
            "period": period,
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
    area_id - area_id from hh.ru API list of area (default 113 - Russia)
    period - period for vacancies
    Out:
    Dict with vacancies data
    """

    vacancies = []
    page = 0
    while True:
        try:
            vacancies.append(fetch_vacancies_page_hh(language, page, area_id,
                                                     period))
        except requests.exceptions.HTTPError:
            logging.warning("Can't fetch page with vacancies from hh.ru")
        pages = vacancies[page]['pages']
        if page == pages - 1:
            break
        page += 1

    return vacancies


def get_processed_and_average_salaries(salaries):
    """Returns tuple with processed vacancies and average salaries"""

    # Filtering salaries from None elements
    salaries = [salary for salary in salaries if salary]
    if not salaries:
        return 0, 0
    return len(salaries), sum(salaries) // len(salaries)


def get_data_from_vacancies_hh(vacancies_pages):
    """Returns processed vacancies and average salary"""

    salaries = []
    for vacancy_page in vacancies_pages:
        for vacancy in vacancy_page["items"]:
            salaries.append(
                predict_rub_salary_hh(vacancy['salary'])
            )

    return get_processed_and_average_salaries(salaries)


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
    """Returns avg salary or None if currency is rubles or undefined salary"""

    if not vacancy_salary:
        return None
    if vacancy_salary['currency'] != 'RUR':
        return None
    from_, to_ = vacancy_salary['from'], vacancy_salary['to']
    return predict_salary(from_, to_)


def fetch_langs_avg_salaries_hh(area_id, period, languages):
    """
    Gets area_id, period and languages for searching and return langs data
    In:
    area_id - id of town from https://api.hh.ru/areas
    period - search periods in days
    languages - list of programming languages for search
    Out:
    Dict with programming languages with dicts that contains fetched data for
    this language such as:
        vacancies_found,
        vacancies_processed,
        average_salary
    """

    languages_summary = {}
    # For every language gets count of finded vacancies, processed vacancies
    # and average salary
    for language in languages:
        vacancies = fetch_vacancies_by_language(language, area_id, period)

        vacancies_processed, average_salary = \
            get_data_from_vacancies_hh(vacancies)

        languages_summary[language] = {
            "vacancies_found": vacancies[0]['found'],
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return languages_summary


def predict_rub_salary_from_sj(vacancy):
    """Returns avg salary or None if currency is rubles or undefined salary"""

    if not vacancy:
        return None
    if vacancy['currency'] != 'rub':
        return None
    from_, to_ = vacancy['payment_from'], vacancy['payment_to']
    return predict_salary(from_, to_)


def fetch_vacancies_page_sj(api_key, lang, town, page):
    """Returns certain page with vacancies"""

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
    Returns dict of pages with vacancies accordingly language
    In:
    api_key - superjob api secret key for application
    language - programming language
    area_id - town from superjob.ru API's list of area (default 4 - Moscow)
    Out:
    Dict with vacancies data
    """

    vacancies_by_lang = []
    page = 0

    # Fetched dict of page have key more, that False if there is no other
    # pages to fetch
    while True:
        vacancies_page = {}
        try:
            vacancies_page = fetch_vacancies_page_sj(
                api_key, language, area_id, page
            )
        except requests.exceptions.HTTPError:
            logging.warning("Can't fetch page with vacancies from superjob.ru")

        vacancies_by_lang.append(vacancies_page)
        if not vacancies_page['more']:
            break
        page += 1

    return vacancies_by_lang


def get_data_from_vacancies_sj(vacancies_pages):
    """Returns processed vacancies from superjob.ru and average salary"""

    salaries = []
    for vacancy_page in vacancies_pages:
        for vacancy in vacancy_page["objects"]:
            salaries.append(
                predict_rub_salary_from_sj(vacancy)
            )

    return get_processed_and_average_salaries(salaries)


def fetch_langs_avg_salary_sj(api_key, area_id, languages):
    """
    Gets api, area_id and languages for searching and return langs data
    In:
    api_key - secret key for application from https://api.superjob.ru/register
    area_id - id of town from https://api.superjob.ru/2.0/towns/
    languages - list of programming languages for search
    Out:
    Dict with programming languages with dicts that contains fetched data for
    this language such as:
        vacancies_found,
        vacancies_processed,
        average_salary
    """

    languages_summary = {}
    # For every language gets count of found vacancies, processed vacancies
    # and average salary
    for language in languages:
        vacancies = \
            fetch_vacancies_by_language_sj(api_key, language, area_id)
        vacancies_processed, average_salary = \
            get_data_from_vacancies_sj(vacancies)

        languages_summary[language] = {
            "vacancies_found": vacancies[0]["total"],
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return languages_summary


def print_ascii_table(title, languages_summary):
    data = [[
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"
    ]]

    for language, info in languages_summary.items():
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


def print_table_of_avg_salaries_hh(languages_data):
    title = 'HeadHunter Moscow'
    print_ascii_table(title, languages_data)


def print_table_of_avg_salaries_sj(languages_data):
    title = 'SuperJob Moscow'
    print_ascii_table(title, languages_data)


def main():
    load_dotenv()
    hh_moscow_id = os.getenv('HH_MOSCOW_CITY_ID')
    superjob_api_key = os.getenv('SUPERJOB_API_KEY')
    sj_moscow_id = os.getenv('SJ_MOSCOW_CITY_ID')

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

    print_table_of_avg_salaries_hh(
        fetch_langs_avg_salaries_hh(hh_moscow_id, 30, languages)
    )
    print_table_of_avg_salaries_sj(
        fetch_langs_avg_salary_sj(superjob_api_key, sj_moscow_id, languages)
    )


if __name__ == "__main__":
    main()
