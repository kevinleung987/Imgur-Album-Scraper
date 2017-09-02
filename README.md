# Imgur Album Scraper
Python Imgur Scraper that scrapes all the images of an Imgur album into a folder. If you have already downloaded the album in the past, duplicate images won't be overwritten and only new additions to the album will be downloaded. Should work with any kind of file hosted inside of an Imgur album.
# Instructions/How to Use
- Install Python 3
- Install the Requests library by running the following command.
```sh
$ python pip -m install requests
```
- Replace client_id with your own Imgur API Application Client ID, you can acquire one in this page https://api.imgur.com/oauth2/addclient
- Modify directory_name to what you want, the directory will be created and the album folders will be generated within that directory. An empty string will generate album folders in the same directory as the Python file.
- Place main.py where you want the album directories to be stored and run it.
- Input the Imgur album links that you want to download.

License
----
MIT