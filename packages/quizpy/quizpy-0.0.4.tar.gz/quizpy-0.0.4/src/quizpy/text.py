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

from .common import Question
from .multipe_choice import Choice


@dataclass
class ShortAnswer(Question):
    """Question type asking for a one-line answer.

    :param case_sensitive: If `True`, the given answer must match the solution exactly.
    :type case_sensitive: bool
    """
    case_sensitive: bool = False
    accepted_answers: typing.List[Choice] = field(default_factory=list)

    def add_answer(self, text: str, fraction: float, feedback: str = '', format: str = 'html') -> Choice:
        """Convenience method to add an answer to the question.

        The answer itself is the same `Choice` object that MultipleChoice questions use.

        :param text: The source text to be rendered for this answer option.
        :type text: str

        :param fraction: The fraction of the total points to be given for this answer as percentage between 0 and 100.
        :type fraction: float

        :param feedback: Specific feedback for choosing this answer option
        :type feedback: str

        :param format: format for rendering both answer text and feedback.
            Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.

        :returns: The newly added Choice object.
        :rtype: quizpy.Choice
        """

        c = Choice(text, fraction, feedback, format)
        self.accepted_answers.append(c)
        return c

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('shortanswer')
        ET.SubElement(node, 'usecase').text = '1' if self.case_sensitive else 0

        for answer in self.accepted_answers:
            node.append(answer.to_xml())

        return node

    def to_cloze(self, weight: int) -> str:
        """Renders a `ShortAnswer` question in Cloze format to be used as an inline question.

        :param weight: The weight of the question in the total sum of all inline questions.
        :type weight: int
        """
        cloze = f"{weight}:SA:" if not self.case_sensitive else f"{weight}:SAC:"

        cloze += '~'.join(map(lambda s: s.to_cloze(), self.accepted_answers))

        return f"{{{cloze}}}"


class Description(Question):
    """Dummy question type with no grading e.g. to establish some context for further questions."""

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('description')
        return node


@dataclass
class Essay(Question):
    """Question with free-form multiline text answer that must be graded manually.

    .. note:: Moodle allows you to restrict file types of attachements. However, we do not fully understand how this
              works yet.

    :param grading_info: Text to be displayed for the grader (students will never see this)
        e.g. to establish rules for grading. Will be formatted in the question format.

    :type grading_info: str

    :param response_format: Defines how a student can provide an answer. Can be one of the following options:

        * "editor": Standard HTML editor (with possibility to add pictures)
        * "editorfilepicker": Same as editor but with file upload option
        * "plain": Unformatted plain text input.
        * "monospaced": Unformatted plain text input in monospace font.
        * "noinline": No text input field. This requires `attachements_required = True` and `max_attachments > 0`.

    :type response_format: str

    :param response_required: If `True`, a student must enter some text before submitting the answer.
    :type response_required: bool

    :param response_template: A formatted text that is automatically entered as a template for the student.
    :type response_template: str

    :param attachements_required: If `True`, a student must submit a file before submitting the answer.
    :type attachements_required: bool

    :param max_attachements: The maximum number of attachements a student can supply for an answer.
    :type max_attachements: int

    :param max_lines: The maximum number of lines of text an answer can have.
    :type max_lines: int
    """
    grading_info: str = ""
    response_format: str = "editor"
    response_required: bool = True
    response_template: str = ""
    attachements_required: bool = False
    max_attachements: int = 0
    max_lines: int = 15

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('essay')

        ET.SubElement(node, 'responseformat').text = self.response_format
        ET.SubElement(node, 'responserequired').text = '1' if self.response_required else '0'
        ET.SubElement(node, 'responsefieldlines').text = str(self.max_lines)
        ET.SubElement(node, 'attachements').text = str(self.max_attachements)
        ET.SubElement(node, 'attachementsrequired').text = '1' if self.attachements_required else '0'

        grading_info = ET.SubElement(node, 'graderinfo')
        grading_info.set('format', self.format)
        ET.SubElement(grading_info, 'text').text = self.grading_info

        template = ET.SubElement(node, 'responsetemplate')
        template.set('format', self.format)
        ET.SubElement(template, 'text').text = self.response_template

        return node


class Cloze(Question):
    """The question text will be rendered using the custom Cloze syntax.
    See https://docs.moodle.org/310/en/Embedded_Answers_(Cloze)_question_type.

    You can also use the `to_cloze()` functions of the relevant question classes to generate the syntax for you.
    """

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('cloze')
        return node
