import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor
import mtk2
doc = docx.Document("variants/variant10.docx")
tex_1, tex_2, tex_3, tex_4, tex_5 = "", "", "", "", ""

for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        print(run._r.get_or_add_rPr())
        print(run._r.get_or_add_rPr().xpath("./w:spacing"))
        print(type(run._r.get_or_add_rPr().xpath("./w:spacing")))
        # Р Ш
        if run.font.size.pt == 11.5:
            tex_1 += "1" * len(run.text)
        else:
            tex_1 += "0" * len(run.text)

        # Ц С
        if run.font.color.rgb != RGBColor(0,0,0):
            tex_2 += "1" * len(run.text)
        else:
            tex_2 += "0" * len(run.text)

        # ЦВЕТ ФОНА
        if run.font.highlight_color != WD_COLOR_INDEX.WHITE:
            tex_3 += "1" * len(run.text)
        else:
            tex_3 += "0" * len(run.text)

        # МЕЖСИМВОЛЬНЫЙ ИНТЕРВАЛ
        if run._r.get_or_add_rPr().xpath("./w:spacing"):
            tex_4 += "1" * len(run.text)
        else:
            tex_4 += "0" * len(run.text)

        # МАСШТАБ ШРИФТА
        if run._r.get_or_add_rPr().xpath("./w:w"):
            tex_5 += "1" * len(run.text)
        else:
            tex_5 += "0" * len(run.text)

def dlina(tex):
    while len(tex) % 8 != 0:
        tex += "0"
    return tex
tex_1 = dlina(tex_1)
tex_2 = dlina(tex_2)
tex_3 = dlina(tex_3)
tex_4 = dlina(tex_4)
tex_5 = dlina(tex_5)


def encode(code):
    print("cp1251 - ", bytes.fromhex(hex(int(code, 2))[2:]).decode(encoding="cp1251"))
    print("koi8_r - ", bytes.fromhex(hex(int(code, 2))[2:]).decode(encoding="koi8_r"))
    print("cp866 - ", bytes.fromhex(hex(int(code, 2))[2:]).decode(encoding="cp866"))
    print("mtk2 - ", mtk2.MTK2_decode(code))

if tex_1 != "0" * len(tex_1):
    print("РАЗМЕР ШРИФТА")
    encode(tex_1)

if tex_2 != "0" * len(tex_2):
    print("ЦВЕТ СИМВОЛОВ")
    encode(tex_2)

if tex_3 != "0" * len(tex_3):
    print("ЦВЕТ ФОНА")
    encode(tex_3)

if tex_4 != "0" * len(tex_4):
    print("МЕЖСИМВОЛЬНЫЙ ИНТЕРВАЛ")
    encode(tex_4)

if tex_5 != "0" * len(tex_5):
    print("МАСШТАБ ШРИФТА")
    encode(tex_5)
