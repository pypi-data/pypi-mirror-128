## csd.py
## Jacob Westerberg
## Vanderbilt University
## jakewesterberg@gmail.com
## Created: 2021-11-14
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

def csd(data_in, data_spc, units = "uV", cndt = 0.0004):

    ## data_in: LFP sample x channel x trial matrix
    ## data_spc: spacing between channels in mm
    ## units: data units
    ## cndt: conductivity estimate

    ## data_out: CSD sample x channel x trial matrix

    ## convert to uV
    if units == "V":
        data_in = data_in * 1000000
    elif units == "mV":
        data_in = data_in * 1000

    ## define channel info
    nChan       = size(t_csd_1, 1) * spc
    dChan       = np.arrange([spc, nChan, spc])
    nE          = len(dChan)
    d           = mean(diff(dChan))

    ## initialize output array
    data_out = np.nan([np.size(data_in, 0), np.size(data_in, 1)])

    ## generate differentiation matrix
    diff_mat = np.nan([np.size(data_in, 0), np.size(data_in, 1)])
    for j in range(nE):
        for k in range(nE)
            if j == (j - 1)
                diff_mat(j, k) = -2 / d^2
            elif abs(j - k + 1) == 1
                diff_mat(j, k) = 1 / d^2
            else
                diff_mat(j, k) = 0

    ## loop through trials
    for i in range(np.size(data_in, 2)):

        ## differentiate, ohm's law convert, convert to nA/mm3
        data_out(:, 1:-2, i) = -1 * cndt * diff_mat * data_in[:, :, i] * 1000

    return data_out
