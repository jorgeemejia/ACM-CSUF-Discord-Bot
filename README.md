![](imgs/ACMDevLogo.png)
# ACM-CSUF-Discord-Bot

#Welcome!
This is the GitHub for ACM-CSUF's Discord Bot. (Mission Statement Here)

# Features
## There are 2 main features we would like for this bot to have.

## 1
* On-Boarding Feature
  * Restricts new members to view only certain channels (#announcements, #get-roles, #rules, #help, #server-wiki)  until they choose a role, once they choose a role, they’ll be able to view all of the channels that pertain to their chosen role + #General

## 2

# More Info About The Features

## On-Boarding Feature

This functionality will consist of Two Events:

i.On_Member_Join:

* Get the role id of the “New_Members” role
  * (Users in the New_Members Role will only be able to see (#announcements, #get-roles, #rules, #help, #server-wiki)
* Assign the member who just joined to “New_Members”



ii.On_Raw_Reaction_Add:

* Get the message-id of “Role Message”
  * (Role Message will be the only message found in Get-Roles, Role Message will be the message new members will react to in order to get a role)
* If the message-id of “Role Message” is the same as the message-id of the payload, 
   * store the value of the member of the payload 
   * store the guild of that member^
* Get the id of the emoji the member used to react
* If the id of the emoji matches the id of the Dev emoji, assign the user to the Dev role 
* If the id of the emoji matches the id of the Create emoji, assign the user to the Create role
* If the id of the emoji matches the id of the Algo emoji, assign the user to the Algo role 
* If the id of the emoji doesn’t match with any of the Path emojis (Dev, Create, Algo), ignore the reaction add



# Installation

## Pre-Req's:

* Have Python3 installed
(since we will be using Discord.py, you will need the latest version of Python aka Python3)
* An IDE of your choice
(e.g. Atom, Visual Studio, Visual Studio Code)
* A Github Account

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
