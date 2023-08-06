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
import enum

from dataclasses import dataclass, field

from .common import Question
from .multipe_choice import Choice


class UnitGradingType(enum.Enum):
    NO_PENALTY = 0
    FRAC_RESPONSE_GRADE = 1
    FRAC_TOTAL_GRADE = 2


class UnitBehaviour(enum.Enum):
    Optional = 0
    Force = 1
    NoUnits = 3


@dataclass
class NumericalAnswer(Choice):
    """A Choice sub-class with added tolerance for Numerical questions.

    :param tolerance: The absolute tolerance that a students answer is allowed to deviate from the correct value.
        .. note:: In case you use units the tolerance is assumed to be in the base unit and is converted accordingly.
    """

    tolerance: float = 0.0

    def to_xml(self) -> ET.Element:
        answer = super().to_xml()
        ET.SubElement(answer, 'tolerance').text = str(self.tolerance)
        return answer

    def to_cloze(self) -> str:
        """Converts answer into cloze representation. Do not use directly. This used by ``Numerical.to_cloze()``."""
        if self.fraction == 100.0:
            s = f"={self.text}:{self.tolerance}#{self.feedback}"
        elif self.fraction == 0.0:
            s = f"{self.text}:{self.tolerance}#{self.feedback}"
        else:
            s = f"%{int(self.fraction)}%{self.text}:{self.tolerance}#{self.feedback}"
        return s


@dataclass
class Numerical(Question):
    """A question with a one-line answering option that should be a number with optional units.

    :param units_left: If ``True``, Moodle will try to parse the unit on the left side of the number e.g. $1.
    :type units_left: bool

    :param unit_grading_type: Determines the grading for using possibly the wrong unit:

        UnitGradingType.NO_PENALTY
            No penalty is applied for not using the base unit / no unit at all.

            .. caution:: This does not imply ``unit_behaviour = UnitBehaviour.Optional``.
                         If ``unit_behaviour = UnitBehaviour.Force`` Moodle just ignores
                         this setting on import and assumes a penalty.

        UnitGradingType.FRAC_RESPONSE_GRADE
            A fraction of the grade given for this particular answer is
            deducted from the total grade. Implies ``unit_behaviour = UnitBehaviour.Force``

        UnitGradingType.FRAC_TOTAL_GRADE
            A fraction of the total grade is deducted. Implies ``unit_behaviour = UnitBehaviour.Force``

        .. note:: The penalty is applied when

            1. Using a unit that has a multiplier other than 1.
            2. Using a unit that was not defined
            3. Not using a unit at all

    :type unit_grading_type: UnitGradingType

    :param unit_behaviour: Determines if and how units are used in the question:

        UnitBehaviour.Optional
            Units can be used but if no unit is provided the base unit is assumed

        UnitBehaviour.Force
            Units must be provided.

        UnitBehaviour.NoUnits
            No units are used in the question

    :type unit_grading_type: UnitBehaviour

    :param unit_penalty: The fractional penalty between 0 and 1.
        This is only used if ``unit_behaviour = UnitBehaviour.Force``

    :type unit_penalty: float
    """
    accepted_answers: typing.List[NumericalAnswer] = field(default_factory=list)
    units: typing.List[typing.Tuple[str, float]] = field(default_factory=list)
    units_left: bool = False
    unit_grading_type: UnitGradingType = UnitGradingType.NO_PENALTY
    unit_behaviour: UnitBehaviour = UnitBehaviour.NoUnits
    unit_penalty: float = 0.1

    # TODO: Eingabeformat wird im XML komplett vergessen

    def to_xml(self) -> ET.Element:
        node = self.generate_common_xml('numerical')

        for answer in self.accepted_answers:
            node.append(answer.to_xml())

        units = ET.SubElement(node, 'units')
        for unit, multiplier in self.units:
            u = ET.SubElement(units, 'unit')
            ET.SubElement(u, 'multiplier').text = str(multiplier)
            ET.SubElement(u, 'unit_name').text = unit

        ET.SubElement(node, 'unitgradingtype').text = str(self.unit_grading_type.value)
        ET.SubElement(node, 'unitsleft').text = '1' if self.units_left else '0'
        ET.SubElement(node, 'showunits').text = str(self.unit_behaviour.value)
        ET.SubElement(node, 'unitpenalty').text = str(self.unit_penalty)

        return node

    def to_cloze(self, weight: int):
        """Turns this question into its Cloze syntax representation to be used in a Cloze question text."""
        cloze = f'{weight}:NM:'
        cloze += '~'.join(map(lambda a: a.to_cloze(), self.accepted_answers))

        return f'{{{cloze}}}'

    def add_unit(self, unit: str, conversion_factor: float):
        """Convenience method to add a unit.

        :param unit: A string representing the unit.
            .. note:: Due to this bug <https://tracker.moodle.org/browse/MDL-69597> we strip the whitespaces before
            adding it to the list.

        :type unit: str

        :param conversion_factor: The factor that is applied before comparing it with the correct answer.

            .. note:: If you use units you should always add at least one option with ``conversion factor = 1.0`` so
                      that your unit will be accepted as the correct unit.
        """

        self.units.append((unit.strip(), conversion_factor))

    def add_answer(self, number: float, fraction: float, feedback: str = '', format: str = 'html', tolerance: float = 0.0) -> NumericalAnswer:
        """Convenience method to add a ``NumericalAnswer``
        :param number: The correct number (assume the base unit in case that units are used).
        :type number: float

        :param fraction: The fraction of the total points to be given for this answer as percentage between 0 and 100.
        :type fraction: float

        :param feedback: Specific feedback for choosing this answer option
        :type feedback: str

        :param format: format for rendering both answer text and feedback.
            Can either be `html` (default), `markdown`, `plain_text` or `moodle_auto_format`.
        """

        n = NumericalAnswer(f"{number}", fraction, feedback=feedback, format=format, tolerance=tolerance)
        self.accepted_answers.append(n)
        return n

