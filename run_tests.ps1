#!/bin/bash
pytest -m desktop --platform desktop --alluredir=reports/allure-results --clean-alluredir
allure serve reports/allure-results