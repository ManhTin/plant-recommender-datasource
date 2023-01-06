# Plant Recommender App
Datasourcing for the Homeplant Recommender System project in Data Integration 22/23 at WWU Münster

## Cleaned Data

The cleaned dataset contains 1666 indoor and outdoor plants with following attributes:

| Attribute               | Indoor | Outdoor |
|-------------------------|--------|---------|
| active_growth_period    | -      | x       |
| bloom_period            | -      | x       |
| climate                 | x      | -       |
| common_name             | x      | x       |
| difficulty              | x      | -       |
| drought_tolerance       | x      | x       |
| duration                | -      | x       |
| family                  | -      | x       |
| family_common_name      | -      | x       |
| flower_color            | -      | x       |
| foliage_color           | x      | x       |
| foliage_porosity_summer | -      | x       |
| foliage_porosity_winter | -      | x       |
| frost_free_days         | -      | x       |
| fruit_color             | -      | x       |
| growth_habit            | x      | x       |
| growth_rate             | -      | x       |
| height                  | x      | x       |
| humidity                | x      | -       |
| image                   | x      | -       |
| leaf_shape              | x      | x       |
| lifespan                | -      | x       |
| light                   | x      | -       |
| origin                  | x      | x       |
| ph_minimum              | -      | x       |
| ph_maximum              | -      | x       |
| scientific_name         | x      | x       |
| temperature             | x      | -       |
| toxicity                | x      | x       |
| type                    | x      | x       |
| width                   | x      | -       |

## Installation and Setup

Getting started

### Prerequisites

- Python 3.10
    - We recommend to use [miniforge](https://github.com/conda-forge/miniforge#install) (or [miniconda](https://docs.conda.io/en/latest/miniconda.html)). Since you can manage Python versions and virtual environments with it. Follow the setup steps below if you use miniforge (or miniconda)
    - after successful installation of miniforge (or miniconda) the command `conda` should be available
    - follow the setup guide from step 4 if you use another method of managing virtual environments
- Setup project
    1. `cd` into this directory
    1. Create virtual environment for project: `conda create --name plant-recommender-datasource python=3.10`
    1. Activate virtual environment of project: `conda activate plant-recommender-datasource`
    1. Install dependencies into virtual env: `pip install -r requirements.txt`
    1. Start jupyter server: `jupyter notebook`
- Run scraper
    1. howmanyplants.com scraper: `python scrapers/how_many_plants_scraper.py` -> exports to `data/...`
