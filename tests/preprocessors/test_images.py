import pytest
from nbformat import notebooknode
from nb2hugo.preprocessors import ImagesPreprocessor


@pytest.fixture
def preprocessor():
    return ImagesPreprocessor()

@pytest.fixture
def resources(tmpdir):
    nb_dir = tmpdir.mkdir('nb_dir')
    img_dir = nb_dir.mkdir('img_dir')
    img_dir.join('fake.png').write('not really an image')
    resources = {
        'metadata': {
            'name': 'notebook',
            'path': nb_dir,
        },
    }
    return resources


def test_process_image_link(preprocessor, resources):
    resources['images_path'] = {}
    link = preprocessor._process_image_link('Some alt text', 'img_dir/fake.png', resources)
    assert link == '![Some alt text](fake.png)'
    assert 'fake.png' in resources['images_path']
    

source = 'Some text with an ![image](img_dir/fake.png).\nAnd more text.'
processed_source = 'Some text with an ![image](fake.png).\nAnd more text.'
raw_cell, code_cell, markdown_cell, expected_markdown_cell = [
    notebooknode.from_dict({"cell_type": cell_type,
                            "metadata": {},
                            "source": source})
    for cell_type, source in [('raw', source), 
                              ('code', source),
                              ('markdown', source),
                              ('markdown', processed_source)]
]

@pytest.mark.parametrize("input_cell, expected_cell, fake_in_images_path", [
    (raw_cell, raw_cell, False),
    (code_cell, code_cell, False),
    (markdown_cell, expected_markdown_cell, True),
])
def test_preprocess_cell(preprocessor, resources, input_cell, 
                         expected_cell, fake_in_images_path):
    resources['images_path'] = {} 
    result = preprocessor.preprocess_cell(input_cell.copy(), resources.copy(), None)
    assert result[0] == expected_cell
    assert ('fake.png' in resources['images_path']) == fake_in_images_path
