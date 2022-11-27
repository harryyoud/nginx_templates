from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import os
import os.path

os.makedirs("sites-available", exist_ok=True)
os.makedirs("sites-enabled", exist_ok=True)
[f.unlink() for f in Path("sites-available").glob("*") if f.is_file()]
[f.unlink() for f in Path("sites-enabled").glob("*") if f.is_file() or f.is_symlink()]

environment = Environment(loader=FileSystemLoader("templates/"))
templates = environment.list_templates(None, lambda x: x.endswith(".conf.jinja2") and
                                       not os.path.basename(x).startswith("_"))

print(f"Found {len(templates)} templates to render")

for name in templates:
    template = environment.get_template(name)
    out_name = name.replace('.jinja2', '')

    with open(f'sites-available/{out_name}', 'w') as f:
        f.write(template.render())
        os.symlink(f"../sites-available/{out_name}", f"sites-enabled/{out_name}")
        print(f" => Processed {out_name}")

print("All done!")