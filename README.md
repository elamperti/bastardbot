![BastardBot](https://raw.githubusercontent.com/wiki/elamperti/bastardbot/images/bastard_banner720.png)

## Welcome to the bastardbot project

This bot connects to Google Hangouts conversations using
[hangups](https://github.com/tdryer/hangups/), by Tom Dryer.
It will let you use/interact with the conversations *soon*.
We are working on it as much as we can.

For more information read [the wiki](wiki)!

### Objectives

  * **Follow an ongoing conversation**, acting upon its messages according to its *filters*.
  * **Give information** back to conversations when an *event* is triggered or by request of the users (via *slash commands* or a *web API*).
  * We would like this to eventually evolve into a **logging tool** for chats.


Installation
------------

The bot is not ready yet!

**IMPORTANT**: Python 3.3 or higher is required by hangups.
You can install `pyenv`, which will make your life *a lot* easier. 
Here's a [good tutorial about pyenv](http://davebehnke.com/python-pyenv-ubuntu.html).

---

Before starting you must get the *hangups* submodule.
```
git submodule init
git submodule update
```

Install the required packages with pip: 
`pip install -r requirements.txt`

The first time you start BastardBot, you will be prompted to log into your Google
account by the hangups library. It only sends your credentials to Google, and it 
stores session cookies locally.

Documentation, help and feedback are welcome.
