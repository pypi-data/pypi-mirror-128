## ref.py
## Jacob Westerberg
## Vanderbilt University
## jakewesterberg@gmail.com
## Created: 2021-11-18
## Updated: 2021-11-18

## MIT License
## Copyright (c) 2021 Jacob Westerberg
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

def ref(data_in, method = "CAR", ref_chs = 0:-1, app_chs = 0:-1):

    ## common average reference method
    if method == "CAR":

        dim1 = np.size(data_in(0, app_chs, 0))

        data_out = data_in
        data_out = data_in(:, app_chs, :) - \
            tile(np.nanmean(data_in(:,ref_chs,:), axis = 1), \
            (np.size(data_in, 0), dim1, np.size(data_in, 2)))

    return data_out
