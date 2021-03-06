#!/usr/bin/env python
'''
MIT License

Copyright (c) 2017 Kevin Leung

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
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
