from os import path

from utility import (find_url_of_book_category,
                     find_url_book,
                     retrieve_data_listed_in_item_produit,
                     copy_picture,
                     write_list_in_file,
                     project_path)

def main():
    ''' main function which performed the following actions:
            from the Books_to_Srape homepage site, retrieve all the url for each book category.
            For each book category, retrieve all the url for all this king of book:
                For each book, retrieve the data listed in "list_item_produit".
                Then, these data are saved in a .csv file (one file by book category)
    '''

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

    # DEBUG_MODE: Uncomment the 2 lines below in order to take
    # only few category of book for each category.
    # count = 0
    # count2 = 0
    
    # from the Books_to_Srape homepage site, retrieve all the url for each book category.
    url_book_category = find_url_of_book_category()

    # For each book category, retrieve all the url for all this king of book.
    for url, category in url_book_category:
        # DEBUG_MODE: Uncomment the 3 lines below in order to take
        # only few category of book for each category.
        # count += 1
        # if count > 2:
        #     break
        url_of_this_category = find_url_book(url, [])

        data_list = []
        # Add of header for .csv file
        data_list.append(list_item_produit)

        for url_book in url_of_this_category:
            # For each book, retrieve the data listed in "list_item_produit".
            data_dict = retrieve_data_listed_in_item_produit(url_book, category)
            # DEBUG_MODE: Uncomment the 4 lines below in order to take
            # only few book for each category.
            # count2 += 1
            # if count2 > 5:
            #     count2 = 0
            #     break

            # The collected data are stored in a list
            data_list.append([])
            for element in list_item_produit:
                data_list[-1].append(data_dict[element])
            
            # And the picture of the book is stored in a folder
            # named with the category name.
            copy_picture(
                    data_dict["image_url"],
                    path.join(project_path, "..\\Picture", category + "\\"),
                    data_dict["title"].replace(": ", "_").replace(":", "_") + data_dict["image_url"][-4:])

        # Then, these data are saved in a .csv file (one file by book category).
        write_list_in_file(data_list, "..\\CSV\\" + category + ".csv")


################
# Run the code #
################
if __name__ == "__main__":
    main()
