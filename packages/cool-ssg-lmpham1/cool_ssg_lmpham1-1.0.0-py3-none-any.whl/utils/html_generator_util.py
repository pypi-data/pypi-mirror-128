import shutil
import re
from pathlib import Path

# To add new supported file type, simply add to this list
ACCEPTED_FILES = [".txt", ".md"]


# Generate HTML file from filepath, and export to output folder
def generate_from_file(filepath, output, options, input_dir=None):
    # extract file name without extension
    filename = Path(filepath).stem

    if Path(filepath).suffix in ACCEPTED_FILES:
        with open(filepath, encoding="utf8") as (file):
            contents = "".join(file.readlines())
            output_filepath = Path(output).joinpath(filename + ".html")

            out_content = create_html_string(
                filename, contents, output_filepath, options, input_dir
            )

            if Path(filepath).name.endswith(".md"):
                out_content = process_markdown(out_content)

            output.mkdir(parents=True, exist_ok=True)

            output_file = open(output_filepath, "w", encoding="utf-8")
            output_file.write(out_content)
            output_file.close()
            print('"' + filename + '.html" generated successfully!')
            return output_filepath
    return None


# Generate HTML files with the same structure as the input folder,
# and export to output folder
def generate_from_directory(input_dir, output, options):
    index_links = []
    for filepath in Path(input_dir).rglob("*.*"):
        output_path = Path(output).joinpath(
            Path(filepath).parents[0].relative_to(input_dir)
        )
        generated_filepath = generate_from_file(
            filepath, output_path, options, input_dir
        )
        if generated_filepath:
            index_links.append(
                '<a class="list-item" href="{file}"><li class="link">{title}</li></a>'.format(  # noqa: E501
                    file=generated_filepath.relative_to(output),
                    title=generated_filepath.relative_to(output).stem,
                )
            )

    index_skeleton = """<!doctype html>
<html lang="{lang}">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        {stylesheets}
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h1>{title}</h1>
        <ul class=\"link-container\">
            {contents}
        </ul>
    </body>
</html>"""

    style_html = ""
    if options["stylesheets"] is not None:
        for stylesheet in options["stylesheets"]:
            style_html += '<link rel="stylesheet" href="{}">\n'.format(
                stylesheet
            )

    index_title = Path(input_dir).name

    index_html_content = index_skeleton.format(
        stylesheets=style_html,
        contents="\n".join(index_links),
        title=index_title
        if index_title != "" and index_title is not None
        else "Index Page",
        lang=options["lang"],
    )

    output_file = open(
        Path(output).joinpath("index.html"), "w", encoding="utf-8"
    )
    output_file.write(index_html_content)
    output_file.close()


# Create HTML from markdown file
def process_markdown(html_content):
    # Parse bold markdown
    html_content = re.sub(
        r"\*\*([^\s\*.]{1}.*?)\*\*|__([^\s_.]{1}.*?)__",
        r"<strong>\1\2</strong>",
        html_content,
    )
    # Parse italic markdown
    html_content = re.sub(
        r"\*([^\s\*.]{1}.*?)\*|_([^\s\_.]{1}.*?)_",
        r"<em>\1\2</em>",
        html_content,
    )
    # Parse link markdown
    html_content = re.sub(
        r"\[(.+)\]\((.+\..+)\)", r'<a href="\2">\1</a>', html_content
    )
    # Parse horizontal rule
    html_content = re.sub(
        r"(\n|(\n<p>))\s{0,3}((---)|(\*\*\*))\s{0,3}((</p>\n)|\n)",
        r"\n<hr/>\n",
        html_content,
    )

    return html_content


# Create HTML mark up and append the content
# return the complete HTML mark up for a page
def create_html_string(filename, contents, output, options, input_dir=None):
    title = filename

    if contents.split("\n\n\n", 1)[0] == contents.splitlines()[0]:
        title = contents.split("\n\n\n", 1)[0]
        contents = contents.split("\n\n\n", 1)[1]

    contents = "<p>" + contents + "</p>"
    contents = contents.replace("\n\n", "</p>\n\n<p>")

    html_skeleton = """<!doctype html>
<html lang="{lang}">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        {stylesheets}
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <div class=\"main-container\">
            {sidebar}
            <div class=\"content-container\">
                <h1>{title}</h1>

                {contents}
            </div>
        </div>
    </body>
</html>"""

    style_html = ""
    if options["stylesheets"] is not None:
        for stylesheet in options["stylesheets"]:
            if isinstance(stylesheet, Path):
                for part in range(0, len(output.parts) - 2):
                    stylesheet = Path("..").joinpath(stylesheet)
            style_html += '<link rel="stylesheet" href="{}">\n'.format(
                stylesheet
            )

    sidebar = generate_sidebar(input_dir, output, options["sidebar"])

    return html_skeleton.format(
        title=title,
        contents=contents,
        stylesheets=style_html,
        lang=options["lang"],
        sidebar=sidebar if sidebar else "",
    )


