from bs4 import BeautifulSoup
import urllib.request
import click

@click.command()
@click.option('--arguments', '-a', 'arguments')

def search(arguments):

    words = arguments.split(' ')

    if len(words) >1:
        final = '+'.join(words)
    else:
        final = ''.join(words)

    try:
        url = 'https://www.google.com/search?q=<%s>' % final

        # now, with the below headers, we defined ourselves as a simpleton who is
        # still using internet explorer.
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()

        soup = BeautifulSoup(str(respData), 'html.parser')

        headings = [i.get_text() for i in  soup.find_all('h3', class_='LC20lb')]
        links = [i.get_text() for i in  soup.find_all('cite', class_='iUh30')]
        desc = [i.get_text() for i in  soup.find_all('span', class_='st')]

        for i in range(len(headings)):
        	print('')
        	print('%s. %s' % (i+1, headings[i]))
        	print(links[i])
        	print(desc[i])
        	print('')


        # print()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    search()