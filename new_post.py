#!/usr/bin/env python3
#
import os
import re
import sys
from datetime import date


def fix_up_title(pathname, title):
    with open(pathname, "r") as file:
        content = file.readlines()
    # find and update the title
    for i, line in enumerate(content):
        if re.match(r"^title:", line):
            content[i] = f'title: "{title}"\n'
            break
    # write back file
    with open(pathname, "w") as file:
        file.writelines(content)


def main():
    title = " ".join(sys.argv[1:])
    today = date.today()
    filename = (
        "_".join([today.isoformat(), re.sub("[^a-z_]+", "_", title.lower())]) + ".md"
    )
    slug = "/".join(["posts", str(today.year), filename])
    os.system("hugo new " + slug)
    pathname = os.path.join("content", "posts", str(today.year), filename)
    fix_up_title(pathname, title)


if __name__ == "__main__":
    main()

# end