# emptying old output folder
def empty_folder(dir):
    shutil.rmtree(dir)
    Path(dir).mkdir()


# generate stylesheet files in <OUTPUT>/public/stylesheet/
def generate_stylesheets(stylesheets, output):
    stylesheet_paths = []

    # default stylesheet
    default_stylesheet = "public/stylesheet/default.css"
    stylesheet_folder = Path(output).joinpath("public", "stylesheet")
    Path(stylesheet_folder).mkdir(parents=True, exist_ok=True)

    if stylesheets:
        for stylesheet in stylesheets:
            if stylesheet.startswith("https://") or stylesheet.startswith(
                "http://"
            ):
                stylesheet_paths.append(stylesheet)
            elif Path(stylesheet).is_file() and Path(stylesheet).exists():
                shutil.copy(stylesheet, stylesheet_folder)
                stylesheet_paths.append(
                    stylesheet_folder.joinpath(
                        Path(stylesheet).name
                    ).relative_to(output)
                )
            else:
                print("ERROR: Cannot find stylesheet: {}".format(stylesheet))
    else:
        shutil.copy(default_stylesheet, stylesheet_folder)
        stylesheet_paths.append(
            stylesheet_folder.joinpath(
                Path(default_stylesheet).name
            ).relative_to(output)
        )

    return stylesheet_paths


def recurse_sidebar_map(sidebar_dir, output, input_dir):
    links = []
    for item in Path(sidebar_dir).glob("*"):
        itempath = Path(item)
        if itempath.is_dir():
            subfolder_links = recurse_sidebar_map(item, output, input_dir)
            if subfolder_links:
                links.append(
                    "<li>\n" + itempath.name + "\n" + subfolder_links + "</li>"
                )
        elif Path(item).is_file() and Path(item).suffix in ACCEPTED_FILES:
            itempath = itempath.with_suffix(".html").relative_to(
                Path(input_dir)
            )
            for part in range(0, len(output.parts) - 2):
                itempath = Path("..").joinpath(itempath)
            links.append(
                '<li><a href="{link}">{title}</a></li>'.format(
                    link=itempath, title=itempath.stem
                )
            )
    if len(links) > 0:
        return "<ul>\n{contents}\n</ul>\n".format(contents="\n".join(links))
    else:
        return None


def generate_sidebar(input_dir, output, sidebar_options):
    if not sidebar_options:
        return None

    sidebar_html = '<div class="sidebar-container">\n{}\n</div>\n'
    sidebar_links = None

    if sidebar_options == -1:
        sidebar_links = recurse_sidebar_map(input_dir, output, input_dir)

    elif isinstance(sidebar_options, dict):
        links = []
        if sidebar_options["type"] == "pages":
            for item in sidebar_options["items"]:
                input_itempath = Path(input_dir).joinpath(item)
                if input_itempath.exists():
                    if input_itempath.is_dir():
                        links.append(
                            recurse_sidebar_map(
                                input_itempath, output, input_dir
                            )
                        )
                    else:
                        itempath = Path(item).with_suffix(".html")
                        for part in range(0, len(output.parts) - 2):
                            itempath = Path("..").joinpath(itempath)
                        links.append(
                            '<li><a href="{link}">{title}</a></li>'.format(
                                link=itempath, title=itempath.stem
                            )
                        )
        sidebar_title = (
            "<h2>{}</h2>".format(sidebar_options["title"])
            if sidebar_options["title"]
            else None
        )
        sidebar_links = (
            "<ul>\n" + sidebar_title + "\n".join(links) + "\n</ul>\n"
        )

    return sidebar_html.format(sidebar_links)
