#    Quizpy - Creating Moodle exams in Python
#    Copyright (C) 2021  Sebastian Bräuer
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
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import xml.etree.ElementTree as ET
import typing

from dataclasses import dataclass, field
from .common import Question, InlineFile


# TODO Question Type ddwtos

@dataclass
class DragOption:
    """Represents an answering option box to be placed on a DropZone within a DDImage.

    :param text: The text on the box. This is treated as plain text without any markup.
    :type text: str

    :param group: Options can be grouped so that options with the same group number have the same shape that
                  is also represented in the DropZone, i.e. DragOptions can only be dragged on DropZones whos DragOption
                  is in the same group.
    :type group: str

    :param infinite: If `True` the option can be placed on an infinite number of DropZones.
    :type infinite: bool

    """
    text: str
    group: int = 1
    infinite: bool = False


@dataclass
class DropZone:
    """Represents a box in which a user can drop an answer on in a DDImage question.

    :param location: x,y coordinates of the drop zone relativ to the top left corner of the base image.
    :type location: typing.Tuple[int, int]

    :param choice: a reference to the `DragOption` that represents the correct answer for this field.

        .. attention:: choice must be a valid reference to a DragOption in DDImage.options

    :type choice: DragOption

    :param text:
        .. note:: TODO: Find out what this actually does. It is visible in the editor but seemingly not in the question?!
    """
    location: typing.Tuple[int, int]
    choice: DragOption
    text: str = ""

@dataclass
class DDText(Question):
    """This question type allows a student to drop answers on gaps in a given text.

    Gaps in the question text are created by using [[n]] references, where n is the 1-based index of the options.

    :param shuffle: If `True`, drag options will be sorted randomly each time the question is presented.
    """

    options: typing.List[DragOption] = field(default_factory=list)
    shuffle: bool = False

    def add_option(self, text: str, group: int = 1, infinite: bool = False) -> DragOption:
        """Adds an DragOption to the DDImage question and returns the newly created instance.

        :param text: The text on the box. This is treated as plain text without any markup. No line breaks!
        :type text: str

        :param group: Options can be grouped so that options with the same group number have the same color that
                      is also represented in the gap.
        :type group: str

        :param infinite: If `True` the option can be placed on an infinite number of DropZones.
        :type infinite: bool
        """

        c = DragOption(text, group=group, infinite=infinite)
        self.options.append(c)
        return c

    def to_xml(self) -> ET.Element:

        node = self.generate_common_xml('ddwtos')

        if self.shuffle:
            ET.SubElement(node, "shuffleanswers").text = '1'

        for o in self.options:
            dragbox = ET.SubElement(node, "dragbox")

            ET.SubElement(dragbox, 'text').text = o.text
            ET.SubElement(dragbox, 'group').text = str(o.group)

            if o.infinite:
                ET.SubElement(dragbox, 'infinite')

        return node


@dataclass
class DDImage(Question):
    """This question type allows a student to drop answers on custom-placed fields on a background image.

    :param base_image: an `InlineFile` instance that serves as the background to the question.

        .. attention:: Although this (for technical reasons) defaults to `None` you need to provide a background image
                       before you can call `to_xml()`!

    :type base_image: quizpy.InlineFile

    :param shuffle: If `True`, drag options will be sorted randomly each time the question is presented.
    """

    base_image: InlineFile = None  # Unfortunately,  this must be set with a default
    options: typing.List[DragOption] = field(default_factory=list)
    drops: typing.List[DropZone] = field(default_factory=list)
    shuffle: bool = False

    def add_option(self, text: str, group: int = 1, infinite: bool = False) -> DragOption:
        """Adds an DragOption to the DDImage question and returns the newly created instance.

        :param text: The text on the box. This is treated as plain text without any markup.
        :type text: str

        :param group: Options can be grouped so that options with the same group number have the same shape that
                      is also represented in the DropZone, i.e. DragOptions can only be dragged on DropZones whos DragOption
                      is in the same group.
        :type group: str

        :param infinite: If `True` the option can be placed on an infinite number of DropZones.
        :type infinite: bool
        """

        c = DragOption(text, group=group, infinite=infinite)
        self.options.append(c)
        return c

    def add_dropzone(self, location: typing.Tuple[int, int], correct_choice: DragOption, text: str = "") -> DropZone:
        """Adds an DropZone to the DDImage question and returns the newly created instance.

        :param location: x,y coordinates of the drop zone relativ to the top left corner of the base image.
        :type location: typing.Tuple[int, int]

        :param correct_choice: a reference to the `DragOption` that represents the correct answer for this field.

        .. attention:: choice must be a valid reference to a DragOption in DDImage.options

        :type choice: DragOption

        :param text:
             .. note:: TODO: Find out what this actually does. It is visible in the editor but seemingly not in the question?!

        """
        d = DropZone(location, correct_choice, text=text)
        self.drops.append(d)
        return d

    def to_xml(self) -> ET.Element:

        if self.base_image is None:
            raise ValueError("You need to set a base image!")

        node = self.generate_common_xml('ddimageortext')

        if self.shuffle:
            ET.SubElement(node, "shuffleanswers")

        node.append(self.base_image.to_xml())

        for i, opt in enumerate(self.options, start=1):
            drag = ET.SubElement(node, 'drag')
            ET.SubElement(drag, 'text').text = opt.text
            ET.SubElement(drag, 'draggroup').text = str(opt.group)
            ET.SubElement(drag, 'no').text = str(i)

            if opt.infinite:
                ET.SubElement(drag, 'infinite')

        for i, d in enumerate(self.drops, start=1):
            x, y = d.location
            drop = ET.SubElement(node, 'drop')
            ET.SubElement(drop, 'text')  # Empty sub-element
            ET.SubElement(drop, 'xleft').text = str(x)
            ET.SubElement(drop, 'ytop').text = str(y)
            ET.SubElement(drop, 'no').text = str(i)

            try:
                ET.SubElement(drop, 'choice').text = str(self.options.index(d.choice) + 1)
            except ValueError:
                raise ValueError("Choice for dropzone not found in drag options!")

        return node
