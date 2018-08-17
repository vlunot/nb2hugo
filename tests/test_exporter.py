import pytest
from nbformat import notebooknode
from nb2hugo.exporter import HugoExporter


notebook = notebooknode.from_dict({
    'cells': [
        {
            "cell_type": 'raw',
            "metadata": {},
            "source": 'Text in a raw cell, should be ignored.'
        },
        {
            "cell_type": 'markdown',
            "metadata": {},
            "source": (
                'This line should be ignored.\n'
                '# This is the title\n'
                'Date: 2018-06-10\n'
                'This line should be ignored.\n'
                'Tags: Test, Front Matter, Markdown\n'
            )
        },
        {
            "cell_type": 'code',
            "metadata": {},
            "outputs": [],
            "execution_count": 1,
            "source": 'Text in a code cell, should be ignored.'
        },
        {
            "cell_type": 'markdown',
            "metadata": {},
            "source": (
                'This line should be ignored.\n'
                'Categories: Front Matter, Converter\n'
                'This line should be ignored.\n'
                'This text should be ignored.<!--eofm-->This text should be visible.\n'
                'This line should be visible.\n'
            )
        },
        {
            "cell_type": 'markdown',
            "metadata": {},
            "source": (
                'Some text with an inline equality $escaped\_0 = lower_0$.\n' 
                'And a display equality:\n'
                '$$escaped\_1 = subscript_1.$$'
            )
        },
        {
            "cell_type": 'markdown',
            "metadata": {},
            "source": 'Some text with an ![image](https://url.url/image.png).\nAnd more text.'
        },
    ],
    'metadata': {},
    'nbformat': 4,
    'nbformat_minor': 2
})
expected_markdown = (
    '\n'
    '+++\n'
    'title = "This is the title"\n'
    'date = "2018-06-10"\n'
    'tags = ["Test", "Front Matter", "Markdown"]\n'
    'categories = ["Front Matter", "Converter"]\n'
    '+++\n'
    '\n'
    '\n'
    'This text should be visible.\n'
    'This line should be visible.\n'
    '\n'
    '\n'
    'Some text with an inline equality \\\\(escaped\\\\_0 = lower_0\\\\).\n' 
    'And a display equality:\n'
    '\\\\[escaped\\\\_1 = subscript_1.\\\\]'
    '\n'
    '\n'
    'Some text with an ![image](https://url.url/image.png).\n'
    'And more text.'
    '\n'
)

def test_exporter(tmpdir):
    exporter = HugoExporter()
    with pytest.warns(UserWarning, match='should be ignored.$'):
        markdown, resources = exporter.from_notebook_node(notebook)
    assert markdown == expected_markdown
    