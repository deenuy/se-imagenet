import json, config
import requests
import urllib.request
import urllib.error
import os.path
import os, shutil
import hashlib
import itertools

try:
  shutil.rmtree('images')
except FileNotFoundError:
  pass
os.makedirs('images')

api_key = ""
se_id = ""

def urls_from_google(query):
  r = requests.get(
    'https://customsearch.googleapis.com/customsearch/v1',
    params = {'searchType': 'image', 
              'cx': config.GOOGLE_SE_ID, 
              'key': config.GOOGLE_API_KEY,
              'q': query, 
              'num': 10},
    headers = {'Accept': 'application/json'}
  )
  urls = (x['link'] for x in r.json()['items'])
  return urls

def download_urls(urls):
  for url in urls:
    try:
      r = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
      print(e)
      continue
    with open(os.path.join('images', hashlib.sha1(url.encode('utf-8')).hexdigest()), "wb") as f:
      f.write(r.read())

# Enter keywords for Google image search here
keywords = ('rock', 'stone', 'tree', 'tree,bark', 'brook', 'soil')

if api_key:
  urls = itertools.chain(*map(urls_from_google, keywords))
else:
  print("No API keys found, using sample urls.")
  print("Type your api key and search engine id into download_images.py to use Google image search.")
  urls = ['https://upload.wikimedia.org/wikipedia/commons/b/b4/Logan_Rock_Treen_closeup.jpg', 'https://specials-images.forbesimg.com/imageserve/dv424076/960x0.jpg?fit=scale', 'https://texasgardenmaterials.com/wp-content/uploads/2018/08/bull-rock-landscaping-rocks-gravel-houston-tx-77099.jpeg', 'https://kubrick.htvapps.com/htv-prod-media.s3.amazonaws.com/images/plymouth-rock-vandalism-01-1581953489.jpg', 'https://images.homedepot-static.com/productImages/94af8836-0338-4802-914e-04cc71e562ad/svn/backyard-x-scapes-fake-rocks-hdd-rof-rocsb-64_1000.jpg', 'https://cdn.britannica.com/11/150911-050-E7CEBE50/Rocks-size-rock-Some-sand-grains-Others.jpg', 'https://cdn.psychologytoday.com/sites/default/files/field_blog_entry_images/2019-11/gray_rock-arulonline-_pixabay.jpg', 'https://upload.wikimedia.org/wikipedia/commons/f/f6/Rock_balancing_20190227_2.jpg', 'https://res.cloudinary.com/dk-find-out/image/upload/q_80,w_1920,f_auto/Limestone-060-RD010-C-SH_by22j3.jpg', 'https://api.time.com/wp-content/uploads/2020/01/colorado-sheriff-large-small-boulder-tweet.jpg?quality=85&w=1200&h=628&crop=1', 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/e/e4/Mind_Stone_VFX.png/revision/latest?cb=20190427012504', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Stone_wall%2C_Co_Cork.jpg/1200px-Stone_wall%2C_Co_Cork.jpg', 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/0/0a/Space_Stone_VFX.png/revision/latest?cb=20190427012702', 'https://www.fieldstonecenter.com/wp-content/uploads/2019/08/creative-stone-3.jpg', 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/f/f0/Time_Stone_VFX.png/revision/latest?cb=20190427012724', 'https://cdn.shopify.com/s/files/1/1167/8568/products/manten-stone-11979710398545.jpg?v=1602846008', 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/d/d7/Power_Stone_VFX.png/revision/latest/top-crop/width/360/height/450?cb=20190427012543', 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Cloughmore_Stone.jpg', 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/0/0a/Space_Stone_VFX.png/revision/latest/top-crop/width/360/height/450?cb=20190427012702', 'https://post.healthline.com/wp-content/uploads/2020/06/Blue_Stone_1200x628-facebook-1200x628.jpg', 'https://images.theconversation.com/files/223163/original/file-20180614-32334-1el058q.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=1200.0&fit=crop', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Ash_Tree_-_geograph.org.uk_-_590710.jpg/220px-Ash_Tree_-_geograph.org.uk_-_590710.jpg', 'https://www.gardeningknowhow.com/wp-content/uploads/2013/07/sycamore.jpg', 'https://ichef.bbci.co.uk/images/ic/960x960/p08634k6.jpg', 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Ash_Tree_-_geograph.org.uk_-_590710.jpg', 'https://c.files.bbci.co.uk/8A0B/production/_109893353_gettyimages-1172556174.jpg', 'https://www.gardeningknowhow.com/wp-content/uploads/2020/11/ginkgo-biloba-tree.jpg', 'https://arbordayblog.org/wp-content/uploads/2018/06/oak-tree-sunset-iStock-477164218.jpg', 'https://extension.unh.edu/sites/default/files/styles/2x_blog_main/public/field/image/maple-tree-in-park-110661300191011Zru.jpg?itok=Ma4-jMXY&timestamp=1567092160', 'https://www.telegraph.co.uk/content/dam/news/2016/09/08/107667228_beech-tree-NEWS_trans_NvBQzQNjv4BqplGOf-dgG3z4gg9owgQTXEmhb5tXCQRHAvHRWfzHzHk.jpg', 'http://www.portertreeservicesllc.com/wp-content/uploads/2016/03/tree-bark.jpg', 'https://i.pinimg.com/originals/26/16/84/26168455691666b9183e8901d8125f75.jpg', 'https://images.pexels.com/photos/3578592/pexels-photo-3578592.jpeg?cs=srgb&dl=pexels-tim-mossholder-3578592.jpg&fm=jpg', 'https://media.tegna-media.com/assets/WQAD/images/de7e5028-c8a3-463c-ac7f-64422e713bb1/de7e5028-c8a3-463c-ac7f-64422e713bb1_1920x1080.jpeg', 'https://www.gardeningknowhow.com/wp-content/uploads/2008/04/tree-bark.jpg', 'https://www.treehugger.com/thmb/dHCP77HmRucTFz08FeYWnW4EPzM=/4001x2668/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__mnn__images__2019__06__oak_trunk_ridges-59b5b9c5c8e145a0ae07dbe5c48a7854.jpg', 'https://www.friendlyshade.com/wp-content/uploads/2017/11/pine-tree-bark-03.jpg', 'https://cdna.artstation.com/p/assets/images/images/012/018/886/large/olivier-lau-treebark-6-render2-web.jpg?1532595132', 'https://www.gardeningknowhow.com/wp-content/uploads/2020/11/maple-tree-bark-with-moss.jpg', 'https://natlands.org/wp-content/uploads/2020/01/TREE-BARK-012020-9-rotated-e1579537280348.jpg', 'https://static.wikia.nocookie.net/onepiece/images/e/e7/Brook_Anime_Pre_Timeskip_Infobox.png/revision/latest?cb=20131130081430', 'https://img.apmcdn.org/daa3090cbbbaaba0e62c94d0089ab79ce30b7d82/widescreen/a5e817-20200424-bubbling-brook.jpg', 'https://static.wikia.nocookie.net/onepiece/images/4/41/Brook_Anime_Post_Timeskip_Infobox.png/revision/latest?cb=20161016160925', 'https://upload.wikimedia.org/wikipedia/commons/3/3f/Town_Brook_Plymouth_MA.jpg', 'https://pinstripes.com/oak-brook/wp-content/uploads/sites/26/2020/02/oak-brook-hero-scaled.jpg', 'https://www.georgesriver.org/wp-content/uploads/2012/02/IMG_0127-1024x768.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Town_Brook_Plymouth_MA.jpg/1200px-Town_Brook_Plymouth_MA.jpg', 'https://www.massaudubon.org/var/ezdemo_site/storage/images/site_ma/get-outdoors/wildlife-sanctuaries/richardson-brook/219851-20-eng-US/richardson-brook-wildlife-sanctuary.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Kelly_Brook_at_2015_TCA_%28cropped%29.jpg/1200px-Kelly_Brook_at_2015_TCA_%28cropped%29.jpg', 'https://i.pinimg.com/originals/25/dd/5b/25dd5bbc2853fd8e8fa7488783670b55.jpg', 'https://www.thespruce.com/thmb/uHBDfnbPlje3n5I90H1EYU193d8=/5400x3037/smart/filters:no_upscale()/person-holding-handfull-of-soil-129288276-5c4018b546e0fb0001ac25a3.jpg', 'https://s3-eu-west-1.amazonaws.com/onlineturfuploads/online-soil/main-page-images/_1200x630_crop_center-center_82_none/what-is-topsoil.jpg?mtime=1507888651', 'https://www.gardeningknowhow.com/wp-content/uploads/2011/10/soil-testing.jpg', 'https://images.theconversation.com/files/275002/original/file-20190516-69195-1yg53ff.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=1200.0&fit=crop', 'https://www.gardeningknowhow.com/wp-content/uploads/2020/11/sandy-soil.jpg', 'https://www.nrcs.usda.gov/Internet/FSE_MEDIA/nrcseprd1474614.jpg', 'https://www.thespruce.com/thmb/LQxKbXKb2Z-uPAccSZDEqvQpFS0=/3865x2174/smart/filters:no_upscale()/hands-holding-soil-502864861-588125563df78c2ccd163cd0.jpg', 'https://scx2.b-cdn.net/gfx/news/hires/2018/soilprobioti.jpg', 'https://www.thespruce.com/thmb/1hk-NUSaA9-WG9OZBEWL4rVoEUw=/5400x3613/filters:fill(auto,1)/person-holding-handfull-of-soil-129288276-5c4018b546e0fb0001ac25a3.jpg', 'https://leafly-cms-production.imgix.net/wp-content/uploads/2017/06/19151830/organic-soil-for-growing-cannabis.jpg']

download_urls(urls)