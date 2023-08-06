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

import typing
import base64
import abc
import xml.etree.ElementTree as ET
import os

from dataclasses import dataclass, field

@dataclass
class InlineFile:
    """Helper class to attach and reference files directly in the XML file.

    :param name: Name of the file including the file extension.
    :type name: str

    :param file: File-like object to read data from. Must be opened in binary mode.
    :type name: typing.BinaryIO
    """
    name: str
    file: typing.BinaryIO

    @classmethod
    def load(cls, path: str):
        """Open a file in binary-mode and use the file handle to instantiate an InlineFile."""
        f = open(path, 'rb')
        return cls(os.path.basename(path), f)

    def to_xml(self) -> ET.Element:
        """Reads the file and turns it into `file` node in XML. If the file is seekable it will be read from the start."""
        if self.file.seekable():
            self.file.seek(0)

        node = ET.Element('file')
        node.set('name', self.name)
        node.set('path', '/')
        node.set('encoding', 'base64')

        node.text = base64.standard_b64encode(self.file.read()).decode('utf-8')

        return node

    def link(self):
        """Returns a string that Moodle can use to reference the file. Useful for e.g. links to pictures.

        :rtype: str
        """
        return f'@@PLUGINFILE@@/{self.name}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


@dataclass
class Question(abc.ABC):
    """Abstract base class for all question types.

    :param title: The question title
    :type title: str

    :param text: The full question text in its raw form.
    :type text: str

    :param default_points: The base number of points given for this question. This can be scaled in the actual quiz on moodle.
    :type default_points: float

    :param format: The format of the question text. Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.
    :type format: str

    :param id: Apparently moodle supports some kind of questions identifiers. We have no idea, how.
    :type id: int

    :param tags: A set of tags to group questions by. Unfortunately, not yet fully supported in moodle.
    :type tags: typing.Iterable[str]

    :param penalty: A penalty factor for in case of retries. Only applies if retry is possible for the quiz.
    :type penalty: float

    :param hidden: A marker to prevent 'old' questions from being displayed in the category.
    :type hidden: bool

    :param general_feedback: Feedback that will be shown after the question was answered (but during the quiz!). Will be rendered in the same format as the question text.
    :type general_feedback: bool

    :param files: A list of `InlineFiles` that can be referenced in the question text (e.g. pictures).
    :type files: typing.List[InlineFile]
    """
    title: str
    text: str
    default_points: float

    format: str = 'html'
    id: int = None
    tags: typing.Iterable[str] = field(default_factory=list)
    penalty: float = 0.0
    hidden: bool = False
    general_feedback: str = ''

    files: typing.List[InlineFile] = field(default_factory=list)

    def generate_common_xml(self, qtype: str) -> ET.Element:
        """Generates XML node with attributes common to all question types.

        :param qtype: the XML-question type
        :type qtype: str
        """
        node = ET.Element('question')
        node.set('type', qtype)

        name = ET.SubElement(node, 'name')
        ET.SubElement(name, 'text').text = self.title

        text = ET.SubElement(node, 'questiontext')
        text.set('format', self.format)
        ET.SubElement(text, 'text').text = self.text

        for inline in self.files:
            text.append(inline.to_xml())

        feedback = ET.SubElement(node, 'generalfeedback')
        feedback.set('type', self.format)
        ET.SubElement(feedback, 'text').text = self.general_feedback

        ET.SubElement(node, 'defaultgrade').text = str(self.default_points)
        ET.SubElement(node, 'penalty').text = str(self.penalty)
        ET.SubElement(node, 'hidden').text = '1' if self.hidden else '0'
        ET.SubElement(node, 'idnumber').text = str(self.id) if self.id is not None else ''
        return node

    @abc.abstractmethod
    def to_xml(self) -> ET.Element:
        pass



@dataclass
class Category:
    """Represents a group of questions within one XML-file.

    :param name: The category name that will be displayed in Moodle.
    :type name: str

    :param description: A long formatted description of the content.
    :type description: str

    :param format: The format used to render the description.
        Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.
    :type format: str
    """
    name: str
    description: str = ''
    questions: typing.List[Question] = field(default_factory=list)
    format: str = 'html'

    def to_xml(self) -> typing.List[ET.Element]:
        nodes = []

        category = ET.Element('question')  # Dummy question node
        category.set('type', 'category')

        name = ET.SubElement(category, 'category')
        ET.SubElement(name, 'text').text = self.name

        info = ET.SubElement(category, 'info')
        info.set('format', self.format)
        ET.SubElement(info, 'text').text = self.description

        nodes.append(category)

        for q in self.questions:
            nodes.append(q.to_xml())

        return nodes


@dataclass
class Quiz:
    categories: typing.List[Category] = field(default_factory=list)

    def to_xml(self) -> ET.Element:
        root = ET.Element('quiz')

        for c in self.categories:
            root.extend(c.to_xml())

        return root

    def add_category(self, name: str, description: str = '', format: str = 'html') -> Category:
        cat = Category(name, description=description, format=format)
        self.categories.append(cat)
        return cat

    def export(self, path):
        with open(path, 'wb') as f:
            tree = ET.ElementTree(self.to_xml())
            tree.write(f, encoding='UTF-8', xml_declaration=True)
