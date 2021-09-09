import requests
import re
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models


BASE_URL = "https://losangeles.craigslist.org/search/?query={}"
BASE_IMAGE = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    return render(request, 'base.html')


def search(request):
    search_val = request.POST.get("search")
    models.Search.objects.create(search=search_val)
    url = BASE_URL.format(search_val)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")

    post_listing = soup.find_all("li", {"class": "result-row"})
    final_post = []
    for post in post_listing:
        post_title = post.find(class_="result-title").text
        post_url = post.find("a").get("href")
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            post_price = "N/A"
        if post.find(class_="result-image").get("data-ids"):
            image = post.find(class_="result-image").get("data-ids").split(",")[0].split(":")[1]
            post_image = BASE_IMAGE.format(image)
        else:
            post_image = "https://craigslist.org/images/peace.jpg"

        final_post.append((post_title, post_url, post_price, post_image))

        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            new_response = requests.get(post_url)
            new_data = new_response.text
            new_soup = BeautifulSoup(new_data, "html.parser")
            post_text = new_soup.find(id="postingbody").text

            r1 = re.findall(r"\$\w", post_text)
            if r1:
                post_price = r1[0]
            else:
                post_price = "N/A"

        if post.find(class_="result-image").get("data-ids"):
            post_image_id = post.find(class_="result-image").get("data-ids").split(",")[0]
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"

        final_post.append((post_title, post_url, post_price, post_image_url))
    print(final_post)

    context = {
        "search": search_val,
        "posting": final_post
    }
    return render(request, "my_app/new_search.html", context)
# Create your views here.
