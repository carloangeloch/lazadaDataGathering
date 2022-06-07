#Objective is to get all useful data from the lazada pdp url

import logging
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import json
import os
from datetime import datetime

lists = np.loadtxt('laz_url.csv', dtype=str)
urls = lists.tolist()
urls = urls[1::]

# urls = ['https://www.lazada.com.ph/products/century-tuna-calamansi-155g-i1673850891-s7220284823.html?spm=a2o4l.pdp_revamp.recommend_2.1.6e6b77511Jr24x&mp=1&cid=0&mp=1&impsrc=&ad_src=1110_1201:184.441696,1400_910:0.99956722758188,1400_1015:1.99920042605661,1400_2200:0.951581189361557&cpc=343&originalCpc=1000&pos=-1&highest_price=1000&pa=sponsored_bottom&did=62df6c3c-a8ad-4dfe-9885-c4e1041627a7&abid=0,13242120,237633,12786048,12656132,12523892,12449264,12773904,13058896,11989614,12475494,12189920,12346150,12618398,12345564,12950436,12192856,195686,13132974,12267602,12559250,10910152,12900842,12575244,12729396,8460342,13296946,12849084,12793016,13198514,12091908,13271924&adFlag=3&adid=0&bucketId=0&sellerId=500159556001&itemId=1673850891&member_id=153320619&ncid=101100011736086&adgroup_id=464258366&creative_id=0&brand_id=2822&category_id=25368&regional_key=142508020000&pdp_item=2304415736&pid_pvid=d0b41e082dc2ab8ee1e2d042289fd2c9&nick=&pvid=62df6c3c-a8ad-4dfe-9885-c4e1041627a7&pvtime=1649841868&ad_src=1110_1201:184.441696,1400_910:0.99956722758188,1400_1015:1.99920042605661,1400_2200:0.951581189361557&crowd_id=&one_id=',
#         'https://www.lazada.com.ph/products/century-tuna-paella-180g-i2443751291-s11146681643.html?spm=a2o4l.pdp_revamp.recommend_2.2.6e6b77511Jr24x&mp=1&cid=0&mp=1&impsrc=&ad_src=4700_3002:7010&cpc=459&originalCpc=1000&pos=-1&highest_price=1000&pa=sponsored_bottom&did=62df6c3c-a8ad-4dfe-9885-c4e1041627a7&abid=0,13242120,237633,12786048,12656132,12523892,12449264,12773904,13058896,11989614,12475494,12189920,12346150,12618398,12345564,12950436,12192856,195686,13132974,12267602,12559250,10910152,12900842,12575244,12729396,8460342,13296946,12849084,12793016,13198514,12091908,13271924&adFlag=3&adid=0&bucketId=0&sellerId=500159556001&itemId=2443751291&member_id=153320619&ncid=101100014204020&adgroup_id=523870165&creative_id=1425616401&brand_id=2822&category_id=25368&regional_key=142508020000&pdp_item=2304415736&pid_pvid=d0b41e082dc2ab8ee1e2d042289fd2c9&nick=&pvid=62df6c3c-a8ad-4dfe-9885-c4e1041627a7&pvtime=1649841868&ad_src=4700_3002:7010&crowd_id=&one_id=',
#         'https://www.lazada.com.ph/products/century-tuna-flakes-in-hot-spicy-155g-x4-century-tuna-with-calamansi-155g-i2304415738-s10431389109.html']

