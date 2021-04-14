# Contributing

Your contributions are always welcome!

## Guidelines

* Search previous Pull Requests or Issues before making a new one, as yours may be a duplicate.
* Follow [`How to contribute to a new data entry`](CONTRIBUTING.md)
* Add one project per Pull Request.
  * Make sure the PR title is in the format of `Add project-name`.
  * Don't mention `Citizen Science` in the description as it's implied.
  * Write down the reason why the project is awesome.
* For each project, use the template you can find under PULL_REQUEST_TEMPLATE.yml:
* Each project should have **at least** the following information:
  * Name;
  * Concise and **short** description of the project;
  * Category to which the project belongs, if the category is not present, add a new one. Please try not to add a category if there is already one that might fit;
  * Main link where more information is present.
* Check your spelling and grammar.
* Remove any trailing whitespace.

## How to contribute to a new data entry

To contribute to Awesome Citizen Science NL, please follow these simple steps:

1. Fork `citizen-science-project-nl`.
2. Clone your project to your computer, from your terminal:
```bash
git clone https://github.com/yourname/awesome-citizen-science-project-nl.git
cd awesome-citizen-science-project-nl
```
3. Using `PULL_REQUEST_TEMPLATE.yml`, that you can find in the main directory of the project, create a new entry for the project you want to add. Try to complete all fields, but do not worry to leave some information blank.
4. Give a name to the new project, for example `new_project.yml`.
5. Add the new project within fitting category
6. Commit the modification to your repository
```bash
git add ./data/categories/SELECTED_CATEGORY/NEW_DATASET.yml
git commit -m "Add NEW_DATASET under SELECTED_CATEGORY"
git push origin master
```
7. Create a new Pull Request by going on Awesome Citizen Science NL pull requests: https://github.com/sodascience/awesome-citizen-science-nl/pulls