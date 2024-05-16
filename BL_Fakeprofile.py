import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import io
import sys

def detect_fake_profile(profile_url):
    # Download the profile page
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for profile picture
    profile_pic = soup.find('img', {'class': 'profile_picture'})
    if not profile_pic or 'src' not in profile_pic.attrs:
        print('No profile picture or a generic image')

    # Check for complete profile information
    complete_info = True
    for field in ['name', 'location', 'website', 'bio']:
        field_value = soup.find('span', {'class': f'_50f0'})
        if not field_value or field not in field_value.text.lower():
            complete_info = False
            break
    if not complete_info:
        print('Incomplete profile information')

    # Check for friends and followers
    friends = soup.find('span', {'class': 'fsl'})
    followers = soup.find('span', {'class': 'fsl fwb'})
    if not friends or not followers:
        print('Lack of friends or followers')

    # Check for high volume of activity
    activity = soup.find_all('span', {'class': 'fwb'})
    if len(activity) > 10:
        print('High volume of activity')

    # Check for unsolicited friend requests or messages
    friend_requests = soup.find_all('span', {'class': 'dui'})
    messages = soup.find_all('span', {'class': 'pam'})
    if friend_requests or messages:
        print('Unsolicited friend requests or messages')

    # Check for grainy or low-quality profile picture
    image_url = profile_pic['src'] if profile_pic else ''
    if image_url:
        image_response = requests.get(image_url)
        image_file = io.BytesIO(image_response.content)
        image = Image.open(image_file)
        if image.width < 100 or image.height < 100:
            print('Grainy or low-quality profile picture')

    # Check for inconsistent details
    name = soup.find('span', {'class': 'fwb'})
    location = soup.find('span', {'class': 'fcg'})
    website = soup.find('a', {'class': 'bxw'})
    bio = soup.find('span', {'class': 'fwb'})
    if name and 'name' not in name.text.lower():
        print('Inconsistent name')
    if location and 'location' not in location.text.lower():
        print('Inconsistent location')
    if website and 'website' not in website.text.lower():
        print('Inconsistent website')
    if bio and 'bio' not in bio.text.lower():
        print('Inconsistent bio')

    # Check for geographic inconsistencies
    if soup.find('span', {'class': 'fcg'}) and 'geographic inconsistencies' in soup.find('span', {'class': 'fcg'}).text.lower():
        print('Geographic inconsistencies')

# Example usage
detect_fake_profile('https://www.facebook.com/fakeprofile')