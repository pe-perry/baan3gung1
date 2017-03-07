## baan3gung1

baan3gung1 (*in Cantonese 扮工*) means a worker pretends to work,
but in fact he/she is not working.

This package was created for me to 'baan3gung1' initially. It is
still in its development stage, it would be appreciated if you can
report any issues found.

Currently, the users of this package can 'browse' the following
websites.

1. LIHKG (one of the most popular forums in Hong Kong).

To be added:

- JobsDB (a famous Job searching website in Hong Kong).

---

## Installation

First, you need Python 3.

If you don't have a python 3, you may download it in the following
links and install:

- [Anaconda](https://www.continuum.io/downloads)
- [python.org](https://www.python.org/downloads/)
- [Enthought Canopy](https://www.enthought.com/products/canopy/)

**Method 1:**

1. Run.

```
pip install git+https://github.com/kitman0804/baan3gung1.git
```

**Method 2:**

1. Download the repository.

2. Run the following code in the downloaded directory.

```
python setup.py install
```

---

## Examples

```
from bann3gung1 import lihkg

# Show all threads in the page 1 of Channel 2 (Hot).
lihkg.Channel.get_channel(2).show()

# Show all posts in thread 1 (5 seconds/page).
lihkg.Thread.get_thread(1, time_interval=5).show()
```

---

## Version

**Version 0.1.3:**

Fixed unexplainable BeautifulSoup issue in Mac OS.
Added full width name.

**Version 0.1.2:**

Minor fixes.

**Version 0.1.1:**

Fixed Channel.search.

**Version 0.1:**

Hello world.

Users can now read the threads and posts in LIHKG.

