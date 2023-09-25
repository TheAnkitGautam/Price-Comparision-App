import tokenize
from requests_html import HTMLSession
from bs4 import BeautifulSoup#_21lJbe
# from amazonscrape import mai
import sqlite3
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "laptop.db")
print(db_path)
conn=sqlite3.connect(db_path)

c=conn.cursor()
conn.commit()
# print()
s=HTMLSession()
def get_url(search_term):
    template="https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page1=&page="
    search_term=search_term.replace(' ','+')
    url=template.format(search_term)
    # print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    n = soup.find("div", {"class": "_2MImiq"})
    n=n.find("span").text
    j=n.find("of")
    n=n[j+2:len(n)]
    n=int(n)
    return url,n
def extract_info(result):
    try:
        price=result.find("div",{"class":"_30jeq3 _1_WHN1"}).text
        price=price[1:len(price)]
        price=price.replace(",","")
        price= ''.join(x for x in price if x.isdigit())
        price=int(price)
    except AttributeError:
        return
    for a in result.find_all('a', href=True):
        se=a['href']
        break

    link="https://www.flipkart.com"+se
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    r = s.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    model=soup.find("div",{"class":"_3k-BhJ"})
    if model is None:
        return
    te = model.find_all('tr')
    for t in te:
        if (t.text.find("Model Number") != -1):
            break
    t = t.find('td',{"class":"URwL2w col col-9-12"}).text
    model_n = t.strip()
    data_tuple = (model_n, price, link)
    data_t = (price, link, model_n)
    # c.execute(query,data_tuple)
    c.execute('INSERT OR IGNORE INTO one(model_number,filpkart_price,flipkart_link) VALUES(?,?,?)', data_tuple)
    c.execute('UPDATE one SET filpkart_price = ?,flipkart_link = ? WHERE model_number=?', data_t)
    conn.commit()
    info=(price,link,model_n)
    print(info)
    return price,link
def main(search_term):
    records=[]
    url,n=get_url(search_term)
    c=0
    for i in range(1,n):
        ur=url+str(i);
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        r = s.get(ur, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.title)
        results =soup.find_all("div",{"class":"_2kHMtA"})
        for item in results:
            record = extract_info(item)
            if record:
                c=c+1
                records.append(record)
    print(c)
names=["lenovo laptops"]#,"Xiaomi mobile","Samsung mobile","OnePlus mobile","realme mobile","Oppo mobile","Vivo mobile"]
for name in names:
    print(name)
    main(name)
