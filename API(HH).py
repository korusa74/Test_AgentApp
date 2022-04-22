'''Здравствуйте, скрипт ищет компании у которых максимальное количество вакансий в выбранном регионе, так же можно добавить поиск по слову в названии, или в описании компании.
'''

import requests

type_list = ['Прямой работодатель', 'Кадровое агентство', 'Руководитель проекта', 'Частный рекрутер']
url_area = 'https://api.hh.ru/areas'
url_dict = 'https://api.hh.ru/dictionaries'
url_empl = 'https://api.hh.ru/employers'


def getting_regions(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def getting_dicts(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['employer_type']


def find_id_region(country_list):
    for country in country_list:
        region_list = country['areas']
        for region in region_list:
            if region['name'] == my_region:
                id_area = region['id']
                return id_area


def find_id_type(dicts_list):
    for type in types_list:
        if type['name'] == employer_type:
            id_type = type['id']
            return id_type


def getting_company(url, page):
    if len(search_word) != 0:
        payload = {'text': search_word, 'area': id_area, 'type': id_type, 'only_with_vacancies': True, 'page': page, 'per_page': 100}
    else:
        payload = {'area': id_area, 'type': id_type, 'only_with_vacancies': True, 'page': page, 'per_page': 100}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def find_cmp_max_vc(pages, company_list):
    if pages > 1:
        for page in range(1, (pages)):
            company_list.extend(getting_company(url_empl, page)['items'])
    max_vc_cmp = sorted(company_list, key=lambda d: d['open_vacancies'], reverse=True)[0:5]
    return max_vc_cmp


if __name__ == '__main__':
    my_region = input('Введите регион: ')
    search_word = input('Введите слово для поиска из назавния работодателя, или из его описания: ')
    employer_type = int(input('Введите тип работодателя: 0 - Прямой работодатель, 1 - Кадровое агентство, 2 - Руководитель проекта, 3 - Частный рекрутер: '))
    if employer_type in [0, 1, 2, 3]:
        employer_type = type_list[employer_type]
    else:
        print('Не верно введен тип попробуйте еще раз: ')
        employer_type = int(input('Введите тип работодателя: 0 - Прямой работодатель, 1 - Кадровое агентство, 2 - Руководитель проекта, 3 - Частный рекрутер: '))

    try:
        country_list = getting_regions(url_area)
    except requests.exceptions.HTTPError:
        print('Что-то пошло не так при выборе региона')
    try:
        types_list = getting_dicts(url_dict)
    except requests.exceptions.HTTPError:
        print('Что-то пошло не так при выборе id типа работодателя')

    id_area = find_id_region(country_list)
    if not id_area:
        print('Ошибка в названии региона, попробуйте ещё раз')
        my_region = input('Введите регион: ')
        id_area = find_id_region(country_list)
    
    id_type = find_id_type(types_list)

    try:
        pages = getting_company(url_empl, 0)['pages']
    except requests.exceptions.HTTPError:
        print('Что-то пошло не так при выборе компании')

    company_list = getting_company(url_empl, 0)['items']

    for vc in find_cmp_max_vc(pages, company_list):
        name = vc['name']
        open_vacancies = vc['open_vacancies']
        print(f'Название: {name}, Количество открытых вакансий: {open_vacancies}')
