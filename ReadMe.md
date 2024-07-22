# Project Description

This project introduced a test framework to validate 17 different finance reports, and 17 templates to compare reports
from 2 systems on varied metrics:

* Stock
* Sales (by Category, or supplier name)
* Transaction
* Import summary
* Import invoice
* Inventory
* Counting
* Export
* Export invoice
* Basic information

# Scripts for GitHub

## push to remote git repo

```
git push -u origin master
```

## start the validation script

In ```main.py```, comment out the line that calls the corresponding template function, and run ```main.py```.