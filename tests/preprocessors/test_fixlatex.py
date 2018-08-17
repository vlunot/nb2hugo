import pytest
from nbformat import notebooknode
from nb2hugo.preprocessors import FixLatexPreprocessor


@pytest.fixture
def preprocessor():
    """Return an instance of FixLatexPreprocessor."""
    return FixLatexPreprocessor()

source = (
    'Some text with an inline equality $escaped\_0 = lower_0$.\n' 
    'And a display equality:\n'
    '$$escaped\_1 = subscript_1.$$\n'
    'And a second one on multiple lines:\n'
    '$$\n'
    'escaped\_2\n'
    '$$\n'
)
dollars_processed = (
    'Some text with an inline equality \\\\(escaped\_0 = lower_0\\\\).\n' 
    'And a display equality:\n'
    '\\\\[escaped\_1 = subscript_1.\\\\]\n'
    'And a second one on multiple lines:\n'
    '\\\\[\n'
    'escaped\_2\n'
    '\\\\]\n'
)
fully_processed = (
    'Some text with an inline equality \\\\(escaped\\\\_0 = lower_0\\\\).\n' 
    'And a display equality:\n'
    '\\\\[escaped\\\\_1 = subscript_1.\\\\]\n'
    'And a second one on multiple lines:\n'
    '\\\\[\n'
    'escaped\\\\_2\n'
    '\\\\]\n'
)


def test_replace_latex_enclosing_dollars(preprocessor):
    result = preprocessor._replace_latex_enclosing_dollars(source)
    assert result == dollars_processed
  

def test_fix_latex_escaped_underscores(preprocessor):
    result = preprocessor._fix_latex_escaped_underscores(dollars_processed)
    assert result == fully_processed


raw_cell, code_cell, markdown_cell, expected_markdown_cell = [
    notebooknode.from_dict({"cell_type": cell_type,
                            "metadata": {},
                            "source": source})
    for cell_type, source in [('raw', source), 
                              ('code', source),
                              ('markdown', source),
                              ('markdown', fully_processed)]
]

@pytest.mark.parametrize("input_cell, expected_cell", [
    (raw_cell, raw_cell),
    (code_cell, code_cell),
    (markdown_cell, expected_markdown_cell),
])
def test_preprocess_cell(preprocessor, input_cell, expected_cell):
    assert preprocessor.preprocess_cell(input_cell, None, None) == (expected_cell, None)
