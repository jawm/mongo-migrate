# mongo-migrate

This is just a very basic tool for creating mongo migration scripts.

Usage if fairly simple, just:

```
python migrate.py create Brief Description Here
```

This will generate a script with the description in the name, as well as a timestamp when it was created (to mitigate name collisions, and help order running of the scripts)

The generated file is Javascript, with a small amount of boiler plate code included.

Running all scripts that have not yet been run is easy

```
python migrate.py update
```

If you want to run the scripts on a a specific host, use the `-h` flag when running `update` like so

```
python migrate.py update -h example.com
```

Similarly if you wish to change the port use `-p`

```
python migrate.py update -p 30001
```

By default these values will be 'localhost' and 27017 respectively.

There is also an included `include.js` file which by default is included in all the scripts.
You can put whatever utility functions you wish in here. I've included a function `i(variable)`, which converts a number to be an integer for Mongo (because Javascript doesn't have integers by default)

### Note:

The tool keeps track of which migrations have been ran using a special database 'dev_db'.
If you want to change this, just edit the code, perhaps in future i'll add a flag for `update` to change this.

### Dependencies:

Up to date version is in `requirements.txt`
In short the only external dependency you'll need is PyMongo.

---
