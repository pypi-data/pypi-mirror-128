#!/usr/bin/python3.6
from setuptools import setup

setup(
    name="scienceBot",
    version="0.1.1.1",
    description="Bot for sci-com and policy-com ",
    url="https://github.com/fanasal/science_bot",
    license="GNU Affero General Public License v3.0",
    packages=["scibot"],
    keywords=[
        "psychedelics",
        "fact-checking",
        "sci-com",
        "drug policy",
        "research",
        "science",
    ],
    entry_points={
        "console_scripts": [
            "scibot=scibot.what_a_c:main",
        ]
    },
    install_requires=[
        "beautifulsoup4==4.9.3",
        "feedparser==6.0.2",
        "oauthlib==3.1.1",
        "python-dotenv==0.15.0",
        "requests==2.26",
        "requests-oauthlib==1.3.0",
        "schedule==0.6.0",
        "telebot==0.0.4",
        "Telethon==1.18.2",
        "tweepy==4.4.0",
        "urllib3==1.26.7",
    ],
    zip_safe=False,
)
