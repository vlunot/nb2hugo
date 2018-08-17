import os
import shutil
from .exporter import HugoExporter


class HugoWriter:
    """A configurable writer to create Hugo markdown from a Jupyter notebook."""
    
    def __init__(self, config=None):
        self._exporter = HugoExporter(config)
        
    def convert(self, notebook, site_dir, section):
        """Convert a Jupyter notebook into a Hugo markdown and write 
        the result in the content section of the site located in site_dir.
        """
        (markdown, resources) = self._exporter.from_filename(notebook)
        self._write_resources_images(resources, site_dir, section)
        self._write_markdown(markdown, resources, site_dir, section)
        
    def _write_resources_images(self, resources, site_dir, section):
        """Process resources to create output images in static directory."""
        name = resources['metadata']['name']
        target_dir = os.path.join(site_dir, 'static', section, name)
        if 'outputs' in resources:
            if resources['outputs']:
                os.makedirs(target_dir, exist_ok=True)
            for key, value in resources['outputs'].items():
                target = os.path.join(target_dir, key)     
                with open(target, 'wb') as f:
                    f.write(value)
                    shortname = '/'.join(target.split('/')[-3:])
                    print(f"Created '{shortname}'")
        if 'images_path' in resources:
            if resources['images_path']:
                os.makedirs(target_dir, exist_ok=True)
            for key, value in resources['images_path'].items():
                target = os.path.join(target_dir, key)     
                shutil.copy2(value, target)
                shortname = '/'.join(target.split('/')[-3:])
                print(f"Created '{shortname}'")

    def _write_markdown(self, markdown, resources, site_dir, section):
        """Save markdown to file."""
        name = resources['metadata']['name']
        target_dir = os.path.join(site_dir, 'content', section)
        os.makedirs(target_dir, exist_ok=True)
        target = os.path.join(target_dir, f'{name}.md')
        with open(target, 'w') as f:
            f.write(markdown)
            shortname = '/'.join(target.split('/')[-2:])
            print(f"Created '{shortname}'")
