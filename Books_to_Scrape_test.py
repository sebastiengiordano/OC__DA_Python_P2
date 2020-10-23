import requests
from bs4 import BeautifulSoup

# List of items to recover
list_item_produit = [
    'product_page_url',
    'universal_product_code(upc)',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
]

# Dictionary of items to recover

Dict_item_produit = {
    'product_page_url': '0',
    'universal_product_code(upc)': '0',
    'title': '0',
    'price_including_tax': '0',
    'price_excluding_tax': '0',
    'number_available': '0',
    'product_description': '0',
    'category': '0',
    'review_rating': '0',
    'image_url': '0'
}

def HTTP_of_url(url):
    ''' This function return :
            * the BeautifulSoup object come from the url_book,
            * the status_code "OK",
            * and the codec used in the page.
        In case of error, the return tuple is filled with
            * an empty string,
            * the "error code of the requests response",
            * and the 'utf-8' codec.
    '''

    print("HTTP_of_url")

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup, response.status_code, response.encoding
    else:
        return "", response.status_code, "utf-8"


def BeautifulSoup_extract(tag, html_data):
    ''' Extract all the data include inside 'tag' in a BeautifulSoup object.
        For each tag find, the data is append in a list which is return by this function.
    '''

    print("BeautifulSoup_extract")

    extract_all_tags = html_data.findAll(tag)
    tag_list = []
    for extract_tag in extract_all_tags:
        tag_list.append(extract_tag)

    return tag_list


def write_list_in_file(list_to_save, file, codec):
    ''' Each element of the "list_to_save" is save on a row of the "file".
    '''

    print("write_list_in_file")

    with open(file, "w", encoding=codec) as open_file:
        for element_number in range(len(list_to_save)):
            open_file.write(";".join(list_to_save[element_number]) + "\n")


def find_url_book_category():
    ''' From the Books_to_Srape homepage site, retrieve all the url for each book category.
    '''

    print("find_url_book_category")

    url_home_page ='http://books.toscrape.com/'
    soup, status_code, codec = HTTP_of_url(url_home_page)

    url_book_category_list = []

    # For this present release of code, this function return a specific url (link to a book)
    url_book_category_list.append('http://books.toscrape.com/catalogue/category/books/travel_2/index.html')

    return url_book_category_list


def find_url_book(url):
    ''' For this book category, retrieve all the url of all this king of book
    '''

    print("find_url_book")

    url_book_list = []

    # For this present release of code, this function return a specific url (link to a book)
    url_book_list.append('http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html')

    return url_book_list


def retrieve_data_listed_in_item_produit(url_book):
    ''' This function retrieve the data listed in "list_item_produit" from the url_book
        and send this data in a dictionary.
        In case of trouble, the Dict_item_produit is filled with the url_book, the others fields are set by '0'.
        The codec used in the page is also return.
    '''

    print("retrieve_data_listed_in_item_produit")

    data_dict = Dict_item_produit.copy

    soup, status_code, codec = HTTP_of_url(url_book)

    if status_code == requests.codes.ok:
        # The data are contains between the tag '<td>   </td>'
        data_list = BeautifulSoup_extract('td', soup)
    else:
        data_dict['product_page_url'] = url_book

    return data_dict, codec


def main():
    ''' main function which performed the following actions:
            from the Books_to_Srape homepage site, retrieve all the url for each book category.
            For each book category, retrieve all the url for all this king of book:
                For each book, retrieve the data listed in "list_item_produit".
                Then, these data are saved in a .csv file (one file by book category)
    '''

    # from the Books_to_Srape homepage site, retrieve all the url for each book category.
    url_book_category = find_url_book_category()

    # For each book category, retrieve all the url for all this king of book.
    for url in url_book_category:
        url_of_this_category = find_url_book(url)

        for url_book in url_of_this_category:
            # For each book, retrieve the data listed in "list_item_produit".
            data_list, codec = retrieve_data_listed_in_item_produit(url_book)

            data_list.insert(0, list_item_produit)
            # Then, these data are saved in a .csv file (one file by book category)
            write_list_in_file(data_list, "test.csv", codec)


if __name__ == "__main__":
    url = 'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'
    soup, status_code, codec = HTTP_of_url(url)

    print(str(BeautifulSoup_extract('td', soup)))
