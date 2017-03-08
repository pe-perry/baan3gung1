## baan3gung1

*Current version: 0.1.5*

baan3gung1 (Cantonese: 扮工) means a worker pretends to work,
but in fact he/she is not.

This package was created for me to 'baan3gung1' and practise my Python
skills initially. It's still in its development stage. It would be
appreciated if you find any issues and report them
[here](https://github.com/kitman0804/baan3gung1/issues).

Currently, the users of this package can 'browse' the following
websites on console.

1. LIHKG (one of the most popular forums in Hong Kong).

To be added:

- Reply function for LIHKG.
- JobsDB (a famous Job searching website in Hong Kong).

---

## Installation

First, you need Python 3. Sorry for those Python 2 users.

If you don't have python 3 installed in your computer, you can download
it from the following links and install:

- [Anaconda (Recommended)](https://www.continuum.io/downloads)
- [python.org](https://www.python.org/downloads/)
- [Enthought Canopy](https://www.enthought.com/products/canopy/)

You are also required to install `requests`, `lxml`, `BeautifulSoup`
before using.

**Method 1:**

1. Run the follow command.

```
pip install git+https://github.com/kitman0804/baan3gung1.git
```

**Method 2:**

1. Download the repository.

2. Run the following command in the downloaded directory.

```
python setup.py install
```

---

## Examples

```
import baan3gung1
from baan3gung1 import lihkg

# Settings
## Set headers
baan3gung1.settings.HEADERS = {
    'User-Agent': 'baan3gung1zai2.'
}

## Set connect and read timeout (3.05s & 60s).
baan3gung1.settings.TIMEOUT = (3.05, 60)

## Set min. sleep time between requests (5s).
baan3gung1.settings.MIN_SLEEP_TIME = 5


# Show all threads in the page 1 of Channel 2 (Hot).
lihkg.Channel.get_channel(2).show()

# Search threads related to 'api'.
lihkg.Channel.search('api', count=20).show()

# Show all posts(/replies) in thread 1 (5s/page).
lihkg.Thread.get_thread(1, time_interval=5).show()
```

---

## Version

**Version 0.1.5**

- Fixed settings bugs: Users' settings on `HEADERS`, `TIMEOUT` and
`MIN_SLEEP_TIME` now take effect.
- `baan3gung1.settings.SLEEP_TIME` has been renamed as
`baan3gung1.settings.MIN_SLEEP_TIME`.

**Version 0.1.4**

- Users can now set their own `HEADERS`, `TIMEOUT` and `SLEEP_TIME`.
- Added more controls on full width and half width text.

**Version 0.1.3:**

- Fixed unexplainable BeautifulSoup issues in Mac OS.
- Added full width name.

**Version 0.1.2:**

- Minor fixes.

**Version 0.1.1:**

- Fixed Channel.search.

**Version 0.1:**

- Hello world.
- Users can now read the threads and posts posted on LIHKG.

