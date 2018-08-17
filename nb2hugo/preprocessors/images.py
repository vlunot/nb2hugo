from nbconvert.preprocessors import Preprocessor
import re
import os
import urllib.request


class ImagesPreprocessor(Preprocessor):
    """Preprocess the notebook markdown cells:
    - copy images to static directory,
    - update image link.
    """

    def preprocess(self, nb, resources):
        """Preprocess the entire notebook."""
        if not 'images_path' in resources:
            resources['images_path'] = {}    
        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources
    
    def preprocess_cell(self, cell, resources, index):
        """Preprocess one cell."""
        if cell.cell_type == "markdown":
            # Find and process links:
            process_match = lambda m: self._process_image_link(m.group(1), m.group(2), resources)
            cell.source = re.sub('!\[([^"]*?)\]\(([^"]+?)\)', process_match, cell.source)
        return cell, resources
    
    def _process_image_link(self, alt_text, url, resources):
        """Copy image and return updated link."""
        url_as_path = os.path.join(resources['metadata']['path'], url)
        if os.path.isfile(url_as_path):
            filename = os.path.basename(url)
            resources['images_path'][filename] = url_as_path
            link = '![' + alt_text + '](' + filename + ')'
        else:
            link = '![' + alt_text + '](' + url + ')'
        return link
