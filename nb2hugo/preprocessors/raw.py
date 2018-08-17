from nbconvert.preprocessors import Preprocessor

class RawPreprocessor(Preprocessor):
    """Preprocess the notebook raw cells and convert them into plain text."""
    
    def preprocess_cell(self, cell, resources, index):
        """Preprocess a notebook cell."""
        if cell.cell_type == "raw":
            cell.source = '```\n' + cell.source + '\n```'
        return cell, resources