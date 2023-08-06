# Terminal

![Tests](https://github.com/tristanmsct/Terminal/actions/workflows/tests.yml/badge.svg)
![Coverage](https://cdn.jsdelivr.net/gh/tristanmsct/Terminal/coverage.svg)

## How to install

First download the whole thing and unzip it. Then navigate to the package directory. Typically :

`$ cd ~/Downloads/Terminal`

You can use the installer :

`$ ./install`

Or you can paste the "terminal" directory in the site-package of your python installation. The ./install file take care of that and install the package in your current python environment while also install all the dependencies.

## How to use terminal

Content of the `demo.py` file :

```Python
# Packages
from terminal import InputManager as im

# %% Read line function

# Open question
str_name = im.read_line('What is your name ?\n')
print(f'Hello, {str_name}.')

# Closed question
str_fruit = im.read_line('Do you prefere apples or pears ?\n', bl_case=False, lst_values=['Apples', 'Pears'])
print(f'I too like {str_fruit.lower()} :).')

# %% Yes or No questions

# By default recognize (yes, y, oui and o) as yes, and (no, n and non) as no.
im.read_yes_no('Proceed ? [y/n]\n')

# This can be changed
im.read_yes_no('Continuar ? [Si/No]\n', lst_pos_vals=['Si', 's'], lst_neg_vals=['No', 'n'])

# %% Read numeric

# Basic numeric read
int_res = im.read_numeric('Choose a numer :\n')
print(f'You chose {int_res}.')

# This function can be tweaked with some parameters :

int_res = im.read_numeric('Choose a number between 1 and 10 :\n', bl_int=True,
                          num_lb=1, num_ub=10, bl_inc_lb=True, bl_inc_ub=True)
print(f'You chose {int_res}.')

# %% Force read

# In order not to crash on a bad input, you can use the force_read function
int_res = im.force_read(im.read_numeric, 'Choose a number between 1 and 10 :\n', bl_int=True,
                        num_lb=1, num_ub=10, bl_inc_lb=True, bl_inc_ub=True)
print(f'You chose {int_res}.')
```
