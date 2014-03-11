#!/usr/bin/env python
# -*- coding: utf8 -*-

# My imports
from __future__ import division
import numpy as np
import re


class Filehandler():

    """
    This class will make your life SO much easier and make me famous! ;)

    Parameters
    ----------
    template : ASCII
        A template for the datafile that should be created. We just need the
        PATH here.
    data : matrix
        Preferably a numpy array with all the data we want to copy in to the
        datafile with the same format as 'template'.
    fname : filename or file handle
        If the filename ends in ``.gz``, the file is automatically saved in
        compressed gzip format.  `loadtxt` understands gzipped files
        transparently.
    skipheader : int
        Skip the first n lines of the template (this will be copied to the
        datafile, if no new header is supplied).
    header : str
        If None the header from the template will be copied to the datafile.
        Otherwise this string will be used as the new header.
    comments : str, optional
        String that will be prepended to the ``header`` and ``footer`` strings,
        to mark them as comments. Default: '# ',  as expected by e.g.
        ``numpy.loadtxt``.
    """

    def __init__(self, template, data, output, skipheader=None, header=None,
                 comments='#'):
        self.template = template
        self.data = data
        self.output = output
        self.comments = comments

        # TODO - need to make this work better, so I'm able to read the ugly
        # data
        if type(self.data) is not np.ndarray:
            try:
                self.data = np.array(self.data)
            except:  # Which error do we expect here
                print "Not able to convert data to a numpy array!"

        self.skipheader = skipheader
        try:
            self.skipheader = int(abs(self.skipheader))
        except TypeError:
            print "Warning: The skipheader argument must be a positive integer"
            print "         Setting the skipheader to 0 (no header added).\n"
            self.skipheader = 0
        
        self.header = header
        if self.header == None:
            print "The header argument was set to None. No header will be added."
            self.header = ''
        if self.header.count('\n') + 1 != self.skipheader:
            print "Warning: The length of the header is different from the"
            print "         skipheader paramter.\n"

    def create_header(self):
        if self.header == '':
            with open(self.template, "r") as tmp:
                self.header = ''
                for i in xrange(self.skipheader):
                    self.header += tmp.readline()
            return self.header[0:-1]
        else:
            return self.header

    def fmt_from_template(self):
        # Large part of this is from
        # www.stackoverflow.com/questions/21865757/use-python-to-handle-and-create-input-files-for-external-software
        with open(self.template, "r") as tmp:
            # Getting 1 line with the data to extract the format.
            if self.skipheader != 0:
                for i in xrange(self.skipheader):
                    z = tmp.readline()
                del z
                tmpl = tmp.readline()
            else:
                tmpl = [line.strip() for line in tmp][-1]
            if tmpl[-1::] == '\n':  # Don't want the '\n' in the end
                tmpl = tmpl[:-1]

        pat = r'( *-?\d+\.(\d+))'
        fmt = []
        while tmpl:
            match = re.search(pat, tmpl)
            if match:
                x = len(match.group(1))
                d = len(match.group(2))
                fmt += ['%%%d.%df' % (x, d)]
                tmpl = tmpl[x:]
        fmt = ''.join(fmt)
        return fmt

    def create(self):
        fmt = self.fmt_from_template()
        self.header = self.create_header()
        with open(self.output, 'w') as f:
            np.savetxt(f, self.data, fmt, header=self.header,
                    comments=self.comments)
            print "Data saved in", self.output


def main():
    data = np.loadtxt("data.dat")
    template = "template.txt"
    header = 'This is a header\nAnd a second line\nAnd when everything is beautiful'

    t = Filehandler(template, data, "result.dat", skipheader=3, header=header,
            comments=' ')
#    t = Filehandler(template, data, "result.dat", header=header)
#    t = Filehandler(template, data, "result.dat")
    t.create()


if __name__ == '__main__':
    main()
