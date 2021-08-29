import requests
URL = 'https://mk0vcwebsiteaupg2jli.kinstacdn.com/wp-content/uploads/2019/09/responsive-background-example.png'
img_data = requests.get(URL, verify = False).content

with open("test" , "wb") as handler:
    handler.write(img_data)