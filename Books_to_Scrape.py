import requests
from bs4 import BeautifulSoup

# List of items to recover
list_item_produit = [
    "product_page_url",
    "universal_product_code(upc)",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

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

    print("\nHTTP_of_url")

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        return soup, response.status_code, response.encoding
    else:
        return "", response.status_code, "utf-8"


def BeautifulSoup_extract(tag, html_data):
    ''' Extract all the data include inside 'tag' in a BeautifulSoup object.
        For each tag find, the data is append in a list which is return by this function.
    '''

    print("\nBeautifulSoup_extract")

    extract_all_tags = html_data.findAll(tag)
    tag_list = []
    for extract_tag in extract_all_tags:
        tag_list.append(extract_tag.get_text())

    return tag_list


def write_list_in_file(list_to_save, file, codec):
    ''' Each element of the "list_to_save" is save on a row of the "file".
    '''

    print("\nwrite_list_in_file")

    with open(file, "w", encoding=codec) as open_file:
        for element_number in range(len(list_to_save)):
            open_file.write(";".join(list_to_save[element_number]) + "\n")


def find_url_book_category():
    ''' From the Books_to_Srape homepage site, retrieve all the url for each book category.
    '''

    print("\nfind_url_book_category")

    url_home_page ="http://books.toscrape.com/"
    soup, status_code, codec = HTTP_of_url(url_home_page)

    url_book_category_list = []

    # For this present release of code, this function return a specific url (link to a book)
    url_book_category_list.append("http://books.toscrape.com/catalogue/category/books/travel_2/index.html")

    return url_book_category_list


def find_url_book(url):
    ''' For this book category, retrieve all the url of all this king of book
    '''

    print("\nfind_url_book")

    url_book_list = []

    # For this present release of code, this function return a specific url (link to a book)
    url_book_list.append("http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")

    return url_book_list


def retrieve_data_listed_in_item_produit(url_book):
    ''' This function retrieve the data listed in "list_item_produit" from the url_book
        and send this data in a dictionary.
        In case of trouble, the Dict_item_produit is only filled with the url_book,
        the others fields are set with "0" by default.
        The codec used in the page is also return.
    '''

    print("\nretrieve_data_listed_in_item_produit")

    data_dict = Dict_item_produit.copy()
    data_dict["product_page_url"] = url_book

    soup, status_code, codec = HTTP_of_url(url_book)

    if status_code == requests.codes.ok:
        # Some data are contains between the tag '<td>   </td>'
        data_list = BeautifulSoup_extract("td", soup)

        data_dict["universal_product_code(upc)"] = data_list[0]
        data_dict["price_excluding_tax"] = data_list[2]
        data_dict["price_including_tax"] = data_list[3]
        # number_available have the following format "In stock (x available)", so we extract the value
        # Before, we check that the data are in the good format
        number_available = ""
        if len(data_list[5]) > len("In stock ( available)"):
            print ("\ndata_list[5][0:len(\"In stock\")] = "
                    + "\"" + data_list[5][0:len("In stock")] + "\"")
            print("\nrange(len(\"In stock (\"), len(data_list[5])):\t"
                    + str(range(len("In stock ("), len(data_list[5]))))

            if data_list[5][0:len("In stock")] == "In stock":
                print("\n\tdata_list[5][{}] = {}".format(i, number_available))
                for i in range(len("In stock ("), len(data_list[5])):
                    if data_list[5][i] in [0-9]:
                        number_available += data_list[5][i]
                    else:
                        break
                number_available = int(number_available)
                
        data_dict["number_available"] = number_available
        print(data_dict)

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
        data_list = []
        data_list.append(list_item_produit)

        for url_book in url_of_this_category:
            # For each book, retrieve the data listed in "list_item_produit".
            print("\n\n" + str(url_book))
            data_dict, codec = retrieve_data_listed_in_item_produit(url_book)

            data_list.append([])
            for element in list_item_produit:
                data_list[-1].append(data_dict[element])

            # Then, these data are saved in a .csv file (one file by book category)
            write_list_in_file(data_list, "test.csv", codec)


if __name__ == "__main__":
    main()
