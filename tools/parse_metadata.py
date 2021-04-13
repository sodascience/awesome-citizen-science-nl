#!/usr/bin/env python
# coding: utf-8
import glob
import os

import requests
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from ruamel.yaml import YAML

# Path data
CSV = "data/citizen-science-projects.csv"
DATA = "data/categories"
NOT_OK = ":x:"
OK = ":white_check_mark:"


def read_csv_data():
    """Read CSV data and output individual yml files."""
    # Excel not used anymore
    # xlsl = pd.read_excel("data/citizen-science-projects.xlsx")
    # xlsl.to_csv("data/citizen-science-projects.csv")
    csv = pd.read_csv(CSV)

    # Find unique categories
    categories = pd.unique(csv["category"])
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
        cat_data = csv[csv["category"] == categories[cat]].copy()
        cat_data.drop(columns=['Unnamed: 0'], inplace=True)
        # Save each line of each cateogry in json file
        # but only if file was updated
        for i, r in cat_data.iterrows():
            FILE_NAME = r['name'].replace(" ", "_").replace('/', '_')
            PATH_FILE = os.path.join(PATH_CATEGORY, f"{FILE_NAME}.yml")
            dict_r = r.to_dict()
            if os.path.isfile(PATH_FILE):
                with open(PATH_FILE, "r") as old_file:
                    old = y.load(old_file.read())
                    #  if not equal then overwrite with new
                    if not dict(old) == dict(dict_r):
                        old_file.close()
                        with open(PATH_FILE, 'w') as ofile:
                            y.dump(dict_r, ofile)
            else:
                with open(PATH_FILE, 'w') as ofile:
                    y.dump(dict_r, ofile)


def read_yml_files():
    """Read from yaml files each category and save to df."""
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
            "url": r["main_source"],
            "name": r["name"]})
    problems_url = pd.DataFrame(check_urls(list_urls), columns=[
        "name", "url", "error"])
    problems_url["icon"] = NOT_OK
    df = df.merge(problems_url, how="left", on="name")
    #df[['icon']] = df[['icon']].fillna(value=OK)

    return df


def check_url(url, name):
    try:
        response = requests.head(url, allow_redirects=False, timeout=20)
        if response.status_code in [301, 302]:
            return name, url, f'Redirects to {response.headers["Location"]}'
    except Exception as e:
        return name, url, repr(e)


def check_urls(url_list):
    with ProcessPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(check_url, **file) for file in url_list]
        responses = [future.result() for future in futures]

    return [r for r in responses if r is not None]


def create_readme(df):
    """Retrieve text from README.md and update it."""
    readme = str

    categories = pd.unique(df["category"])
    categories.sort()

    with open('README.md', 'r', encoding='utf-8') as read_me_file:
        read_me = read_me_file.read()
        splits = read_me.split('<!---->')

        # Initial project description
        text_intro = splits[0]

        # Contribution and contacts
        text_contributing = splits[3]
        text_contacts = splits[4]

        # TOC
        toc = "\n\n- [Awesome Citizen Science Projects](#awesome-citizen-science-projects)\n"
        # Add categories
        for cat in range(len(categories)):
            toc = toc + \
                f"  - [{categories[cat]}](#{categories[cat]})" + "\n"

    # Add first part and toc to README
    readme = text_intro + "<!---->" + toc + "\n<!---->\n"

    # Add projects subtitle
    readme += "\n## Projects\n"

    # Add individual categories to README
    list_blocks = ""
    for cat in range(len(categories)):
        block = f"\n### {categories[cat]}\n\n"
        filtered = df[df["category"] == categories[cat]]
        list_items = ""
        for i, r in filtered.iterrows():
            try:
                start_date = int(r['start_date'])
            except:
                start_date = "NA"
            if not pd.isna(r['icon']):
                project = f"- {r['icon']}  [{r['name']}]({r['main_source']}) - {r['description']} (`{start_date}` - `{str(r['end_date'])}`)\n"
                list_items = list_items + project
            else:
                project = f"- [{r['name']}]({r['main_source']}) - {r['description']} (`{start_date}` - `{str(r['end_date'])}`)\n"
                list_items = list_items + project
        list_blocks = list_blocks + block + list_items

    # Add to categories to README.md
    readme += list_blocks

    # Add contribution and contacts
    readme += '<!---->' + text_contributing
    readme += '<!---->' + text_contacts

    return readme


# Write new README.md
if __name__ == "__main__":
    df = read_yml_files()
    readme_file = create_readme(df)
    with open('README.md', 'w+', encoding='utf-8') as sorted_file:
        sorted_file.write(readme_file)
