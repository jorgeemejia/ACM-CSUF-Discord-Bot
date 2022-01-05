![](imgs/ACMDevLogo.png)
# ACM-CSUF-Discord-Bot

THIS WAS ALL MADE BY ME 

# Welcome!
This is the GitHub for ACM-CSUF's Discord Bot. 

# Features
## There are 2 main features we would like for this bot to have.

i. On-Boarding Feature
  * Restricts new members to view only certain channels (#announcements, #get-roles, #rules, #help, #server-wiki)  until they choose a role, once they choose a role, they’ll be able to view all of the channels that pertain to their chosen role + #General

ii. Scheduling Feature : Matching of Classes
  * A pinned message with a link to a Google Form asking students to fill out their schedules in the "Scheduling" text channel.
  * This Google Form will gather the class sections they are taking. Links to a backend Database.
  * Add members to text channels based on their classes (pulled from this database). It is like adding a role to them, and classes they are not in will not be visible to avoid visual clog of the server. 
  * Computer Science Classes: Each class inclusive of all sections will be their own text channel. ("CS 120" has 120-1,-2,-3,-4..., "CS 121" has 121-1,-2,-3,-4...,...)
  * Select Math Classes: Math 125, 150A, 150B, 250A, 270A, 270B, 338 will have their own text channels inclusive of all sections. 
  * Non CS Dept Classes: Each department inclusive of all classes will be their own text channel. ("GEOL" has all sections of 101, 201, ...)
  * Members can do a command within these channels that shows who in the text channel has the same section number as them. 
iii. Scheduling Feature : Data Metrics
  * Coming from the same Backend Database, the data of class times will be what is analyzed.
  * Analysis of when members are in classes, output of times when most students (50%+) are out of class to help us schedule club events
  * Can be filtered to output based on paths (Algo, Create, Dev)

# More Info About The Features

## On-Boarding Feature

This functionality will consist of Two Events:

i. On_Member_Join:

* Get the role id of the “New_Members” role
  * (Users in the New_Members Role will only be able to see (#announcements, #get-roles, #rules, #help, #server-wiki)
* Assign the member who just joined to “New_Members”

ii. On_Raw_Reaction_Add:

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
git clone https://github.com/jorgeemejia/acmCSUF-DiscordBot.git
```

## Step 3:

Move into repository, 

```
cd acmCSUF-DiscordBot
```

## Step 4:

```
python -m pip install -r ./requirements.txt
```
If this isn't working, try:

```
python3 -m pip install -r ./requirements.txt
```

## Step 5:

To run the bot, 

```
python main.py
```
