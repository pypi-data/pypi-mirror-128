# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "08/04/2020"


from Orange.widgets.widget import OWWidget, Input, Output
from darfix.gui.metadataWidget import MetadataWidget
from darfix.core.process import DataPassThrough


class MetadataWidgetOW(OWWidget):
    """
    Widget to select the data to be used in the dataset.
    """

    name = "metadata"
    icon = "icons/metadata.svg"
    want_main_area = False
    ewokstaskclass = DataPassThrough

    # Inputs
    class Inputs:
        dataset = Input("dataset", tuple)

    # Outputs
    class Outputs:
        dataset = Output("dataset", tuple)

    def __init__(self):
        super().__init__()

        self._widget = MetadataWidget()
        self.controlArea.layout().addWidget(self._widget)

    @Inputs.dataset
    def setDataset(self, _input):
        if _input:
            dataset, update = _input
            if dataset:
                self._widget.setDataset(*dataset)
            else:
                self._widget.clearTable()
