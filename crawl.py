import requests
from bs4 import BeautifulSoup
import time
import socket
from urllib.parse import urlparse

# utility functions

def get_location(ip_address):
    """Uses ipapi to extract geolocation from ip address.
        Parameters
        ----------
        ip_address : str
            IP address to translate.
            
        Returns
        -------
        str: 
            Return city name
    """
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    # return location_data
    return response.get("city")
# e.g. 
# ip_address = socket.gethostbyname('nus.edu.sg')
# print(get_location(ip_address))

def get_data(url):
    """Scrapes webpage at url given.
        Parameters
        ----------
        url : str
            URL of page to scrape.

        Returns
        -------
        list: [str, float]
            Returns content of webpage and time taken to scrape page.
    """
    try:
        url = url.strip()
        startTime = time.time()
        response = requests.get(url)
        endTime = time.time()
        print(response.status_code)
    except requests.exceptions.MissingSchema:
        print('skip: ', url)
        return ['',0]
    except requests.exceptions.ContentDecodingError:
       print('ContentDecodingError',url)
       return ['',0]
    return [response.content, endTime-startTime]


def remove_tags(html):
    """Given html page content as string, removes all html tags.
        Parameters
        ----------
        html : str
            HTML page content.

        Returns
        -------
        list: str
            Text content within html page.
    """
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def get_links(html):
    """Given html page content as string, returns a list of all hyperlinks in the page.
        Parameters
        ----------
        html : str
            HTML page content.

        Returns
        -------
        list: str
            All hyperlinks within html page.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a") # Find all elements with the tag <a>
    return links

def extract_hostname(url):
    print(url)
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract the hostname (netloc)
    hostname = parsed_url.netloc
    return hostname

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False


# read seed file
seed_file = open("seed.txt", "r")
url = seed_file.readline()
found = open("found.csv", "a")
visited_file = open("visited.csv","a")

# get data
hostname = extract_hostname(url)
ip = socket.gethostbyname(hostname)
data, responseTime = get_data(url)
text_data = remove_tags(data)
hyperlinks = get_links(data)

# TODO: filter out duplicate URLs, irrelevant URLs
# TODO: keep separate file of visited URLs, so that do not need to get data before exploring
for link in hyperlinks:
  # Write link generated to found file
  link = link.get("href")
  visited_file.write(link+"\n")
  is_valid_url = is_url(link)
  if not(is_valid_url):
    print('invalid url ' + link)
    continue
  print("Link:",link)
  name = extract_hostname(link)
  ip_address = socket.gethostbyname(name)
  data, responseTime = get_data(link) #TODO: where to store data? what to do with it?
  data = remove_tags(data)
  geolocation = get_location(ip_address)
  record = name + "," + str(ip_address) + ","+ str(ip)+","+geolocation+","+str(responseTime)+",'"+data+"'\n"
  found.write(record)
  # spawn new threads that will explore this link
  
found.close()
seed_file.close()
visited_file.close()
 

# Perform data analytics


# Generate report

