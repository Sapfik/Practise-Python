url = 'mailto:tony@alohatony.com?subject=Inquiry%20on%20366%20%20Keolu%20Dr%20from%20hicentral.com'

new_url = url.split('?')[0]
new1_url = new_url.split(':')[-1]
print(new1_url)
