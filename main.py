import requests
import re
from xml.dom import minidom

url = input('Playlist Link: ')
save_file = input('File Name: ')
save_file = save_file + '.xspf'
response = requests.get(url)
webContent = response.text.encode('utf-8')
#f = open('webpage.html', 'wb')
#f.write(webContent)

results = re.findall(r'"url":"(.*?)",', str(webContent))
#print(results)
#f = open('print.txt', 'w')
links = []
count = 0
# Get list of links
for x in results:
    if '/watch?' and 'index' in x and 'QAFIAQ%3D%3D' not in x and 'playlist?' not in x:
        links.append(count)
        links[count] = 'https://youtube.com' + x
        count = count + 1
links = list(dict.fromkeys(links))
#for x in links:
#    f.write(x + '\n')
    
# Create XML file for VLC
root = minidom.Document()
playlist = root.createElement('playlist')
playlist.setAttribute('xmlns', 'http://xspf.org/ns/0/')
playlist.setAttribute('xmlns:vlc', 'http://www.videolan.org/vlc/playlist/ns/0/') 
playlist.setAttribute('version', '1')
root.appendChild(playlist)

title = root.createElement('title')
titleText = root.createTextNode('YoutubePlaylist')

trackList = root.createElement('trackList')

title.appendChild(titleText)
playlist.appendChild(title)
playlist.appendChild(trackList)

track = []
location = []
locationText = []
count = 0
for link in links:
    track.append(count)
    location.append(count)
    locationText.append(count)
    
    track[count] = root.createElement('track')
    trackList.appendChild(track[count])
    location[count] = root.createElement('location')
    locationText[count] = root.createTextNode(link)
    location[count].appendChild(locationText[count])
    track[count].appendChild(location[count])

xml_str = root.toprettyxml(encoding = "utf-8", indent ="\t") 

with open(save_file, "wb") as f:
    f.write(xml_str)
