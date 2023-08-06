# quizpy

This package allows you to create a Moodle Quiz in Python code, which then can be imported via the XML import.
**Stop fumbling around** with the horrible moodle web interface! **Start coding and use version control!**

So far many of the existing question types are supported:

* Multiple Choice
* Multiple True-False
* Numerical 
* ShortAnswer 
* Matching 
* Drag & Drop on Images
* Cloze
* Essay
* Descriptions

## Installation
Quizpy is available on PyPi and can be installed via pip:
```
pip install quizpy
```

## Usage
A moodle quiz (more specifically a question catalogue) consists of multiple categories that need to be filled
with questions. Each `Question` has at least a title, a question text and some default points (which can be
scaled in the actual quiz on moodle). Further customizations depend on the question type.

A minimal 2-question example might look like this:
```python
from quizpy import Quiz, Category, MultipleChoice, Essay, Choice

mc = MultipleChoice("Question Title", 'Is this a question?', 1.0)
mc.add_choice('Yes', 100.00, 'Correct, horse!')
mc.add_choice('No', -100.00, 'Na-ahh')
mc.add_choice('Maybe?', 0.0, 'Na-ahh')

blabber = Essay("Psychology Question", "How does coding an exam make you feel?", 1.0, 
                response_template="Great!")

example_quiz = Quiz()

example_questions = example_quiz.add_category("Example questions")
example_questions.questions.extend([mc, blabber])


example_quiz.export('example_quiz.xml')

```

## Documentation

A full documentation can be found on [ReadTheDocs](https://quizpy.readthedocs.io/en/latest/index.html).
Please, also have a look in the `examples` folder to quickly see how a question type is used.
