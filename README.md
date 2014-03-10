====================
PyFilehandler README
====================

PyFilehandler is a program used to create data files for external software that
requires a number of spaces between the columns.


**Requirements**

python
numpy>=1.7


**Example**

 >>> import PyFilehandler
 >>> data = np.loadtxt("data.dat")
 >>> template = "template.dat"
 >>> header = "This is a new header"
 >>> output = "final.dat"
 >>> example = Filehandler(template, data, output, header=header, comments='')
 >>> example.create()
 Data saved in final.dat
