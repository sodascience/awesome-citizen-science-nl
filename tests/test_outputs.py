#!/usr/bin/env python
from collections import OrderedDict

import os
import yaml

import pandas as pd


def test_output_csv(yaml_dir):
    """Test if output data csv contains the yaml categories."""
    # Retrieve all categories from csv file
    csv = pd.read_csv("data/citizen-science-projects-nl.csv")
    categories_csv = list(csv["main_category"].unique())

    # Retrieve all categories from yaml directory
    categories_yaml = os.listdir(yaml_dir)

    same_categories = True
    for category in sorted(categories_yaml):
        if category not in categories_csv:
            same_categories = False

    return same_categories


def test_output_excel(yaml_dir):
    """Test if output data excel contains the yaml categories."""
    # Retrieve all categories from excel file
    excel = pd.read_excel("data/citizen-science-projects-nl.xls")
    categories_excel = list(excel["main_category"].unique())

    # Retrieve all categories from yaml directory
    categories_yaml = os.listdir(yaml_dir)

    same_categories = True
    for category in sorted(categories_yaml):
        if category not in categories_excel:
            same_categories = False

    return same_categories


def test_output_readme(yaml_dir):
    # Retrieve all categories from yaml directory
    categories_yaml = os.listdir(yaml_dir)

    with open('README.md', 'r', encoding='utf-8') as read_me_file:
        read_me = read_me_file.read()
        splits = read_me.split('<!---->')

        # Initial project description
        readme_content = splits[2]

    same_categories = True
    for category in sorted(categories_yaml):
        if category not in readme_content:
            same_categories = False

    return same_categories


if __name__ == '__main__':
    categories_dir = "data/categories"

    test_csv = test_output_csv(categories_dir)
    #test_excel = test_output_excel(categories_dir)
    #test_readme = test_output_readme(categories_dir)

    assert test_csv == True
    #assert test_excel == True
    #assert test_readme == True
