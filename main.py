import os
import requests
import boto3
from bs4 import BeautifulSoup
import subprocess

def scrape_images(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print("Scraping images from:", url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        domain = os.path.basename(url)
        images_dir = os.path.join("Featured Suppliers", domain)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        img_tags = soup.find_all("img", src=True)
        for i, img_tag in enumerate(img_tags):
            img_url = img_tag["src"]
            img_name = f"image_{i + 1}.jpg"
            img_path = os.path.join(images_dir, img_name)
            try:
                img_response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                if img_response.status_code == 200:
                    with open(img_path, "wb") as f:
                        f.write(img_response.content)
                    print("Image saved:", img_path)
                else:
                    print("Failed to download image:", img_url)
            except Exception as e:
                print("Error downloading image:", e)


def scrape_text(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print("Scraping text from:", url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        div_tag = soup.find("div", class_="col-lg-12 contentside")
        if div_tag:
            text_content = div_tag.get_text()
            with open("assessment.txt", "w", encoding="utf-8") as file:
                file.write(text_content.strip())
            print("Text content saved to assessment.txt")
        else:
            print("Couldn't find the div tag with class 'col-lg-12 contentside'")

def scrape_images_franchise(url, target_div_class):
    page_number = 1
    while True:
        page_url = f"{url}/page/{page_number}/"
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            div_tag = soup.find("div", class_=target_div_class)
            if div_tag:
                domain = os.path.basename(url)
                page_images_dir = os.path.join("Franchise Suppliers", domain, f"Page_{page_number}")
                if not os.path.exists(page_images_dir):
                    os.makedirs(page_images_dir)
                img_tags = div_tag.find_all("img", src=True)
                if not img_tags:  
                    break
                
                for i, img_tag in enumerate(img_tags):
                    img_url = img_tag["src"]
                    img_name = f"image_{i + 1}.jpg"
                    img_path = os.path.join(page_images_dir, img_name)
                    try:
                        img_response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                        if img_response.status_code == 200:
                            with open(img_path, "wb") as f:
                                f.write(img_response.content)
                            print("Image saved:", img_path)
                        else:
                            print("Failed to download image:", img_url)
                    except Exception as e:
                        print("Error downloading image:", e)
                page_number += 1
            else:
                print("Couldn't find the target div:", target_div_class)
                break
        else:
            print("Failed to access page:", page_url)
            break

def scrape_text_resources():
    all_hrefs = []
    page_number = 1
    while page_number <= 15:  
        page_url = f"https://franchisesuppliernetwork.com/resources/page/{page_number}/"
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            link_tags = soup.select("div.news-container.blogpage a[href]")
            if link_tags:
                for link_tag in link_tags:
                    href = link_tag.get("href")
                    all_hrefs.append(href)
                page_number += 1
            else:
                print("No more pages found.")
                break
        else:
            print("Failed to access page:", page_url)
            break

    if not os.path.exists("Resource"):
        os.makedirs("Resource")
    for idx, href in enumerate(all_hrefs, start=1):
        response = requests.get(href, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            text_content = None

            div_tag = soup.find("div", class_="news-container blogpage")
            if div_tag:
                text_div = div_tag.find("div", class_="col-sm-12")
                if text_div:
                    text_content = text_div.get_text().strip()

            if text_content is None:
                text_content = soup.get_text().strip()

            # Save text content to file for each page
            if text_content:
                with open(os.path.join("Resource", f"Resource_page_{idx}.txt"), "w", encoding="utf-8") as file:
                    file.write(text_content)
                print(f"Text content saved to Resource_page_{idx}.txt")
            else:
                print("Couldn't find the text content on page:", href)
        else:
            print("Failed to access page:", href)

def scrape_about_franchise(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print("Scraping About page:", url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the div containing the About page text
        about_div = soup.find("section", class_="inner-content")
        if about_div:
            # Extract text content
            text_content = about_div.get_text(separator="\n").strip()
            # Save text content to file
            with open("franchise_about.txt", "w", encoding="utf-8") as file:
                file.write(text_content)
            print("About page text saved to franchise_about.txt")

            # Find all image URLs within the About page
            img_tags = about_div.find_all("img", src=True)
            # Create a directory to store images
            images_dir = os.path.join("Franchise Suppliers", "franchise_about")
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            # Download and save images
            for i, img_tag in enumerate(img_tags):
                img_url = img_tag["src"]
                img_name = f"image_{i + 1}.jpg"
                img_path = os.path.join(images_dir, img_name)
                try:
                    img_response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    if img_response.status_code == 200:
                        with open(img_path, "wb") as f:
                            f.write(img_response.content)
                        print("Image saved:", img_path)
                    else:
                        print("Failed to download image:", img_url)
                except Exception as e:
                    print("Error downloading image:", e)
        else:
            print("About page div not found.")

def upload_image_to_s3(img_path, s3_folder):
    s3_client = boto3.client('s3')
    s3_key = os.path.join("Sithihalitha_S", s3_folder, os.path.basename(img_path))
    try:
        s3_client.upload_file(img_path, "proco-take-home-assignment", s3_key)
        print(f"Uploaded {img_path} to S3 as {s3_key}")
    except Exception as e:
        print(f"Failed to upload {img_path} to S3:", e)

def upload_to_s3():
    
    subprocess.run(["aws", "s3", "cp", "assessment.txt", "s3://proco-take-home-assignment/Sithihalitha_S/assessment.txt", "--no-sign-request"])
    
    subprocess.run(["aws", "s3", "sync", "Featured Suppliers", "s3://proco-take-home-assignment/Sithihalitha_S/Featured Suppliers", "--no-sign-request"])

    subprocess.run(["aws", "s3", "sync", "Franchise Suppliers", "s3://proco-take-home-assignment/Sithihalitha_S/Franchise Suppliers", "--no-sign-request"])

    subprocess.run(["aws", "s3", "sync", "Resource", "s3://proco-take-home-assignment/Sithihalitha_S/Resource", "--no-sign-request"])

    subprocess.run(["aws", "s3", "cp", "franchise_about.txt", "s3://proco-take-home-assignment/Sithihalitha_S/franchise_about.txt", "--no-sign-request"])


def main():
    base_url = "https://franchisesuppliernetwork.com"
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    print("Response status code:", response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        ul_tag = soup.find("ul", id="primary-menu")
        if ul_tag:
            alist = []
            for a_tag in ul_tag.find_all("a", href=True):
                href = a_tag["href"]
                print(href)
                alist.append(href)
            if alist:
                scrape_images(alist[0])
            if len(alist) > 1:
                scrape_text(alist[1])
            if len(alist) > 2:
                scrape_images_franchise(alist[2], "fs-container page-fs")
            if len(alist) > 3:
                scrape_text_resources()  
            if len(alist) > 11:
                scrape_about_franchise(alist[11])

    # Upload scraped data to S3 bucket
    upload_to_s3()

if __name__ == "__main__":
    main()
