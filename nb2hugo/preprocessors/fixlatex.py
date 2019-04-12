from nbconvert.preprocessors import Preprocessor
import re


class FixLatexPreprocessor(Preprocessor):
    """Preprocess the notebook markdown cells:
    - convert $$ ... $$ to \\[ ... \\],
    - convert $ ... $ to \\( ... \\),
    - double escape underscores inside latex content.
    
    See https://gohugo.io/content-management/formats/#issues-with-markdown
    for some issues with latex.
    """
    
    def preprocess_cell(self, cell, resources, index):
        """Preprocess a notebook cell."""
        if cell.cell_type == "markdown":
            cell.source = self._replace_latex_enclosing_dollars(cell.source)
            cell.source = self._fix_latex_antislash(cell.source)
            cell.source = self._fix_latex_escaped_underscores(cell.source)
        return cell, resources
    
    def _replace_latex_enclosing_dollars(self, text):
        """Convert LaTeX $ ... $ or $$ ... $$ expressions to respectively 
        \\( ... \\) and \\[ ... \\].
        """
        single_dollar_latex = r'(?<![\\\$])\$(?!\$)(.+?)(?<![\\\$])\$(?!\$)'
        to_parentheses = lambda m: r'\\(' + m.group(1) + r'\\)'
        no_single_dollar = re.sub(single_dollar_latex, to_parentheses, text,
                                  flags=re.S)
        double_dollar_latex = r'\$\$(.+?)\$\$'
        to_brackets = lambda m: r'\\[' + m.group(1) + r'\\]'
        no_single_or_double_dollar = re.sub(double_dollar_latex, to_brackets, 
                                            no_single_dollar, flags=re.S)
        return no_single_or_double_dollar
    
    def _fix_latex_escaped_underscores(self, text):
        """Replace '_' by '\_' inside LaTeX expressions delimited by
        \\[ ... \\] or \\( ... \\)."""
        inline_math = r'\\\((.+?)\\\)'
        display_math = r'\\\[(.+?)\\\]'
        double_escape = lambda m: re.sub(r'(?<!\\)_', r'\\_', m.group(0))
        new_text = re.sub(inline_math, double_escape, text, flags=re.S)
        new_text = re.sub(display_math, double_escape, new_text, flags=re.S)
        return new_text
    
    def _fix_latex_antislash(self, text):
        """Replace '\\' by '\\\\\\' and '\' by '\\' inside LaTeX expressions 
        delimited by \\[ ... \\] or \\( ... \\)."""
        inline_math = r'\\\\\((.+?)\\\\\)'
        display_math = r'\\\\\[(.+?)\\\\\]'
        multiple_escape = lambda m: r'\\(' + re.sub(r'\\\\', r'\\\\\\\\\\', m.group(1)) + r'\\)'
        new_text = re.sub(inline_math, multiple_escape, text, flags=re.S)
        multiple_escape = lambda m: r'\\[' + re.sub(r'\\\\', r'\\\\\\\\\\', m.group(1)) + r'\\]'
        new_text = re.sub(display_math, multiple_escape, new_text, flags=re.S)
        double_escape = lambda m: r'\\(' + re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', m.group(1)) + r'\\)'
        new_text = re.sub(inline_math, double_escape, new_text, flags=re.S)
        double_escape = lambda m: r'\\[' + re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', m.group(1)) + r'\\]'
        new_text = re.sub(display_math, double_escape, new_text, flags=re.S)
        return new_text
