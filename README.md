# Image-Service
This microservice uses Bing's Image Search to retrieve links to images with a given keyword. 

Make a POST request to http://khourye.pythonanywhere.com/users. 

Example:

arguments = {'api_key': 'chickens456', 'keyword': 'tree', 'num_images': 2}
response = requests.post(api_url, json=arguments)
