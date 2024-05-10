import urllib.parse
import sys

URL: str = urllib.parse.quote_plus(sys.argv[1])
print(URL)
