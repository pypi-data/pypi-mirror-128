# Lysis-curve

This package generates automated lysis curves (bacterial growth curves) for 
biological research via **Plotly** and utilizes code for automated grouping, titles, annotations and subplotting within a single custom graphing function. 

Simply changing the function arguments can generate a variety of bacterial growth curves.

**The graphs are dynamic** when generated within a webpage (i.e. **Jupyter**) which can be useful when teasing apart data.

For a very similar package which generates non-dynamic but prettier bacterial growth curves / lysis curves using **R** rather than **Python**, see [Cody Martin's lysis_curves package.](https://github.com/cody-mar10/lysis_curves)

### Install Package Using [PyPi](https://pypi.org/project/lysis-curve/)
At the command line, run
```Bash
pip install lysis-curve
```

### Running (in Jupyter or at command line)

First, make sure your x-axis (time) data is your **zeroth (first) column** (this script always plots the first column in the csv file as the x-axis). Next, **make sure you save your data in the .csv file format.**

Next, navigate to the directory containing your .csv file in Jupyter.
```python
import os
os.chdir('your_path_here')
```
Next, import the lysis_curve.py file using 
```python
from lysis_curve import lysis_curve
```
Alternatively, copy/paste the file into a jupyter cell from github
and you can modify the code yourself.
#### Generate basic plot
```python
from lysis_curve import lysis_curve

lysis_curve('yourcsvfile.csv')
```
![basic plot](media/basic_example_plot.png)


#### Generate plot with grouping
This argument is useful if you wish to visually group your data by color. 
It automatically sets each line in each group the same color, 
but assigns them different markers.
*Does not work with subplots.*
Pass the argument to `group` as a list of strings, with each column in a group separated by vertical bars.
```python
lysis_curve('122120JSC.csv',
           title='Title Goes Here',
           group = ['1', '4','3|5'],
           annotate=True)
```
![basic_plot_with_grouping](media/example_plot_with_grouping_and_annotation.png)

#### Generate plot with annotations
Use the argument ```annotations=True``` and follow the prompts.

#### Generate plot with subplots
Use the argument ```subplots=True``` to split your data into subplots.

```Python
lysis_curve('051321JSC.csv',
           title='Title Goes Here',
           subplots=True)
```
![basic_plot_with_subplots](media/example_plot_with_subplots.png)
#### Generate plot with custom title
Use the argument ```title='Your Custom Title Here'```
By default, the title will be taken from your csv file name - thus 'yourcsvfile' if 'yourcsvfile.csv' is passed.

#### Pass custom colors
```python
lysis_curve('yourcsvfile.csv', colors=['red', 'blue', 'blah'])
```

#### Save as .png
Set the argument ```png=True``` and the function will generate a .png file of the graph in your current directory.

#### Save as .svg
Set the argument ```svg=True``` and the function will generate a .svg file of the graph in your current directory.
Requires Kaleido or Orca

### Save .png, .svg and legendless .svg
```save=True```
Saves three versions of the graph: (1) a .png version with a legend (2) a .svg version with a legend (3) a .svg version without a legend and square dimensions

### Dependencies

* Python 3.5+
* Pandas ```pip install pandas```
* Plotly ```pip install plotly```
* Requests ```pip install requests```
* Kaleido ```pip install kaleido``` (Kaleido is recommended over Orca according to Plotly)
