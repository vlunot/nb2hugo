import pytest
from nbformat import notebooknode
from nb2hugo.preprocessors import WrapHtmlPreprocessor
from copy import deepcopy


@pytest.fixture
def preprocessor():
    return WrapHtmlPreprocessor()


cell_without_outputs = notebooknode.from_dict({})
cell_with_empty_outputs = notebooknode.from_dict({"outputs": []})
cell_without_data_in_outputs = notebooknode.from_dict({"outputs": [{"name": "stdout"}]})
cell_without_html_in_outputs = notebooknode.from_dict(
    {"outputs": [{"data": {"text/plain": "text"}}]}
)
cell_with_text_html_in_outputs = notebooknode.from_dict(
    {"outputs": [{"data": {"text/html": "html"}}]}
)
transformed_cell_with_text_html_in_outputs = notebooknode.from_dict(
    {"outputs": [{"data": {"text/html": "{{< rawhtml >}}\nhtml\n{{< /rawhtml >}}"}}]}
)


@pytest.mark.parametrize(
    "input_cell, expected_cell",
    [
        (cell_without_outputs, cell_without_outputs),
        (cell_with_empty_outputs, cell_with_empty_outputs),
        (cell_without_data_in_outputs, cell_without_data_in_outputs),
        (cell_without_html_in_outputs, cell_without_html_in_outputs),
        (cell_with_text_html_in_outputs, transformed_cell_with_text_html_in_outputs),
    ],
)
def test_preprocess_cell(preprocessor, input_cell, expected_cell):
    result = preprocessor.preprocess_cell(deepcopy(input_cell), None, None)
    assert result[0] == expected_cell
