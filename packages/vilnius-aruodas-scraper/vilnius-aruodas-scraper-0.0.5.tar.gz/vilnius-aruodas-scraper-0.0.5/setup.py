import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vilnius-aruodas-scraper",
    version="0.0.5",
    author="Blessing E-Philips",
    author_email="blessingphilips@ymail.com",
    description="Aruodas.lt website scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/u-aaa/Vilnius-Apartment-Predictions",
    project_urls={
        "Bug Tracker": "https://github.com/u-aaa/Vilnius-Apartment-Predictions/issues",
    },
    install_requires=['requests_html', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["aruodas_scraper"],
    package_dir={"": "scraper"},
    packages=setuptools.find_packages(where="scraper"),
    python_requires=">=3.7"
)
