from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sqlite3
conn=sqlite3.connect('laptop.db')
c=conn.cursor()
s=HTMLSession()
def get_url(search_term):
    template="https://www.amazon.in/s?k={}&page="
    search_term=search_term.replace(' ','+')
    search_term=search_term.replace('(','+')
    search_term=search_term.replace(')','+')
    url=template.format(search_term)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    n=soup.find("span",{"class":"s-pagination-item s-pagination-disabled"}).text
    print(int(n))
    return url,int(n)
def getinfo(soup):
    soup=soup.find("div",{"class":"a-expander-content a-expander-section-content a-section-expander-inner"})
    if(soup is None):
        return
    te=soup.find_all('tr')
    ccc=0
    for t in te:
        if(t.text.find("model number")!=-1):
            ccc=1
            break
    if (ccc==0):
        return
    t=t.find('td').text
    model_number=t.strip()
    return model_number
def extract_info(result):
    soup=result.find("h2",{"class":"a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
    # name=result.find("span",{"class":"a-size-medium a-color-base a-text-normal"}).text
    try:
        price=result.find("span",{"class":"a-price-whole"}).text
        price=price.replace(",","")
        price= ''.join(x for x in price if x.isdigit())
        price=int(price)
    except AttributeError:
        return
    for a in soup.find_all('a', href=True):
        ss=a['href']
        break
    link="https://www.amazon.in"+ss
    # info=(name,colour,ram,rom,price,link)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    r = s.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    model_n=getinfo(soup)
    if model_n is None:
        print("hii")
        return
    nn = len(model_n)
    model_n = model_n[1:nn]
    # data_tuple = (model_n, price, link)
    # c.execute('INSERT OR IGNORE INTO model_number,amazon_price,amzon_linkone VALUES(?,?,?)', data_tuple)
    data_tuple = (model_n,price,link)
    data_t = (price,link,model_n)
    # c.execute(query,data_tuple)
    c.execute('INSERT OR IGNORE INTO one(model_number,amazon_price,amazon_link) VALUES(?,?,?)', data_tuple)
    c.execute('UPDATE one SET amazon_price = ?,amazon_link = ? WHERE model_number=?', data_t)
    conn.commit()
    return model_n,price,link
def mai(search_term):
    records=[]
    url,n=get_url(search_term)
    # print(url)
    dddd=0
    check=0
    for i in range(1,n):
        ur=url+str(i);
        # print(ur)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        r = s.get(ur, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup)
        results=soup.find_all("div",{"class":"s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border"})
        for item in results:
            record = extract_info(item)
            if record:
                dddd=dddd+1
                print(record)
                records.append(record)
                check=check+1;
    print(check)
    print(dddd)
names=["lenovo laptop"]
for name in names:
    print(name)
    mai(name)

