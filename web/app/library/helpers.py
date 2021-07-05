# 마크다운파일을 가져와서 app/pages html로 변환하고 반환한다. 

import os.path
import markdown

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data