import pandas as pd
import parsel
import requests

BASE_URL = 'https://www.howmanyplants.com'
LIST_PATH = '/plant-guides'

# get all paths to plants
print('load plant urls...')
response = requests.get(BASE_URL + LIST_PATH)
selection = parsel.Selector(response.text)
plant_paths = selection.css('div.plant-index-grid a::attr(href)').getall()

# initialize dataframe to store data
plant_df = pd.DataFrame(columns=[
    'name', 'official_name', 'alias', 'origins', 'climate', 'description',
    'difficulty', 'water', 'light', 'humidity', 'temperature', 'toxicity',
    'size', 'format', 'leaf_shape', 'image_url', 'url'])

# iterate through each url and store data in dataframe
print('iterate plant urls and parse info...')
for path in plant_paths:
    resp = requests.get(BASE_URL + path)
    sel = parsel.Selector(resp.text)
    # extract information from hero section
    plant_attr = dict()
    plant_attr['url'] = BASE_URL + path
    plant_attr['name'] = sel.css('div.hero-title > h1::text').get().strip()
    plant_attr['image_url'] = sel.css('img.hero-image').xpath('@src').get()
    basic_info = sel.css('div.plants-hero-grid-text > p::text').getall()
    plant_attr['official_name'] = basic_info[0].strip()
    plant_attr['alias'] = basic_info[1].strip()
    if '|' in basic_info[2]:
        plant_attr['origins'] = basic_info[2].split('|')[0].strip()
        plant_attr['climate'] = basic_info[2].split('|')[1].strip()
    else:
        plant_attr['origins'] = basic_info[2].split(',')[0].strip()
        plant_attr['climate'] = basic_info[2].split(',')[1].strip()
    plant_attr['description'] = basic_info[3].strip()
    # count number of green thumbs
    plant_attr['difficulty'] = len(sel.css(
        'div.green-thumb-outline.w-condition-invisible').getall())
    # extract information basic content grid
    basic_content = sel.css('p.the-basics-attribute-text::text').getall()
    plant_attr['water'] = basic_content[0].strip()
    plant_attr['light'] = basic_content[1].strip()
    plant_attr['humidity'] = basic_content[2].strip()
    plant_attr['temperature'] = basic_content[3].strip()
    plant_attr['toxicity'] = basic_content[4].strip()
    plant_attr['size'] = basic_content[5].strip()
    plant_attr['format'] = basic_content[6].strip()
    plant_attr['leaf_shape'] = basic_content[7].strip()
    # concat plant_attr to plant_df
    plant_df = pd.concat([plant_df, pd.DataFrame(plant_attr, index=[0])])

print('export plant data to csv...')
# save plant_df to csv
plant_df.to_csv('plant_data.csv', index=False)
