import os
import argparse

from jinja2 import Environment, PackageLoader, select_autoescape

from utility.parsers import parse_config, parse_content
from utility.support import check_name_mismatch, prepare_folder, copy_folder


class Generator:
    def __init__(self, **args):

        self.source = args["source"]
        self.target = args["target"]

        self.jinja_env = Environment(
            loader=PackageLoader(self.source), autoescape=select_autoescape()
        )

        self.config_dir = os.path.join(self.source, "configs")
        self.content_dir = os.path.join(self.source, "contents")

        self.config_paths = [
            os.path.join(self.source, "configs", name)
            for name in os.listdir(self.config_dir)
        ]
        self.content_paths = [
            os.path.join(self.source, "contents", name)
            for name in os.listdir(self.content_dir)
        ]

        prepare_folder(self.target)
        copy_folder(
            os.path.join(self.source, "static"), os.path.join(self.target, "static")
        )

        for config_path in self.config_paths:
            self.build_page(config_path)

    def build_page(self, config_path):

        config = parse_config(config_path)

        name = ".".join(config_path.split(".")[:-1]).split("/")[-1]

        page_title = config["page_title"]
        template_name = config["template"]
        css_file_name = config["css_file"]
        content_names = [
            "%s_%s.md" % (name, content_name) for content_name in config["contents"]
        ]

        check_name_mismatch(name, ".".join(template_name.split(".")[:-1]))

        contents = []
        for content_name in content_names:
            contents.append(
                parse_content(os.path.join(self.source, "contents", content_name))
            )

        image_grid = [
            (
                os.path.join("static", "imgs", content["image_name"]),
                content["title"],
                content["title"],
                content["title"],
            )
            for content in contents
        ]

        css_path = os.path.join("static/css", css_file_name)
        template = self.jinja_env.get_template(template_name)
        html = template.render(
            css_file=css_path, page_title=page_title, image_grid=image_grid
        )

        with open(os.path.join(self.target, name + ".html"), "w") as f:
            f.write(html)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="MrGranddy Static Website Generator")

    parser.add_argument(
        "--source",
        default="source",
        dest="source",
        help="Source direction of the project. (default: source)",
    )
    parser.add_argument(
        "--target",
        default="target",
        dest="target",
        help="Target direction of the compiled project. (default: target)",
    )

    args = parser.parse_args()

    g = Generator(source=args.source, target=args.target)