def main():

    #perparation of file
    now = datetime.now()
    #check for output folder
    if os.path.exists('output/'):
        logging.warning('Folder exists!')
    else:
        logging.warning('No folder. Creating one . . .')
        os.makedirs('output')
    #check for file name today
    filename = 'lazada_pdp_data_'+ now.strftime("%Y-%m-%d")+".csv"
    if os.path.exists('output/'+filename):
        with open('output/'+filename, 'a') as f:
            logging.warning('File exists. Adding new records . . .')
            f.write("\nsequence,seller_chat_response_rate,seller_name,seller_new_seller,seller_rate,seller_id,seller_ship_on_time,seller_shop_id,seller_time,seller_unit,product_category_0,product_category_1,product_category_2,product_brand_name,product_brand_id,product_pdt_sku,product_core_country,product_core_currency,product_name,product_reviews,product_ratings,product_reviews_5,product_reviews_4,product_reviews_3,product_reviews_2,product_reviews_1,product_bulletpoints,product_url,variation_sku_id,variation_variation_sku,variation_retail_price,variation_sale_price,variation_discount_rate,variation_stock\n")
    else:
        with open('output/'+filename, 'w') as f:
            logging.warning('No data found. Creating new file . . .')
            f.write("sequence,seller_chat_response_rate,seller_name,seller_new_seller,seller_rate,seller_id,seller_ship_on_time,seller_shop_id,seller_time,seller_unit,product_category_0,product_category_1,product_category_2,product_brand_name,product_brand_id,product_pdt_sku,product_core_country,product_core_currency,product_name,product_reviews,product_ratings,product_reviews_5,product_reviews_4,product_reviews_3,product_reviews_2,product_reviews_1,product_bulletpoints,product_url,variation_sku_id,variation_variation_sku,variation_retail_price,variation_sale_price,variation_discount_rate,variation_stock\n")

    counter = 1
    for url in urls:
        #getting the page source
        url = str(url).replace('\"', '')
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        text = soup.prettify()

        #accessing the json data of the product
        if text.find('__moduleData__ = '):
            logging.warning('moduleData found!')
            if text.find('__moduleData__ = ') == -1:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                text = soup.prettify()
                logging.warning('modeluData fixed')

            text = text[text.find('__moduleData__ = '):text.find('var __googleBot__')]
            text = text.replace('__moduleData__ = ',"")
            text = text[:-6]
            if text != '':
                jtext = json.loads(text)
                logging.warning("Getting product_ID "+str(jtext['data']['root']['fields']['tracking']['pdt_sku'])+" data . . .")
                #sku level data >> product level
                #process: get number of variations first then create data for each variation
                skuCount = 0
                skus = jtext['data']['root']['fields']['skuInfos']
                for sku in skus.values():
                    sequence = skuCount
                    skuCount = skuCount + 1
                    if str(sku['dataLayer']['pdt_sku']):
                        variation_sku_id = str(sku['dataLayer']['pdt_sku'])
                    else:
                        variation_sku_id = 'null'

                    if str(sku['dataLayer']['pdt_simplesku']):
                        variation_variation_sku = str(sku['dataLayer']['pdt_simplesku'])
                    else:
                        variation_variation_sku = 'null'

                    if 'originalPrice' in sku['price']:
                        variation_retail_price = str(sku['price']['originalPrice']['value'])
                    else:
                        variation_retail_price = 'null'

                    if str(sku['price']['salePrice']['value']):
                        variation_sale_price = str(sku['price']['salePrice']['value'])
                    else:
                        variation_sale_price = 'null'

                    if 'discount' in sku['price']:
                        variation_discount_rate = str(sku['price']['discount'])
                        variation_discount_rate = "\""+variation_discount_rate+"\""
                    else:
                        variation_discount_rate = 'null'

                    if str(sku['stockList'][0]['stoock']):
                        variation_stock = str(sku['stockList'][0]['stoock'])
                    else:
                        variation_stock = 'null'


                    #product / seller level
                    if 'value' in jtext['data']['root']['fields']['seller']['chatResponsiveRate']:
                        seller_chat_response_rate = str(jtext['data']['root']['fields']['seller']['chatResponsiveRate']['value'])
                    else:
                        seller_chat_response_rate = 'null'

                    if 'name' in jtext['data']['root']['fields']['seller']:
                        seller_name = str(jtext['data']['root']['fields']['seller']['name'])
                    else:
                        seller_name = 'null'

                    if 'newSeller' in jtext['data']['root']['fields']['seller']:
                        seller_new_seller = str(jtext['data']['root']['fields']['seller']['newSeller'])
                    else:
                        seller_new_seller = 'null'
                    if 'rate' in jtext['data']['root']['fields']['seller']:
                        seller_rate = str(jtext['data']['root']['fields']['seller']['rate'])
                    else:
                        seller_rate = 'null'

                    if 'sellerId' in jtext['data']['root']['fields']['seller']:
                        seller_id = str(jtext['data']['root']['fields']['seller']['sellerId'])
                    else:
                        seller_id = 'null'

                    if 'value' in jtext['data']['root']['fields']['seller']['shipOnTime']:
                        seller_ship_on_time = str(jtext['data']['root']['fields']['seller']['shipOnTime']['value'])
                    else:
                        seller_ship_on_time = 'null'

                    if 'shopId' in jtext['data']['root']['fields']['seller']:
                        seller_shop_id = str(jtext['data']['root']['fields']['seller']['shopId'])
                    else:
                        seller_shop_id = 'null'

                    if 'time' in jtext['data']['root']['fields']['seller']:
                        seller_time = str(jtext['data']['root']['fields']['seller']['time'])
                    else:
                        seller_time = 'null'

                    if 'unit' in jtext['data']['root']['fields']['seller']:
                        seller_unit = str(jtext['data']['root']['fields']['seller']['unit'])
                    else:
                        seller_unit = 'null'

                    #count plt_categories
                    pdtCount = len(jtext['data']['root']['fields']['Breadcrumb'])-1
                    product_category_0 = 'null'
                    product_category_1 = 'null'
                    product_category_2 = 'null'

                    if pdtCount == 1:
                        product_category_0 = str(jtext['data']['root']['fields']['Breadcrumb'][0]['title'])
                        product_category_1 = 'null'
                        product_category_2 = 'null'
                    elif pdtCount == 2:
                        product_category_0 = str(jtext['data']['root']['fields']['Breadcrumb'][0]['title'])
                        product_category_1 = str(jtext['data']['root']['fields']['Breadcrumb'][1]['title'])
                        product_category_2 = 'null'
                    elif pdtCount >= 3:
                        product_category_0 = str(jtext['data']['root']['fields']['Breadcrumb'][0]['title'])
                        product_category_1 = str(jtext['data']['root']['fields']['Breadcrumb'][1]['title'])
                        product_category_2 = str(jtext['data']['root']['fields']['Breadcrumb'][2]['title'])

                    if 'brand_name' in jtext['data']['root']['fields']['tracking']:
                        product_brand_name = str(jtext['data']['root']['fields']['tracking']['brand_name'])
                    else:
                        product_brand_name = 'null'

                    if 'brand_id' in jtext['data']['root']['fields']['tracking']:
                        product_brand_id = str(jtext['data']['root']['fields']['tracking']['brand_id'])
                    else:
                        product_brand_id = 'null'

                    if 'pdt_sku' in jtext['data']['root']['fields']['tracking']:
                        product_pdt_sku = str(jtext['data']['root']['fields']['tracking']['pdt_sku'])
                    else:
                        product_pdt_sku = 'null'

                    if 'country' in jtext['data']['root']['fields']['tracking']['core']:
                        product_core_country = str(jtext['data']['root']['fields']['tracking']['core']['country'])
                    else:
                        product_core_country = 'null'

                    if 'currencyCode' in jtext['data']['root']['fields']['tracking']['core']:
                        product_core_currency = str(jtext['data']['root']['fields']['tracking']['core']['currencyCode'])
                    else:
                        product_core_currency = 'null'

                    if 'pdt_name' in jtext['data']['root']['fields']['tracking']:
                        product_name = str(jtext['data']['root']['fields']['tracking']['pdt_name'])
                        product_name = "\""+str(product_name)+".\""
                    else:
                        product_name = 'null'

                    if 'rateCount' in jtext['data']['root']['fields']['review']['ratings']:
                        product_reviews = str(jtext['data']['root']['fields']['review']['ratings']['rateCount'])
                    else:
                        product_reviews = 'null'

                    if 'average'in jtext['data']['root']['fields']['review']['ratings']:
                        product_ratings = str(jtext['data']['root']['fields']['review']['ratings']['average'])
                    else:
                        product_ratings = 'null'

                    if str(jtext['data']['root']['fields']['review']['ratings']['scores'][0]):
                        product_reviews_5 = str(jtext['data']['root']['fields']['review']['ratings']['scores'][0])
                    else:
                        product_reviews_5 = 'null'

                    if str(jtext['data']['root']['fields']['review']['ratings']['scores'][1]):
                        product_reviews_4 = str(jtext['data']['root']['fields']['review']['ratings']['scores'][1])
                    else:
                        product_reviews_4 = 'null'

                    if str(jtext['data']['root']['fields']['review']['ratings']['scores'][2]):
                        product_reviews_3 = str(jtext['data']['root']['fields']['review']['ratings']['scores'][2])
                    else:
                        product_reviews_3 = 'null'

                    if str(jtext['data']['root']['fields']['review']['ratings']['scores'][3]):
                        product_reviews_2 = str(jtext['data']['root']['fields']['review']['ratings']['scores'][3])
                    else:
                        product_reviews_2 = 'null'

                    if str(jtext['data']['root']['fields']['review']['ratings']['scores'][4]):
                        product_reviews_1 = str(jtext['data']['root']['fields']['review']['ratings']['scores'][4])
                    else:
                        product_reviews_1 = 'null'

                    if 'highlights' in jtext['data']['root']['fields']['product']:
                        product_bulletpoints = str(jtext['data']['root']['fields']['product']['highlights'])
                        product_bulletpoints = "\""+str(product_bulletpoints)+".\""
                    else:
                        product_bulletpoints = 'null'

                    if 'link' in jtext['data']['root']['fields']['product']:
                        product_url = str(jtext['data']['root']['fields']['product']['link'])
                    else:
                        product_url = 'null'


                    output_data = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(sequence,seller_chat_response_rate,seller_name,seller_new_seller,seller_rate,seller_id,seller_ship_on_time,seller_shop_id,seller_time,seller_unit,product_category_0,product_category_1,product_category_2,product_brand_name,product_brand_id,product_pdt_sku,product_core_country,product_core_currency,product_name,product_reviews,product_ratings,product_reviews_5,product_reviews_4,product_reviews_3,product_reviews_2,product_reviews_1,product_bulletpoints,product_url,variation_sku_id,variation_variation_sku,variation_retail_price,variation_sale_price,variation_discount_rate,variation_stock)

                    #saving data
                    # json_text = 'data_'+str(counter)+'.json'
                    if sequence != 0:
                        with open('output/'+filename, 'a') as f:
                            f.write(output_data)
                            f.close()
            else:
                pass
        else:
            logging.warning("No moduleData! Skipping . . .")

        time.sleep(5)
        logging.warning('Accessing next product . . .')
        counter += 1


if __name__ == '__main__':
    main()