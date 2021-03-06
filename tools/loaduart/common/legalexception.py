# Legal exception toolbox
#
#    Copyright (C) 2009 Louis Caron
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

class LegalException(Exception):
    "class representing an exception handled by the tool"
    def __init__(self, value, errornumber=0):
        # convert the value parameter into a string for print
        if isinstance(value, str):
            self.value = value
        else:
            self.value = repr(value)
        # record the errornumber to return to the OS
        self.errornumber = errornumber
    def __str__(self):
        "convert the exception into a string"
        return self.value



    
