import urllib.request
import urllib.parse
import json
# import skimage.io as io

# Adding headers to hack API
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"

# URL creation
keyword = 'Дурсль'
args = {'count': 10, 'offset': 1, 'q': keyword}
args = urllib.parse.urlencode(args)
url = 'https://api.qwant.com/api/search/images?{}'.format(args)
req = urllib.request.Request(url, headers = headers)
html = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(html)

# Image manipulation
image = data['data']['result']['items'][0]['media']
filename = image.split("/")[-1]
local_filename, headers = urllib.request.urlretrieve(image, filename=filename)

# To show image uncomment this lines and do
# pip install -U scikit-image
# image = io.imread(local_filename)
# io.imshow(image)
# io.show()
