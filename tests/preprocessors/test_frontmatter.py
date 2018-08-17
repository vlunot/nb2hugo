import pytest
from nbformat import notebooknode
from nb2hugo.preprocessors import FrontMatterPreprocessor


@pytest.fixture
def preprocessor():
    """Return an instance of FrontMatterPreprocessor."""
    return FrontMatterPreprocessor()


def test_toml_frontmatter(preprocessor):
    result = preprocessor._toml_frontmatter('# Notebook title\nDate: 2018-06-10')
    assert result == '+++\ntitle = "Notebook title"\ndate = "2018-06-10"\n+++\n'

    
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
        }
    ],
    'metadata': {},
    'nbformat': 4,
    'nbformat_minor': 2
})
expected_notebook = notebook.copy()
expected_notebook.cells = [
    {
        "cell_type": 'markdown',
        "metadata": {},
        "source": (
            '+++\n'
            'title = "This is the title"\n'
            'date = "2018-06-10"\n'
            'tags = ["Test", "Front Matter", "Markdown"]\n'
            'categories = ["Front Matter", "Converter"]\n'
            '+++\n'
        )
    },
    {
        "cell_type": 'markdown',
        "metadata": {},
        "source": (
            'This text should be visible.\n'
            'This line should be visible.\n'
        )
    }
]

def test_preprocess(preprocessor):
    with pytest.warns(UserWarning, match='should be ignored.$'):
        result = preprocessor.preprocess(notebook, None)
    assert  result == (expected_notebook, None)
