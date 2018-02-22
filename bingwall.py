#!/usr/bin/env python2

import urllib, urllib2, json, sys
from os.path import join, isfile, exists
from os import makedirs


IMAGE_DIR = '/home/jens/Pictures/background/'

def print_help_message():
    msg = 'Usage: ' + sys.argv[0] + ' [set background command]'
    print(msg)
    sys.exit()


def downloadimage(url, set_background_cmd=''):
    file_name = url.split('/')[-1]
    file_path = join(IMAGE_DIR, file_name)
    if not exists(IMAGE_DIR):
        makedirs(IMAGE_DIR)

    if not isfile(file_path):
        print('Downloading ' + url)
        urllib.urlretrieve(url, file_path)

    if '' != set_background_cmd.strip():
        print('Set background: ' +  set_background_cmd + ' ' + file_path)
        import subprocess
        subprocess.call(set_background_cmd + " " + file_path, shell=True)


def main():
    background_set_cmd = ''
    if len(sys.argv) == 1:
        flag_download_only= True
    elif len(sys.argv) == 2:
        if '-h' == sys.argv[1] or '--help' == sys.argv[1]:
            print_help_message()
        else:
            set_background_cmd = sys.argv[1]
    else:
        print('Invalid arguments!')
        print_help_message()

    # See http://stackoverflow.com/questions/10639914/is-there-a-way-to-get-bings-photo-of-the-day
    url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'

    try:
        response = urllib2.urlopen(url)
        json_data = json.load(response)

        if 'images' in json_data:
            images = json_data['images']
        else:
            sys.exit('Error in JSON')

        url = 'http://www.bing.com' + images[0]['url']
        downloadimage(url, set_background_cmd)

    except urllib2.HTTPError, e:
        print('Error ' + str(e.code))
    except urllib2.URLError, e:
        print('Error')


if __name__ == '__main__':
    main()
