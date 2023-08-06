import gdown
import requests
import yaml

def download_weights(id_or_url, cached=None, md5=None, quiet=False):
    if id_or_url.startswith('http'):
        url = id_or_url
    else:
        url = 'https://drive.google.com/uc?id={}'.format(id_or_url)

    return gdown.cached_download(url=url, path=cached, md5=md5, quiet=quiet)

def download_config(id):
    url = 'https://raw.githubusercontent.com/pbcquoc/config/master/vietvocoder/{}.yml'.format(id)
    r = requests.get(url)
    config = yaml.safe_load(r.text)
    return config
