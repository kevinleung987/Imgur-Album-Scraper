import requests
import os
import shutil

client_id = 'e36ce095653e924'  # Imgur application Client ID, fill this in
# Change directory_name into an empty string for images to be stored in the
# same directory as the python file
directory_name = 'Imgur Albums\\'


def scrape(album_id):
    ''' (str) -> list of str
    Given an Imgur album ID, scrapes all the images within the album into a
    folder. Returns a list containing all the links that were scraped.
    '''
    # Seperate directory for each album's images to be stored in
    directory = directory_name+album_id+'\\'
    scraped = []
    imageList = []
    print('Downloading Album: '+album_id)
    # Loading the album with Requests
    link = 'https://api.imgur.com/3/album/' + album_id
    header = {'Authorization': 'Client-Id '+client_id}
    album = requests.get(link, headers=header).json()
    if not album['success']:
        raise Exception(album['data']['error'])
    # Scrape image links from the album
    for image in album['data']['images']:
        imageList.append(image['link'])
    # Creates the full directory for the album
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Downloads each image and writes to disk
    for image in imageList:
        download = requests.get(image, stream=True)
        imagepath = directory+image[image.find('com/')+4:]
        # Only download the image if it does not already exist in the folder
        if not os.path.isfile(imagepath):
            print('Downloaded '+imagepath)
            with open(imagepath, 'wb') as outFile:
                shutil.copyfileobj(download.raw, outFile)
            scraped.append(image)
    return scraped

if __name__ == '__main__':
    while True:
        link = input('Input a Imgur album link: ')
        if '/a/' in link:
            scrape(link[link.find('/a/')+3:])
        elif '/gallery/' in link:
            scrape(link[link.find('/gallery/')+9:])
        else:
            print('Invalid link! Example: https://imgur.com/a/cusMo')
