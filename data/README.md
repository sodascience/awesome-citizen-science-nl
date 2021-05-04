# Citizen Science Projects Dataset Specifications

The dataset contains citizen science projects in the Netherlands. Citizen science is scientific work that citizens completely or partially conduct themselves on a voluntary basis. Professional researchers often provide instructions and guidance, but they are not the main collectors of the data. Alongside project names, the dataset includes supplementary information regarding a description of the project, its organizers, location, duration, data accessibility, and links to the main project information and data if applicable. This document contains a technical specification of the dataset. 

## Data availability 

The list of Citizen Science projects is available in various formats. This makes the reuse 
of the dataset easy. The human-readable list of projects is available on the website 
https://sodascience.github.io/awesome-citizen-science-nl/. This list is also available on
GitHub https://github.com/sodascience/awesome-citizen-science-nl where it is 
maintained.

Structured datsets with more variables (see [Codebook](#codebook)) are available as CSV and 
Excel files on both GitHub and Zenodo. The latter one is recommended for academic use because
the releases are persistent and therefore won't change anymore (important for reproducibility).

### GitHub

- Directory: [`data/`](https://github.com/sodascience/awesome-citizen-science-nl/tree/main/data)
- File format: 
  - CSV [`data/citizen-science-projects-nl.csv`](https://github.com/sodascience/awesome-citizen-science-nl/tree/main/data/citizen-science-projects-nl.csv)
  - Excel [`data/citizen-science-projects-nl.xlsx`](https://github.com/sodascience/awesome-citizen-science-nl/tree/main/data/citizen-science-projects-nl.xlsx)

### Zenodo

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4724569.svg)](https://doi.org/10.5281/zenodo.4724569)

- Directory: [`data/`](https://github.com/sodascience/awesome-citizen-science-nl/tree/main/data)
- File format: 
  - CSV `data/citizen-science-projects-nl.csv`
  - Excel `data/citizen-science-projects-nl.xlsx`

## Data updates

The dataset on Github is updated every time a new project is proposed and merged into the 
project by the maintainers. The dataset on Zenodo is updated once in a while when new projects 
are added to the list. The version number of the dataset on Zenodo reflects the date of 
retrieval from GitHub. 

## Codebook

The following table contains an overview of the available variables and outcome values.

| Column name | Description    | Format    |
|-|-|-|
| name    | Name of the project | Character    |
| description    | Short description of what the citizen scientists do in the project    | Character    |
| main_category    | What category the project mainly belongs to     | Character – *archeology, cities, ecology, environment, health, history, science, society, uncategorized*     |
| extra_categories    | Any extra categories that would also fit the project     | Character – *archeology, cities, ecology, environment, health, history, science, society, uncategorized*    |
| organization    | List of the organization that organize the project    | Character    |
| country    | The Netherlands    | Character    |
| location    | If applicable, a more specific location in the Netherlands    | Character    |
| notes_on_location    | Any remarks on the location    | Character    |
| start_date    | Year the project started    | YYYY    |
| end_date    | Year the project ended, reoccurring if the project takes place every year or ongoing if the project has not yet finished    | YYYY or character – *reoccurring, ongoing*    |
| notes_duration    | Any remarks on the duration    | Character    |
| data_accessibility    | The extent to which the data is accessible    | Character – *downloadable, viewable, no direct download*    |
| accessibility_for_research    | Whether the data can be accessed for research purposes    | Character – *yes, no*    |
| project_information_url    | Link to an information page on the project    | Character    |
| data_url    | Link to the data    | Character    |

## Contribute new projects

We aim to make this list as complete as possible and up-to-date. You can easily propose new 
citizen science projects to this list or update information on existing ones. See 
[Contribute or update project](https://github.com/sodascience/awesome-citizen-science-nl#contribute-or-update-project)

## Data license

This dataset is published with a CC-BY-4.0 License license https://github.com/sodascience/awesome-citizen-science-nl/blob/main/LICENSE. 

## Data citation

To cite this dataset in academic publications, you can cite the following Zenodo publication [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4724569.svg)](https://doi.org/10.5281/zenodo.4724569). 

```
Timmers, Annemarie, & Lugtig, Peter. (2021). List of Citizen Science Projects 
in the Netherlands (Version v2021.4.29) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4724570
```

## Contact

For contact, reach out to a.g.j.timmers@uu.nl or p.lugtig@uu.nl. 
