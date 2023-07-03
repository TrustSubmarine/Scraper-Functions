# Install dependencies in project root
pip3 install --platform manylinux2014_x86_64 --target=scraping --implementation cp --python-version 3.9 --only-binary=:all: --upgrade beautifulsoup4 requests

# Zip files for deployment
zip -r files