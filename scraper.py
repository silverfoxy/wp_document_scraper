import requests
import csv
from bs4 import BeautifulSoup

# Fetch the WP Functions documents page
function_documents_urls = []
first_page = 1
last_page=49
for i in range(first_page, last_page+1):
    print(f"[+] Getting function documents {i}/{last_page}")
    response = requests.get(f"https://developer.wordpress.org/reference/functions/page/{i}/")
    soup = BeautifulSoup(response.text, 'html.parser')
    function_documents_urls += [a['href'] for a in soup.find_all('a') if 'functions' in a['href'] and '#' not in a['href']]
    # print(function_documents_urls)

functions_with_callback = []
for function_url in function_documents_urls:
    print(f"[+] Checking if {function_url} accepts callable")
    response = requests.get(function_url)
    # Foreach span with class="arg-type", if text == callable, then save it
    soup = BeautifulSoup(response.text, 'html.parser')
    spans = soup.find_all('span', attrs={'class': 'arg-type'})
    for span in spans:
        if span.text == 'callable':
            functions_with_callback.append(function_url)

print('---Functions with callable parameters---')
print(functions_with_callback)

with open('callable_functions.csv', 'wb') as output_file:
    wr = csv.writer(output_file, quoting=csv.QUOTE_ALL)
    wr.writerow(functions_with_callback)
print('[+] Results written to "callable_functions.csv"')