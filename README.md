![](imgs/ACMDevLogo.png)
# ACM-CSUF-Discord-Bot

# Features
* On-Boarding Feature
  * Restricts new members to view only certain channels (#announcements, #get-roles, #rules, #help, #server-wiki)  until they choose a role, once they choose a role, they’ll be able to view all of the channels that pertain to their chosen role + #General


# Installation

## Pre-Req's:

* Have Python3 installed
(since we will be using Discord.py, you will need the latest version of Python aka Python3)

### Don't Have Python Installed?
Link to downloads:
https://www.python.org/downloads/

Guide to download Python3 on Windows:
https://phoenixnap.com/kb/how-to-install-python-3-windows

Guide to download Python3 on Mac
https://docs.python-guide.org/starting/install3/osx/

## Step 1:

Open your terminal

## Step 2:

Git clone

```
git clone https://github.com/wesleychoucsuf/acmCSUF-DiscordBot.git
```

## Step 3:

Move into repository, 

```
cd acmCSUF-DiscordBot
```

## Step 4:

```
python -m pip install -r .\requirements.txt
```
If this isn't working, try:

```
python3 -m pip install -r .\requirements.txt
```

## Step 5:

To run the bot, 

```
python main.py
```
