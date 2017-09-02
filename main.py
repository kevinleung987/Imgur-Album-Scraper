import requests
import os
import shutil

client_id = ''  # Imgur application Client ID, fill this in.
directory_name = 'Imgur Albums\\'  # Directory for the images to be stored


def scrape(album_id):
    ''' (str) -> list of str
    Given an Imgur album ID, scrapes all the images within the album into a
    folder. Returns a list containing all the links that were scraped.
    '''
    # Seperate directory for each album's images to be stored in
    directory = directory_name+album_id+'\\'
    if not os.path.exists(directory):
        os.makedirs(directory)  # Creates the full directory for the album
    imageList = []
    print('Loading Album: '+album_id)
    link = 'https://api.imgur.com/3/album/' + album_id
    header = {'Authorization': 'Client-Id '+client_id}
    album = requests.get(link, headers=header).json()
    if not album['success']:
        return album['data']['error']
    # Scrape image links from the album
    for x in range(len(album['data']['images'])):
        imageList.append(album['data']['images'][x]['link'])
    # Downloads each image and writes to disk
    for image in imageList:
        download = requests.get(image, stream=True)
        with open(directory+image[image.find('com/')+4:], 'wb') as outFile:
            shutil.copyfileobj(download.raw, outFile)
    return imageList
