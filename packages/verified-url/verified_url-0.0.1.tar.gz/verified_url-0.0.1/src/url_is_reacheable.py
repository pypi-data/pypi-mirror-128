#! /usr/bin/python
import urllib
import urllib.request


def check(url):
    r = dict()
    if url == '':
        r['url'] = url
        r['available'] = False
        r['status_code'] = 400
        print('URL cannot be empty')
    else:
        r = is_reacheable(url)

    print("Result check URL: " + str(r))
    return r


def is_reacheable(url):
    r = dict()

    try:
        url_checker = urllib.request.urlopen(url)
    except ValueError as err:
        r['url'] = url
        r['available'] = False
        r['status_code'] = 400
    except urllib.error.HTTPError as err:
        r['url'] = url
        r['available'] = False
        r['status_code'] = err.code
    except urllib.error.URLError as err:
        r['url'] = url
        r['available'] = False
        r['status_code'] = err.code.toString()
    else:
        r['url'] = url
        r['available'] = True
        r['status_code'] = url_checker.getcode()
    return r