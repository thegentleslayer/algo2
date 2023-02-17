'''
Importation blibliothèques nécessaire
'''
from bs4 import BeautifulSoup 
from pprint import pprint
import requests 
import csv


def filtre_url(energy, brand, km_max, km_min, page, price_max, price_min, year_max, year_min) :

    url_site = 'https://www.lacentrale.fr/listing?energies={energy_url}&makesModelsCommercialNames={brand_url}&mileageMax={km_max_url}&mileageMin={km_min_url}&options=&page={next_page}&priceMax={price_max_url}&priceMin={price_min_url}&yearMax={year_max_url}&yearMin={year_min_url}'
    url = url_site.format(energy_url = energy, brand_url = brand, km_max_url = km_max, km_min_url = km_min, next_page = page, price_max_url = price_max, price_min_url = price_min, year_max_url = year_max, year_min_url = year_min) #line is for make the filter & remplace the var 
    print(url)
    return url

def scrap_listing(url) :
    '''
    Fonction permettant de récuperer le contenu html de la page en utilisant l'url

    '''
    re = requests.get(url)
    print(re)
    return re.text

def scrap(html_page, csv_writer) :
    '''
    Fonction scrap permet d'extraire tous les élements "div" de la page web qui ont une class CSS spécifique, en utilisant la blibliothèque BeautifulSoup

    '''
    soup = BeautifulSoup(html_page, 'html.parser')
    cards = soup.find_all("div",'Vehiculecard_Vehiculecard_cardBody') #On scrap toutes les cards de tout les véhicules de la page
    
    for card in cards :     #On scrap qu'une seul card à la fois
    
        car_name = card.find("h3","Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")      #On récupère l'intégralité du nom donné à chaque voiture
        full_car_name = car_name.get_text()
        brand_car = ""
        name_start = 0      #On créer une variable d'ittération
        while full_car_name[name_start] != " " :     #On va isoler le nom de la marque et le nom du modèle de chaque voiture
            brand_car += full_car_name[name_start]
            name_start += 1
        print(brand_car)    
        
        model_car = ""
        for start2 in range(name_start+1, len(full_car_name)) :  
            model_car += full_car_name[start2]
        print(model_car)
        

        
        motor = card.find("div","Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2")       #On récupère l'energie de chaque voiture
        motorbis = motor.get_text()
        print(motorbis)

        
        elem_car_list = []
        for elem in card.find_all("div","Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2") :     #On récupère tous les élements de la voitures qui sont collés
            elem_text = elem.get_text()
            elem_car_list.append(elem_text)
            print(elem_text.replace(" ", "").replace("km", '').replace('\xa0', ''))
        car_km_new = elem_car_list[1].replace(" ", "").replace("km", '').replace('\xa0', '') #On transforme les km en int avec la fonction .replace
        car_km_new = int(car_km_new)
        elem_car_list[1] = car_km_new

            
            
        
        #On scrap le prix de chaque véhicule
        price = card.find("span","Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
        pricebis = price.get_text()
        #Transformation des euros en int 
        price_new = pricebis.replace(' ','').replace('€', '')
        pricebis = price_new
        print(int(pricebis))
        print ("-------------------------------------------------")

        csv_script([brand_car,model_car,motorbis,elem_car_list[0],elem_car_list[1],elem_car_list[2],elem_car_list[3],pricebis],csv_writer) 


def csv_script(data,csv_writer) :
    '''
    La fonction csv_script permet prend deux arguments en entrée: data et csv_writer. Elle a pour but d'écrire les données de data dans un fichier CSV à l'aide de l'objet csv_writer
    
    '''
    csv_writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])
    
def error(soup) :
    """
    Fonction qui va permettre d'éviter les erreurs

    """
    the_error_of_page = soup.find('span',"Text_Text_text Text_Text_headline2")
    the_error_of_pagebis = the_error_of_page.get_text()
    the_error_of_page = the_error_of_pagebis.replace(' ','').replace('\xa0', '')
    the_error_of_page = int(the_error_of_page)
    return(the_error_of_page)
    
def main() :

    csv_document = open('file_test.csv', 'w')   #On ouvre le document csv
    csv_writer = csv.writer(csv_document)
    csv_writer.writerow(['Brand', 'Model', 'Motor', 'Year', 'mileage', 'Box', 'Energy', 'Price'])
    fuel = "dies"
    model = "PEUGEOT"
    url_request = filtre_url(fuel, model, '12000', '10000', 1, '50000', '10000', '2021', '1980')
    html_page = scrap_listing(url_request)
    soup = BeautifulSoup(html_page, 'html.parser')
    the_error_of_page = error(soup)
    
    if the_error_of_page > 0 :
        for one_page in range (1,11):   #On créer une boucle pour pouvoir scraper 10 pages
            url_request = filtre_url(fuel, model, '12000', '10000', str(one_page), '50000', '10000', '2021', '1980') #On lance la requête qu'on a spécifié
            html_page = scrap_listing(url_request)  
            scrap(html_page, csv_writer)
    else:
        print("error 0 annonce")
    csv_document.close()



main()  #Permet d'éxecuter le code en toute sécurité
