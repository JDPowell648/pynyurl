import urllib.parse
import sys

# python3 urlencode.py "https://www.youtube.com/watch?v=qNdjZOgCU1I"
URL: str = urllib.parse.quote_plus(sys.argv[1])
print(URL)
