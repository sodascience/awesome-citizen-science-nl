#!/usr/bin/env python
# coding: utf-8
import argparse
from concurrent.futures import ProcessPoolExecutor
import glob
import os
import urllib3

import pandas as pd
import requests
from ruamel.yaml import YAML

# Path data
CSV = "data/citizen-science-projects-nl.csv"
EXCEL = "data/citizen-science-projects-nl.xlsx"
DATA = "data/categories"
NOT_OK = ":x:"
OK = ":white_check_mark:"

# Ignore InsecureRequestWarning warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup YAML
y = YAML()
y.default_flow_style = False
y.explicit_start = True
y.indent(sequence=4, offset=2)


def excel_to_csv():
    """Convert excel to csv for other uses."""
    excel = pd.read_excel(EXCEL, engine='openpyxl')
    excel.to_csv(CSV, index=False, sep=",")


def csv_to_yaml():
    """Read CSV data and output individual yml files."""
    csv = pd.read_csv(CSV, sep=",")

    # Find unique categories
    categories = pd.unique(csv["main_category"])
    categories.sort()

    # Save rows csv to yaml files
    y = YAML()
    y.default_flow_style = False
    y.explicit_start = True
    y.indent(sequence=4, offset=2)

    for cat in range(len(categories)):
        PATH_CATEGORY = os.path.join(DATA, categories[cat])
        if not os.path.exists(PATH_CATEGORY):
            os.makedirs(PATH_CATEGORY)
        cat_data = csv[csv["main_category"] == categories[cat]].copy()
        # Save each line of each cateogry in json file
        # but only if file was updated
        for i, r in cat_data.iterrows():
            FILE_NAME = r['name'].replace(" ", "_").replace('/', '_')
            PATH_FILE = os.path.join(PATH_CATEGORY, f"{FILE_NAME}.yml")
            dict_r = r.to_dict()
            if os.path.isfile(PATH_FILE):
                with open(PATH_FILE, "r") as old_file:
                    old = y.load(old_file.read())
                    if old is None:
                        save_dict_to_yaml(PATH_FILE, dict_r)
                    #  if not equal then overwrite with new
                    elif not dict(old) == dict(dict_r):
                        old_file.close()
                        save_dict_to_yaml(PATH_FILE, dict_r)
            else:
                save_dict_to_yaml(PATH_FILE, dict_r)


def yml_to_csv_and_excel():
    """Read yaml files and create CSV + XLSX file."""
    files = []
    y = YAML()
    y.default_flow_style = None
    y.explicit_start = True
    y.indent(sequence=4, offset=2)

    for filename in glob.iglob(f"{DATA}/**/*", recursive=True):
        if not os.path.isdir(filename):
            with open(filename, "r") as file:
                row = y.load(file.read())
                files.append(row)

    df = pd.DataFrame(files)

    # Check validity of urls
    list_urls = []
    for i, r in df.iterrows():
        list_urls.append({
            "url": r["project_information_url"],
            "name": r["name"]})
    problems_url = pd.DataFrame(check_urls(list_urls), columns=[
        "name", "url", "error"])
    problems_url["icon"] = NOT_OK
    df = df.merge(problems_url, how="left", on="name")

    # Clean df before saving
    df_save = df.copy()
    df_save["start_date"] = df_save["start_date"].astype(pd.Int64Dtype())
    df_save["end_date"] = df_save["end_date"].astype(pd.Int64Dtype())
    df_save.drop(columns=["icon", "url", "error"], inplace=True)
    # Save to CSV
    df_save.to_csv("data/citizen-science-projects-nl.csv",
                   index=False, sep=",")
    # Save to Excel
    df_save.to_excel("data/citizen-science-projects-nl.xlsx",
                     index=False, engine='openpyxl')

    return df


