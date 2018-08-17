from nbconvert.preprocessors import Preprocessor
from nbformat import notebooknode
import warnings


class FrontMatterPreprocessor(Preprocessor):
    """Preprocess the notebook front matter:
    - all the markdown cells before a <!--eofm--> divider
    will be considered as part of the front matter and transformed 
    into a unique cell containing a toml front matter
    - all raw cells or code cells before the <!--eofm--> divider will
    be removed
    - all cells after the <!--eofm--> divider will be kept as is.
    """
    
    def preprocess(self, nb, resources):
        """Execute the preprocessing of the notebook."""
        frontmatter, content_cells = self._split_frontmatter(nb)   
        nb.cells = []
        if frontmatter:
            toml_fm = self._toml_frontmatter(frontmatter)
            nb.cells.append(self._markdown_cell(toml_fm))
        nb.cells += content_cells
        return nb, resources
    
    def _split_frontmatter(self, nb):
        """Return a pair whose first element is a string containing
        the frontmatter and whose second element is a list of all the
        content cells."""
        frontmatter = ''
        for index, cell in enumerate(nb.cells):
            if cell.cell_type == "markdown":
                split = cell.source.split('<!--eofm-->', 1)
                if len(split) > 1: # eofm divider is in the cell
                    fm_part, content_part = split
                    frontmatter += fm_part
                    if content_part.strip():
                        first_content_cell = [self._markdown_cell(content_part)]
                    else: 
                        first_content_cell = []
                    return frontmatter, first_content_cell+nb.cells[index + 1:]
                else:
                    # the entire cell content is part of the front matter
                    frontmatter += cell.source
        warnings.warn('Notebook does not have a front matter.')
        return '', nb.cells
  
    def _toml_frontmatter(self, nb_fm):
        """Convert a notebook front matter into a toml front matter.
        
        Example:
        >>> toml_frontmatter('# Notebook title\nDate: 2018-06-10')
        '+++\ntitle = "Notebook title"\ndate = "2018-06-10"\n+++\n'
        """
        toml_fm = '+++\n'
        for line in nb_fm.split('\n'):
            stripped = line.strip()
            if stripped:
                if stripped.startswith('# '): # The line contains the title
                    toml_fm += 'title = "' + stripped[2:].strip() + '"\n'
                else: # The line is expected to contain a field "key: value0, value1, ..."
                    s = stripped.split(':', 1)
                    if len(s) < 2:
                        warnings.warn(f'This content is not formatted correctly and is ignored: {stripped}')
                        continue
                    key, values = s
                    key = key.lower()
                    values = [value.strip() for value in values.split(',')]
                    if len(values) > 1: # The field has multiple values (e.g. multiple tags)
                        toml_fm += key + ' = [' + ', '.join([f'"{value.strip()}"' for value in values]) + ']\n'
                    else: # The field has a single value (e.g. date)
                        toml_fm += f'{key} = "{values[0]}"\n'
        toml_fm += '+++\n'
        return toml_fm
    
    def _markdown_cell(self, source):
        """Create a markdown cell with source content."""
        return notebooknode.from_dict({"cell_type": "markdown",
                                       "metadata": {},
                                       "source": source})
