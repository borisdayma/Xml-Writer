'''\
Convenient way to write xml in python 3

Copyright 2011 Boris Dayma

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Example (launch it with "python xml_writer.py"):
from xml_writer import xml_writer
xml = xml_writer()
with xml.data:
    xml.name('Toto')
    xml.friend
    with xml.entry(Id='4'):
        xml.visit('Lunch', time = '12h45', day = 'Wednesday')
        xml.summary('Lunch with friends')
    xml.address(country="France", city="Marseille")
'''


# Standard global data
__all__ = ['xml_writer']
__license__ = 'GNU Lesser General Public License v3.0'
__version__ = '0.1'
__author__ = "Boris Dayma <http://github.com/borisd13/>"
__credits__ = "Jonas Galvez <http://jonasgalvez.com.br/>"



class xml_writer:
    
    def __init__(self):
        self.indent = 0
        self.attrib = None
        self.list_lines = []
        self.blocs = []
        self.kargs_mem = dict()
        self.arg0 = None

        self.list_lines.append('<?xml version="1.0" encoding="UTF-8" ?>')

    def __enter__(self):
        self.list_lines.pop()
        list_args = ''.join([' {}="{}"'.format(key,
                    value) for (key, value) in self.kargs_mem.items()])
        self.list_lines.append('{}<{}{}>'.format(self._indent(),
                                            self.attrib, list_args))
        self.indent += 1
        if self.arg0 is not None:
            self.list_lines.append('{}{}'.format(self._indent(),
                                            self.arg0))      
        self.blocs.append(self.attrib)
        return(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.indent -= 1
        out = self.blocs.pop()
        self.list_lines.append('{}</{}>'.format(self._indent(), out))

    def __call__(self, *args, **kargs):
        self.list_lines.pop()
        self.kargs_mem = kargs
        list_args = ''.join([' {}="{}"'.format(key,
                    value) for (key, value) in kargs.items()])
        if ((len(args) == 0) or (args[0] is None)):
            self.list_lines.append('{}<{}{} />'.format(self._indent(),
                                            self.attrib, list_args))
        else:
            self.arg0 = args[0]
            self.list_lines.append('{0}<{1}{2}>{3}</{1}>'.format(self._indent(),
                                            self.attrib, list_args, args[0]))
        return self

    def __str__(self):
        return '\n'.join(self.list_lines)

    def __getattr__(self, name):
        self.attrib = name
        self.kargs_mem = dict()
        self.arg0 = None
        self.list_lines.append('{}<{} />'.format(self._indent(), name))
        return self

    def _indent(self):
        return('\t' * self.indent)


if __name__ == '__main__':
    xml = xml_writer()
    with xml.data:
        xml.name('Toto')
        xml.friend
        with xml.entry(Id='4'):
            xml.visit('Lunch', time = '12h45', day = 'Wednesday')
            xml.summary('Lunch with friends')
        xml.address(country="France", city="Marseille")
    print(xml)
