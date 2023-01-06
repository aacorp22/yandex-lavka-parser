import re
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup

url = "https://lavka.yandex.ru/213/category/energy_beer"

res = requests.get(url)
content = res.text
soup=BeautifulSoup(content, "html.parser")
all_goods = [] # list[dict]

def get_html_text(string: str) -> str:
    """Gets text from html, removes unicode special characters"""
    return string.get_text().strip().replace("\xad", "").replace("\xa0", " ")


for good in soup.find_all('div', class_="p10zc8qs"):
    # extracting goods classes and their names
    good_name_raw = good.find('h3', class_="tvt9inf t18stym3 bw441np r88klks r1dbrdpx n10d4det l14lhr1r c10zw1sq")
    # get text and remove soft-hyphens
    good_name = get_html_text(good_name_raw)
    
    # extracting goods prices
    actual_price_html = good.find('span', class_="tmwo625") # gives "66\xa0₽89\xa0₽" 
    actual_price_raw = get_html_text(actual_price_html) # 66₽89₽
    prices = re.findall(r"(\d+)", actual_price_raw) # ["66", "89"]
    actual_price = int(prices[0])
    regular_price = int(prices[1])
    
    # getiing goods description
    comment_text = good.find_all("span", class_ = "a1dq5c6d")[0]
    comment = get_html_text(comment_text)

    # getting goods weight
    weight_text = good.find("span", class_ = "iks4ndv")
    weight = get_html_text(weight_text)

    # getting discount percentage
    discount_html = good.find("li", class_ = "s17si6sz")
    discount_text = get_html_text(discount_html)
    discount = re.sub(r"[^0-9%]+", "", discount_text)

    # getting goods image
    img_html = good.find('img', class_="i1s3mcod i1shnzmq")
    image = img_html.attrs["src"].replace("-pixelize", "")

    all_goods.append({
        "Наименование": good_name,
        "Актуальная цена, ₽": actual_price,
        "Фактическая цена, ₽": regular_price,
        "Вес товара": weight,
        "Скидка": discount,
        "Комментарий": comment,
        "Картинка": image
        }
    )

df = DataFrame(all_goods)
df.to_excel('energetics.xlsx', index=False)

with open("all_energetics.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())
