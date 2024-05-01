# EzeeAssist_scraping


Web Scraping and Data Upload to AWS S3:
      1. This Python script scrapes data(both text and images) from a website and uploads it to an AWS S3 bucket.
      2. It's designed to scrape various types of content from a franchise supplier network website, including images and text, and then uploads them to AWS S3.

Prerequisites:
    Before running the script, make sure you have the following installed:
        * Python 3.x
        * Required Python packages (requests, boto3, beautifulsoup4)
You'll also need:
        * An AWS account with S3 access

Usage
      1. Clone the repository: https://github.com/sithihalitha/EzeeAssist_scraping.git
      2. Install the required Python packages:  pip install requests boto3 beautifulsoup4
      3. Run the script:   Python main.py

The script will scrape data from the franchise supplier network website and upload it to AWS S3.


Configuration
    1. AWS Credentials: Make sure your AWS credentials are correctly set up on your machine. This can be done via AWS CLI or environment variables.
    2. Target Website: The script is currently set to scrape data from the franchise supplier network website. You can change this by modifying the base_url variable in the script.
    3. S3 Bucket: The script is configured to upload data to an S3 bucket named proco-take-home-assignment. Modify this to match your S3 bucket name.

Files Generated
The script generates the following files:
            assessment.txt: Contains scraped text content.
            Feature Suppiers/: Directory Containing images from franchise feature Suppliers(Home Page)
            Franchise Suppliers/: Directory containing images from franchise suppliers.
            Resource/: Directory containing text files scraped from resource pages.
            franchise_about.txt: Contains text content from the About page of franchise suppliers.
            README.md: This README file.


License
This project is licensed under the MIT License - see the LICENSE file for details.


