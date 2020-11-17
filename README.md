<p align="center">
    <br />
    <h1 align="center">WebScrapping of Books to Scrape site</h1>
    <br />
    <h2 align="center">
        This program aims to track book prices at "Books to Scrape" site.
        <br />
    </h2>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [How run this program](#how-run-this-program)
  * [Installation](#installation)
  * [Run the program](#run-the-program)
  * [Additional informations](#additional-informations)
* [Folder structure](#folder-structure)
  * [Folder CSV](#folder-csv)
    * [Open CSV with Excel](#open-csv-with-excel)
  * [Folder Picture](#folder-picture)


<!-- HOW RUN THIS PROGRAM -->
## How run this program

### Installation

1. Created a folder for this project. Then, open a terminal and go to this folder:
```sh
cd "folder project path"
```
2. Clone the repository:
```sh
git clone https://github.com/sebastiengiordano/OC__DA_Python_P2
```
3. Go to folder OC__DA_Python_P2:
```sh
cd OC__DA_Python_P2
```
4. Create a virtual environment:
```sh
python -m venv env
```
5. Activate the virtual environment :
```sh
.\env\Scripts\activate
```
6. From the "requirements.txt" file, install needed packets:
```sh
python -m pip install -r requirements.txt
```

### Run the program
1. Open a terminal and go to the folder OC__DA_Python_P2 (if its not already the case):
```sh
cd "folder project path" & cd OC__DA_Python_P2
```
2. Activate the virtual environment (if its not already the case):
```sh
.\env\Scripts\activate
```
3. Run the program
```sh
python -m Books_to_Scrape
```

### Additional informations
1. During the program processing, in the terminal, you could see the start of treatment of each category of book, and the time since the start of the program.
2. If a book page is not accessible, several attempts are made. If this page is still not accessible, the following message will be displayed:
```sh
For "url of the book" requests never OK.
```
3. At the end, the total processing time will be displayed.


<!-- FOLDER STRUCTURE -->
## Folder structure

From OC__DA_Python_P2 folder, you will find the following folders:
* CSV
* Picture

### Folder CSV
In the folder CSV, you retreive a csv file for each category of book.
These files are named with the category name and contain, for each book, the following informations:
* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

#### Open CSV with Excel
Follow the steps below to use Microsoft Excel to open these csv file:
* Open Microsoft Excel
* Click on the "Data" menu.
* Click on the "From Text" icon
* Navigate to the location of the file that you want to import
    * Click on the filename and then click on the Import button
* The Text Import Wizard - Step 1/3
    * Choose "Delimited" field
    * Choose 65001: Unicode (UTF-8) from the drop-down list "File origin"
* Click on the Next button to display the Text Import Wizard - Step 2/3
    * In "Delimiters", check the box corresponding to the semicolon
    * In "Text qualifier", choose the quotation mark
* Click on the Finish button

### Folder Picture
In the folder Picture, you retreive one folder by category of book.
These folders are named with the category name and contain the picture of the books of that category.
The pictures are named with the title of the corresponding book.