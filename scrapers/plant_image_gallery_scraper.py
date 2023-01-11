import pandas as pd
import parsel
import requests
import time

BASE_URL = 'https://nobleapps.noble.org/plantimagegallery/'
INDEX_URL = BASE_URL + 'PlantList.aspx?IndexType=ScientificName&PlantTypeID='
PLANT_TYPES = {
    'FORBS': '1',
    'GRASSES_GRASSLIKES': '2',
    'TREES_SHRUBS_WOODY_WINES': '3',
    'AQUATICS': '4',
}

plant_df = pd.DataFrame(columns=['scientific_name', 'image_url'])

for plant_type, plant_type_id in PLANT_TYPES.items():
    print(f'Scraping index for {plant_type}')
    try:
        index_response = requests.get(INDEX_URL + plant_type_id)
    except:
        print('No response')
        break
    index_selection = parsel.Selector(index_response.text)
    link_list = index_selection.xpath('//table[@id="ContentPlaceHolder1_tblIndex"]//a/@href').getall()
    for link in link_list:
        time.sleep(2)
        plant_attr = dict()
        try:
            plant_response = requests.get(BASE_URL + link)
        except:
            print('No response')
            break
        plant_selection = parsel.Selector(plant_response.text)

        scientific_name = plant_selection.xpath('//tr[2]/td[2]/h6/i/i/text()').get()
        if scientific_name is None:
            scientific_name = plant_selection.xpath('//tr[2]/td[2]/h6/i/text()').get()
        plant_attr['scientific_name'] = scientific_name

        image_url = plant_selection.xpath('//div[@id="plantCarousel"]//img/@src').get()
        plant_attr['image_url'] = image_url

        print(f'Scraped data for {scientific_name}')
        plant_df = pd.concat([plant_df, pd.DataFrame(plant_attr, index=[0])])
    time.sleep(2)

print('Export plant data to csv...')
plant_df.to_csv('data/plant_image_gallery.csv', index=False)
