import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url_base = "https://www.futbin.com/20/pgp?page=1&sort=games&order=desc"
url_version = "&version="
url_position = "&position="

version_list = ["all_ifs"]
position_list = ["GK", "RB,RWB", "LB,LWB", "CB", "CDM,CM,CAM", "RM,RW,RF", "LM,LW,LF", "CF,ST"]

for position in position_list:
	for version in version_list:
		print("%s %s" % (position, version))
		url = "%s%s%s%s%s" % (url_base, url_version, version, url_position, position)

		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		table = soup.find("table",{"class":"table table-bordered table-hover"})

		keys = [th.get_text(strip=True)for th in table.find_all('th')]
		l = []
		for tr in table.find_all('tr'):
		    values = [td.get_text(strip=True) for td in tr.find_all('td')]
		    d = dict(zip(keys, values))
		    l.append(d)

		json_string = json.dumps(l, ensure_ascii=False).encode('utf8')
		now = datetime.now()
		dt_string = now.strftime("%Y%m%d%H")
		filename = "../scraped_data/%s_%s_%s.json" % (dt_string, position, version)
		with open(filename, 'x', encoding='utf8') as json_file:
		    json.dump(l, json_file, indent=4, ensure_ascii=False)
input("Finished. Press ENTER to exit.")