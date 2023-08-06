# Python-Legacy-Automation-Framework

## Description

Python library that is built for legacy automation framework use

## Setting Up Virtual Mainframe (for testing purposes)

<a href="https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6?activetab=pivot:overviewtab">Using Ubuntu</a>
Set up virtual mainframe with docker

```docker run -dit --name tk4- -p 3270:3270 -p 8038:8038 -p 21:21 rattydave/docker-ubuntu-hercules-mvs:latest```

Verify Docker instance is started:

<img src="https://github.cms.gov/MPSMMIT/python-legacy-automation-framework/blob/master/images/docker-container.png"
  alt="Docker Test Container">

Check that WSL is enables in container

<img src="https://github.cms.gov/MPSMMIT/python-legacy-automation-framework/blob/master/images/wsl-integration.png"
  alt="WSL Enabled">
  
### Configure the container

Connect to container:

```docker exec -it tk4- /bin/bash```

Install Hercules:

```apt-get update -y```

```apt-get install -y hercules```

install x3720:

```apt-get install -y x3270```

## Installation
On your machince, install wc3270:

<a href=https://x3270.miraheze.org/wiki/Downloads>wc3270 Download<a>

Bring library to your environment: 

```pip install Automation3270```

Initilize the Automation class. Example file to start with:

```python
import Automation3270

# Initialize automation (Username, Password, Host Name:Port Number, Visible = True, Delay Time = 0)
automate = Automation3270.Automation(userName='HERC01', password='CUL8TR', hostNamePort='172.31.96.1:3270', visible=True, delayTime=2)

# Before task
automate.login()

# Tasks to complete

# After task
automate.logout()
```

## Automations availble

Logs in to the terminal with the supplied credentials

```python
login()
```

Logs out of the terminal

```python
logout()
```

Traverses through the terminal to set the Data-set list for HERC01

```python
view_dataset_list()
```