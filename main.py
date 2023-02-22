import requests, csv
from bs4 import BeautifulSoup

url = "https://migrate.njparcels.com/property/"

def write_csv(data_list, property_number):
    # Create the csv file
    f = open(f'property{property_number}.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    # Write header row
    header_row = ["Block","Addresses in Block","Extra"]
    writer.writerow(header_row)

    # Write rows
    for data in data_list:
        writer.writerow(data)

    # Close the file
    f.close()


def get_page(property_number):
    # Get the page
    content = requests.get(url + str(property_number)).content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def get_data(soup):
    data = []
    if not soup:
        return data

    # Get the table
    table = soup.find("table")
    if not table:
        return data

    # Get the rows
    trs =  table.find_all("tr")
    if not trs:
        return data

    # Append the data
    for row in trs:
        tds = row.find_all("td")
        if not tds:
            continue
        data.append([tds[0].text, tds[1].text, tds[2].text])
    return data


if __name__ == "__main__":
    print("This scripts gets data about properties from page https://migrate.njparcels.com/property/")
    try:
        while True:
            property_number = input("Enter property number: ")
            page = get_page(property_number)
            data = get_data(page)
            if data:
                write_csv(data, property_number)

            else:
                print("The given property number return no data.")

            print("Data has been proccesed. Press enter to get another property data \n")
            input("")

    except KeyboardInterrupt:
        print("Program is closing")
