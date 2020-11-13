from os import path
import csv
import urllib.request

import requests
from bs4 import BeautifulSoup

###################
# Global variable #
###################
project_path = path.dirname(path.abspath(__file__))


#############
# Functions #
#############
def find_url_of_book_category():
    ''' From the Books_to_Srape homepage site, retrieve all the url for each book category.
    '''

    url_book_category_list = []

    url_home_page ="http://books.toscrape.com/"
    soup, status_code = HTTP_of_url(url_home_page)

    url_book_category_tag = soup.findAll('a', href=True)

    for extract_url_category in url_book_category_tag:
        url = extract_url_category['href']
        if url[0:len("catalogue/category/books/")] == "catalogue/category/books/":
            url_book_category_list.append([])
            url_book_category_list[-1].append(url_home_page + url)

            category = extract_url_category.text.replace("\n", "").strip()
            url_book_category_list[-1].append(category)

    return url_book_category_list


def find_url_book(url, url_book_list = []):
    ''' For this book category, retrieve all the url of all this king of book
    '''

    response = requests.get(url)

    if response.ok:
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, "html.parser")
        extract_all_h3 = soup.findAll('h3')

        # Find all the url of the books in this page
        for extract_h3 in extract_all_h3:
            url_book = "http://books.toscrape.com/catalogue/" + extract_h3.find('a')['href'].replace("../", "")
            url_book_list.append(url_book)

        # If there is another page of books for this category, the url of the next page is find.
        # url of the next page is inside 'ul' tag with attribute 'pager'
        find_all_ul = soup.findAll('ul')
        count=0
        for ul in find_all_ul:
            ul_get_class = ul.get('class')
            if not(ul_get_class == None) and "pager" in ul_get_class :
                find_all_li = ul.findAll('li')
                for li in find_all_li:
                    if li.get('class')[0] == "next":
                        extract_next_page = li.find('a')['href']

                        # url need to be complete with the beginning of the current page
                        for i in range(-1, -20, -1):
                            if url[i] == "/":
                                url_start_end = i + 1
                                break
                        url_start = url[0:url_start_end]
                        extract_next_page = url_start + extract_next_page
                        url_book_list = find_url_book(extract_next_page, url_book_list)

    return url_book_list


def HTTP_of_url(url):
    ''' This function return :
            * the BeautifulSoup object come from the url,
            * the status_code "OK".
        In case of error, the return tuple is filled with
            * an empty string,
            * the "error code of the requests response".
    '''

    response = requests.get(url)

    if response.ok:
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, "html.parser")
        return soup, response.status_code
    else:
        return "", response.status_code


def BeautifulSoup_extract(tag, html_data):
    ''' Extract all the data include inside 'tag' in a BeautifulSoup object.
        For each tag find, the data is append in a list which is return by this function.
    '''

    extract_all_tags = html_data.findAll(tag)
    tag_list = []
    for extract_tag in extract_all_tags:
        tag_list.append(extract_tag.get_text())

    return tag_list


def write_list_in_file(list_to_save, file):
    ''' Each element of the "list_to_save" is save on a row of the "file".
    '''

    file_path = path.join(project_path, file)

    with open(file_path, "w", encoding="UTF-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in list_to_save:
            spamwriter.writerow(row)

        # for element_number in range(len(list_to_save)):
        #     open_file.write(";".join(list_to_save[element_number]) + "\n")


def retrieve_data_listed_in_item_produit(url_book, category, status_code_nok_counter = 0):
    ''' This function retrieve the data listed in "list_item_produit" from the url_book
        and send this data in a dictionary.
        In case of trouble, the Dict_item_produit is only filled with the url_book,
        the others fields are set with "0" by default.
    '''

    # Dictionary of items to recover
    Dict_item_produit = {
        "product_page_url": "0",
        "universal_product_code(upc)": "0",
        "title": "0",
        "price_including_tax": "0",
        "price_excluding_tax": "0",
        "number_available": "0",
        "product_description": "0",
        "category": "0",
        "review_rating": "0",
        "image_url": "0"
    }

    # Dict_item_produit = Dict_item_produit.copy()
    Dict_item_produit["product_page_url"] = url_book
    Dict_item_produit["category"] = category

    soup, status_code = HTTP_of_url(url_book)

    if status_code == requests.codes.ok:
        # Some data are contains between the tag '<td>   </td>'
        data_list = BeautifulSoup_extract("td", soup)

        Dict_item_produit["universal_product_code(upc)"] = data_list[0]
        Dict_item_produit["price_excluding_tax"] = data_list[2]
        Dict_item_produit["price_including_tax"] = data_list[3]
        # "number_available" have the following format "In stock (x available)", so we extract the value.
        # Before, we check that the data are in the good format
        number_available = ""
        if len(data_list[5]) > len("In stock ( available)"):
            if data_list[5][0:len("In stock")] == "In stock":
                for index in range(len("In stock ("), len(data_list[5])):
                    # if data_list[5][index] in '0123456789':
                    if data_list[5][index] in [str(x) for x in range(0, 10)]:
                        number_available += data_list[5][index]
                    else:
                        break
        Dict_item_produit["number_available"] = number_available
        Dict_item_produit["review_rating"] = data_list[6]


        # "product_description" is contain in twice position, here we take the one in tag 'meta' with the attribute
        # name = "description". The description is in the attribute "content".
        extract_all_meta = soup.findAll('meta')
        for extract_meta in extract_all_meta:
            if extract_meta.get('name') == "description":
                product_description = extract_meta['content'].strip()
                # product_description = extract_meta['content'].replace("\n", "").replace("\t", "")
                # product_description = product_description.strip()
                Dict_item_produit["product_description"] = product_description
                # Dict_item_produit["product_description"] = "\"" + product_description + "\"" 
                break


        # "title" and "image_url" are contain in the tag 'img' (which is inside the tag 'article').
        extract_title = soup.find('article').find('img')

        Dict_item_produit["title"] = extract_title['alt']
        Dict_item_produit["image_url"] = "http://books.toscrape.com/" + extract_title['src'].replace("../", "")

    else:
        status_code_nok_counter += 1
        if status_code_nok_counter > 10:
            print("For " + url_book + "requests never OK.")
        retrieve_data_listed_in_item_produit(url_book, status_code_nok_counter)


    return Dict_item_produit


def copy_picture(url_picture, picture_path, picture_name):
    ''' This function copy the picture from its url (url_picture)
        to the folder "picture_path" with the name "picture_name".
    '''

    picture_path = path.join(project_path, picture_path, picture_name)
    urllib.request.urlretrieve(url_picture, picture_path)