def create_readme(df):
    """Retrieve text from README.md and update it."""
    readme = str

    categories = pd.unique(df["main_category"])
    categories.sort()

    with open('README.md', 'r', encoding='utf-8') as read_me_file:
        read_me = read_me_file.read()
        splits = read_me.split('<!---->')

        # Initial project description
        text_intro = splits[0]

        # Contribution and contacts
        text_contributing = splits[3]
        text_citation = splits[4]
        text_contacts = splits[5]

        # TOC
        toc = "\n\n- [Awesome Citizen Science Projects](#awesome-citizen-science-projects)\n"
        # Add categories
        for cat in range(len(categories)):
            toc += f"  - [{categories[cat]}](#{categories[cat]})" + "\n"
        # Add contributing and contact to TOC
        toc += "- [Contribute or update project](#contribute-or-update-project)\n"
        toc += "- [Citation](#citation)\n"
        toc += "- [Contact](#contact)\n"

    # Add first part and toc to README
    readme = text_intro + "<!---->" + toc + "\n<!---->\n"

    # Add projects subtitle
    readme += "\n## Projects\n"

    # Add individual categories to README
    list_blocks = ""
    for cat in range(len(categories)):
        block = f"\n### {categories[cat]}\n\n"
        filtered = df[df["main_category"] == categories[cat]]
        list_items = ""
        for i, r in filtered.iterrows():
            start_date = convert_date(r, 'start_date')
            end_date = convert_date(r, 'end_date')
            if end_date == "NA":
                # If end date is NA, the status is a better indication of the current
                # state of the proejct
                end_date = r["status"]
            if not pd.isna(r['icon']):
                project = f"- {r['icon']}  [{r['name']}]({r['project_information_url']}) - {r['description']} (`{start_date}` - `{end_date}`)\n"
                list_items = list_items + project
            else:
                project = f"- [{r['name']}]({r['project_information_url']}) - {r['description']} (`{start_date}` - `{end_date}`)\n"
                list_items = list_items + project
        list_blocks = list_blocks + block + list_items

    # Add to categories to README.md
    readme += list_blocks + "\n"

    # Add contribution and contacts
    readme += '<!---->' + text_contributing
    readme += '<!---->' + text_citation
    readme += '<!---->' + text_contacts

    with open('README.md', 'w+', encoding='utf-8') as sorted_file:
        sorted_file.write(readme)


def yaml_to_csv_and_readme():
    df = yml_to_csv_and_excel()
    create_readme(df)

# Helpers


def save_dict_to_yaml(PATH, dict):
    """Very lazy way to update value in dict."""
    with open(PATH, 'w') as file:
        start_date = convert_date(dict, "start_date")
        end_date = convert_date(dict, "end_date")

        try:
            if isinstance(start_date, int):
                dict["start_date"] = start_date
        except ValueError:
            dict["start_date"] = None

        try:
            if isinstance(end_date, int):
                dict["end_date"] = end_date
        except ValueError:
            dict["end_date"] = None
        y.dump(dict, file)


def check_url(url, name):
    try:
        response = requests.head(
            url, allow_redirects=True, verify=False, timeout=25)
        if response.status_code in [301, 302]:
            return name, url, f'Redirects to {response.headers["Location"]}'
    except Exception as e:
        return name, url, repr(e)


def check_urls(url_list):
    with ProcessPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_url, **file) for file in url_list]
        responses = [future.result() for future in futures]

    return [r for r in responses if r is not None]


def convert_date(dict, date_key):
    """Convert dates to int or "NA" if missing."""
    try:
        date = int(dict[date_key])
    except:
        date = "NA"
    return date


# Parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel-to-csv",
                        dest="excel_to_csv",
                        help="Read xlsx and convert it to CSV",
                        action="store_true")
    parser.add_argument("--csv-to-yaml",
                        dest="csv_to_yaml",
                        help="Read CSV and convert rows to YAML files",
                        action="store_true")
    parser.add_argument("--yaml-to-csv-and-readme",
                        dest="yaml_to_csv_and_readme", help="Read YAML files, convert them to CSV and create readme",
                        action="store_true")
    args = parser.parse_args()

    if args.excel_to_csv:
        excel_to_csv()

    if args.csv_to_yaml:
        csv_to_yaml()

    if args.yaml_to_csv_and_readme:
        yaml_to_csv_and_readme()
