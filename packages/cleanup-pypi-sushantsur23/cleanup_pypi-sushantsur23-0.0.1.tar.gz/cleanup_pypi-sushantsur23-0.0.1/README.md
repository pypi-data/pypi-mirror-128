# cleanup_pypi

#Reference for creating python package
[official python page](https://packaging.python.org/tutorials/packaging-projects/)

#Reference URL
[URL helpful for creating python package](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-nodejs-or-python?langId=py)



### This library has 3 functions:- 
``` 
1) replacing null values
2) standardization the column values 
3) finding the variance_inflation_factor value column wise
```
## Points to keep a note

    The base minimum parameter which it expects is either a numpy array or a DataFrame.

    The only things we need to keep in mind is make sure there is no column in date format if so once you have preprocessed it then use these functions.
    If any column has values in dataformat then it may give error.
    Also in case of a DataFrame kindly ensure the first column is target column or dependent column. Only then start using this function.


WHAT IS AN ISSUE??