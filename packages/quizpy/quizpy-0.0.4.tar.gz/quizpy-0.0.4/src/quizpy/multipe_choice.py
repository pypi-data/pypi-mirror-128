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


@dataclass
class Choice:
    """Represents an answer option in a Multiple Choice question or a Short Answer question.

    :param text: The source text to be rendered for this answer option.
    :type text: str

    :param fraction: The fraction of the total points to be given for this answer as percentage between 0 and 100.
    :type fraction: float

    :param feedback: Specific feedback for choosing this answer option
    :type feedback: str

    :param format: format for rendering both answer text and feedback.
        Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.
    """
    text: str
    fraction: float  # TODO: Should this be int?

    feedback: str = ''
    format: str = 'html'

    def to_xml(self) -> ET.Element:
        answer = ET.Element('answer')
        answer.set('fraction', str(self.fraction))
        answer.set('format', self.format)

        ET.SubElement(answer, 'text').text = self.text
        fb = ET.SubElement(answer, 'feedback')
        fb.set('format', self.format)
        ET.SubElement(fb, 'text').text = self.feedback

        return answer

    def to_cloze(self) -> str:
        """Renders a cloze version of this choice.
        This method is called by the applicable question classes and should not be used directly.

        :return: A Cloze-representation of this choice.
        :rtype: str
        """
        if self.fraction == 100.0:
            s = f"={self.text}#{self.feedback}"
        elif self.fraction == 0.0:
            s = f"{self.text}#{self.feedback}"
        else:
            s = f"%{int(self.fraction)}%{self.text}#{self.feedback}"
        return s


@dataclass
class MultipleChoice(Question):
    """Standard Multiple choice question.

    :param shuffle: If `True` then answers will be shuffled every time they are presented in the quiz.
    :type shuffle: bool

    :param single: If `True` then only a single answer can be selected.
    :type single: bool

    :param numbering: Number answers with lowercase letters (`"abc"`), uppercase (`"ABC"`) or with integers (`"123"`)
    :type numbering: str

    :param correct_feedback: Feedback given for a fully correct answer (100%).
    :type correct_feedback: str

    :param partial_feedback: Feedback given for a partially correct answer (<100%).
    :type partial_feedback: str

    :param incorrect_feedback: Feedback given for a wrong answer (0%).
    :type incorrect_feedback: str
    """
    shuffle: bool = True
    single: bool = False
    numbering: str = 'abc'
    choices: typing.List[Choice] = field(default_factory=list)

    correct_feedback: str = 'Die Antwort ist richtig.'
    partial_feedback: str = 'Die Antwort ist teilweise richtig.'
    incorrect_feedback: str = 'Die Antwort ist falsch.'

    def add_choice(self, text: str, fraction: float, feedback: str = '', format: str = 'html'):
        """Convenience method to add a choice to the question.

        :param text: The source text to be rendered for this answer option.
        :type text: str

        :param fraction: The fraction of the total points to be given for this answer as percentage between 0 and 100.
        :type fraction: float

        :param feedback: Specific feedback for choosing this answer option
        :type feedback: str

        :param format: format for rendering both answer text and feedback.
            Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.

        :returns: The newly added choice.
        :rtype: Choice
        """

        c = Choice(text, fraction,feedback,format)
        self.choices.append(c)
        return c

    def to_xml(self):
        node = self.generate_common_xml('multichoice')
        node.set('type', 'multichoice')

        ET.SubElement(node, 'shuffleanswers').text = 'true' if self.shuffle else 'false'

        ET.SubElement(node, 'single').text = 'true' if self.single else 'false'
        ET.SubElement(node, 'answernumbering').text = self.numbering

        correct_feedback = ET.SubElement(node, 'correctfeedback')
        correct_feedback.set('format', self.format)
        ET.SubElement(correct_feedback, 'text').text = self.correct_feedback

        partial_feedback = ET.SubElement(node, 'partiallycorrectfeedback')
        partial_feedback.set('format', self.format)
        ET.SubElement(partial_feedback, 'text').text = self.partial_feedback

        wrong_feedback = ET.SubElement(node, 'incorrectfeedback')
        wrong_feedback.set('format', self.format)
        ET.SubElement(wrong_feedback, 'text').text = self.incorrect_feedback

        for c in self.choices:
            node.append(c.to_xml())

        return node

    def to_cloze(self, weight: int, display_type: str = "dropdown", alignment: str = 'horizontal', shuffle: bool = False) -> str:
        """Renders a MC question in Cloze format to be used as an inline question.

        :param weight: The weight of the question in the total sum of all inline questions.
        :type weight: int

        :param display_type: Determines how the question is rendered.
            Can either be `"dropdown"`, `"radio"` or `"checkbox"`.
        :type display_type: str

        :param alignment: If the `display_type` is "radio" or "checkbox" then you can choose between "horizontal" and
            "vertical" display of the radio buttons / checkboxes.
        :type alignment: str

        :param shuffle: If `True` the choices will be shuffled.
        :type shuffle: bool
        """

        if display_type not in {'dropdown', 'radio', 'checkbox'}:
            raise ValueError("display_type must be either 'dropdown', 'radio' or 'checkbox'!")

        if alignment not in {'horizontal', 'vertical'}:
            raise ValueError("alignment must be either 'horizontal', 'vertical'!")

        if display_type == 'dropdown':
            cloze_type = 'MC'
        elif display_type == 'radio':
            if alignment == 'horizontal':
                cloze_type = 'MCH'
            else:
                cloze_type = 'MCV'
        else:
            if alignment == 'horizontal':
                cloze_type = 'MRH'
            else:
                cloze_type = 'MR'

        if shuffle:
            cloze_type += 'S'

        cloze = f'{weight}:{cloze_type}:'
        cloze += '~'.join(map(lambda s: s.to_cloze(), self.choices))

        return f"{{{cloze}}}"


