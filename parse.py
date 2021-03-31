#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# Path data
XLSX = "data/citizen-science-projects.xlsx"
CSV = "data/citizen-science-projects.csv"
final_README = str

# Convert from xsls to csv in pandas
excel_file = pd.read_excel(XLSX)
excel_file.to_csv(CSV)

# Read csv
csv = pd.read_csv(CSV)

categories = pd.unique(csv["Category"])
categories.sort()

with open('README.md', 'r', encoding='utf-8') as read_me_file:
    read_me = read_me_file.read()
    main_text = ''.join(read_me.split('- - -')[0])
    toc = "\n\n- [Awesome Citizen Science Projects](#awesome-citizen-science-projects)\n"

    # Add catogories to table of content
    for cat in range(len(categories)):
        toc = toc + \
            f"  - [{categories[cat]}](#{categories[cat]})" + "\n"

# Add first part and toc to README
final_README = main_text + "- - -" + toc + "\n- - -"

# Add individual categories to README
list_blocks = ""
for cat in range(len(categories)):
    block = f"\n\n## {categories[cat]}\n"
    filtered = csv[csv["Category"] == categories[cat]]
    list_items = ""
    for i, r in filtered.iterrows():
        try:
            start_date = int(r['Start Date'])
        except:
            start_date = "NA"
        project = f"* [{r['Name']}]({r['Main Source']}) - {r['Description']} (`{start_date}` - `{str(r['End Date'])}`) \n"
        list_items = list_items + project
    list_blocks = list_blocks + block + list_items

# Add to README.md
final_README = final_README + list_blocks

# Save to new README.md
with open('README.md', 'w+', encoding='utf-8') as sorted_file:
    sorted_file.write(final_README)
