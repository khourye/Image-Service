import requests


def getImages(keyword: str, num_images: int) -> list:
    """ Takes a keyword and number of images
        Returns a list of image urls """

    subscription_key = 'aef1f71d9fcc4be187ceab684fc3e340'
    endpoint = 'https://api.bing.microsoft.com/v7.0/images/search'

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": keyword, "license": "public", "imageType": "photo", "count": num_images, "safeSearch": 'moderate'}

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # use set to ensure no duplicate urls
    urls = set()
    for image in search_results['value']:
        urls.add(image['contentUrl'])

    return list(urls)

