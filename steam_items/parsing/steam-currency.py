# import requests
# from bs4 import BeautifulSoup
# from django.shortcuts import render

# def get_currency_rate():
#     url = "https://steam-currency.ru/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     elements = soup.find_all()
#     return elements
#     # for element in elements:
#     #     rate_element = element.find(class_="CurrentCourse_Course__TpQ+-")
#     #     if rate_element is not None:
#     #         return rate_element.text
#     # return "Не удалось получить курс валюты"


# print(get_currency_rate())