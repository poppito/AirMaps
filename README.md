# AirMaps
Airmaps is a django-based concoction that uses Google Maps' JavaScript API (https://developers.google.com/maps/documentation/javascript/) and the T-Dev WIFI API (https://dev.telstra.com/) to give users locations of Telstra's AIR wifi hotspots. I've removed all API keys and username/password references (obviously).

To run:

git clone https://github.com/poppito/AirMaps.git

a) You'll need to create your own settings.py under AirMaps/AirMaps
b) You'll need to create your own API keys for Google Maps (developers.google.com) - this is contingent on creating a google account of course. Place your API key in AirMaps/Airmap/API_KEY
c) You'll need to create an account on T-dev (dev.telstra.com) - place your username in AirMaps/Airmap/username and password in AirMaps/Airmap/password
d) There is no pre-requisite for models.py under Airmap (unless you want to do something smart with this, like tracking users and running analytics etc).
e) I'm running wsgi (wsgi.py has been included) with Apache2 (httpd.conf is not included).

Disclaimer: All references to Google and Telstra are purely for instructional purposes. 
