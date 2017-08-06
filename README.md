muse
==============
cloud music library

Requirements
-------------
- Python 3.6+
- pip (see `requirements.txt`)


Install
------------

```sh
$ cd muse
$ chmod +w data temp
$ pip install --require requirements.txt
$ python muse/db.py  # initialize db
```

Run app
--------------

```sh
$ python app.py
```

API
----------
- `GET /musics` get musics as json
- `GET /musics/:id` get music as json
- `POST /musics` add music
