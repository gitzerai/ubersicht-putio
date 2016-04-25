# [Ubersicht](http://tracesof.net/uebersicht/) meets [Put.io](https://put.io/)

Have info about your latest TV Shows available at put.io right on your Mac desktop.

## Requirements

- [Ubersicht MacOSX App](http://tracesof.net/uebersicht/) 
- Python >= 2.7 
- requests python package installed. If you do not have it installed, please follow http://docs.python-requests.org/en/master/user/install/ 

## Installation

- clone this repository somewhere on your disk
- copy the putio.widget folder into your Ubersicht widgets folder
- edit the get-data.py info with your credentials and your folder RSS
- (optional) edit index.coffee file styles based on your placement requirements

## Configuration

- PUTIO_FOLDER_RSS - your put.io folder RSS link
- PUTIO_USERNAME - your username to put.io service
- PUTIO_PASSWORD - your password to put.io service
- FROM_DATE_DAY_OFFSET = count of how many days in the back should be considered as "latest TV Shows"
- SHOULD_VALIDATE_DATE - boolean (True/False) whether the show download date should be considered
- TIME_FORMAT - time format shown in the widget header
- ITEM_LIMIT - number of items to be shown before 'more' information appears

## Screenshots
![Desktop Screenshot 1](https://github.com/gitzerai/ubersicht-putio/blob/master/screenshot.png)
