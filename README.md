# nb2hugo

*nb2hugo* is a simple way to convert a Jupyter notebook to a Hugo markdown page.


## Motivation

Jupyter Notebook is a great way to create a single document that contains code that can be executed, formatted text to provide detailed explanations, as well as figures. Hugo is a simple yet very powerful static site generator. While a few solutions to convert a Jupyter notebook to a Hugo markdown with front matter already exist, *nb2hugo* put an emphasis on getting a result that looks similar to the original Jupyter notebook.


## Installation

Using pip:
```
pip install nb2hugo
```


## Usage

In your python notebook, start by using one or more markdown cells that will contain the front matter information. Next, add an html comment as a front matter divider: everything in the notebook before the End Of Front Matter divider `<!--eofm-->` will be the front matter. This approach is similar to the one used for [content summaries](https://gohugo.io/content-management/summaries/).  
A markdown title before the `<!--eofm-->` divider will automatically become the front matter title. You can also provide other front matter fields by writting pairs of "key: value" on different lines.  
Below is an example of a notebook markdown cell that will become a front matter:

```text
# My notebook title

Date: 2018-06-01  
Author: firstname lastname  
Categories: category1, category2  
Tags: tag1, tag2, tag3  
<!--eofm-->
```

All content after the `<!--eofm-->` divider will be considered as normal notebook content.

Once you have finished writing your notebook, you can convert it using the following command:

```bash
nb2hugo notebook_file --site-dir hugo_website_directory --section content_section
```


## Author

**Vincent Lunot** - *Initial work*


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


## Acknowledgements

*nb2hugo* is based on [nbconvert](https://github.com/jupyter/nbconvert)