@dataclass
class MultiTrueFalse(Question):
    """Question, which displays a column of statements, which can be answered in a binary fashion (usually True/False).

    :param scoring_method: Can either be `"subpoints"` for partial points or `"mtfonezero"` for all-or-nothing scoring.
    :type scoring_method: str

    :param shuffle: If `True`, statements will be displayed randomly.
    :type shuffle: bool

    :param options: A list answering options for each statement. Defaults to `["Wahr", "Falsch"]`.
    :type options: typing.List[str]
    """
    scoring_method: str = 'subpoints'
    shuffle: bool = True
    options: typing.List[str] = field(default_factory=lambda: ['Wahr', 'Falsch'])
    statements: typing.List[typing.Tuple[str, str, str]] = field(default_factory=list)

    def add_statement(self, text: str, value: str, feedback: str = ''):
        """Adds a True/False statement to the question.

        :param text: Text of the statement to be shown. Will be formatted in the format of the question itself.
        :type text: str

        :param value: The correct value out of the available choices in `self.options`.
        :type value: str

        :param feedback: Feedback to be shown after the answer was submitted. Will be rendered in the question format.
        :type feedback: str

        :raises ValueError: if `value` is not an answering option
        """
        if value not in self.options:
            raise ValueError(f'The supplied value "{value}" is not an available answering option!')

        self.statements.append((text, value, feedback))

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('mtf')

        scoring = ET.SubElement(node, 'scoringmethod')
        ET.SubElement(scoring, 'text').text = self.scoring_method

        ET.SubElement(node, 'shuffleanswers').text = 'true' if self.shuffle else 'false'

        num_rows = len(self.statements)
        num_cols = len(self.options)

        ET.SubElement(node, 'numberofrows').text = str(num_rows)
        ET.SubElement(node, 'numberofcolumns').text = str(num_cols)

        for i, (text, _, feedback) in enumerate(self.statements, start=1):
            row = ET.SubElement(node, 'row')
            row.set('number', str(i))

            opt = ET.SubElement(row, 'optiontext')
            opt.set('format', self.format)
            ET.SubElement(opt, 'text').text = text

            fb = ET.SubElement(row, 'feedbacktext')
            fb.set('format', self.format)
            ET.SubElement(fb, 'text').text = feedback

        for i, opt in enumerate(self.options, start=1):
            col = ET.SubElement(node, 'column')
            col.set('number', str(i))

            resp = ET.SubElement(col, 'responsetext')
            resp.set('format', self.format)
            ET.SubElement(resp, 'text').text = opt

        for i, (_, correct, _) in enumerate(self.statements, start=1):
            for j, opt in enumerate(self.options, start=1):
                weight = ET.SubElement(node, 'weight')
                weight.set('rownumber', str(i))
                weight.set('columnnumber', str(j))

                ET.SubElement(weight, 'value').text = '1.000' if opt == correct else '0.000'

        return node


@dataclass
class Matching(Question):
    """Match drop-down menu items to the correct text.

    :param shuffle: If `True`, items will be shuffled.
    :type shuffle: bool
    """

    shuffle: bool = True
    pairs: typing.List[typing.Tuple[typing.Union[str, None], str]] = field(default_factory=list)

    def add_pair(self, text: typing.Union[str, None], answer: str):
        """Adds a matching pair to the question. If the `text` parameter is `None` a decoy option is added.

        :param text: The first element of the pair, displayed as normal text.
        :type text: str

        :param answer: The corresponding match to the `text` shown as drop-down menu item.
        :type text: str
        """
        self.pairs.append((text, answer))

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('matching')

        for text, answer in self.pairs:
            subquestion = ET.SubElement(node, 'subquestion')
            subquestion.set('format', self.format)

            text = "" if text is None else text

            ET.SubElement(subquestion, 'text').text = text
            aw = ET.SubElement(subquestion, 'answer')
            ET.SubElement(aw, 'text').text = answer

        return node

