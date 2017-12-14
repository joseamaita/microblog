# Getting Started with Flask and Microblog

## Set and unset environment variables for 'venv'

To do this, first navigate to the repository folder:

```
$ cd microblog.git/
```

There, to edit the `activate` script within `venv`, type:

```
$ vim venv/bin/activate
```

Add the environment variable to the end of the file with the `export` 
command like this:

```
export FLASK_APP=microblog.py
```

Make sure to set a similar hook to unset the environment variable by 
locating the `deactivate` definition and using the `unset` command at 
the end of such definition:

```
deactivate () {
    ...

    # Unset variable
    unset FLASK_APP
}
```

Save and close the `activate` script with `:wq!`.

To test the configuration, activate `venv` and search the `FLASK_APP` 
environment variable like this:

```
$ source venv/bin/activate
(venv) $ env | grep "FLASK_APP"
FLASK_APP=microblog.py
```

Finally, deactivate `venv` and make sure `FLASK_APP` is not reachable:

```
(venv) $ deactivate
$ env | grep "FLASK_APP"
(nothing is shown)
```
