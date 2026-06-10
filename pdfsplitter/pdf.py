import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def split_pdf_page(input_pdf_path, output_pdf_path):
    """
    将 PDF 的每一页切割成四个子页（横竖各一刀）。
    
    参数：
    - input_pdf_path: 输入 PDF 文件路径
    - output_pdf_path: 输出 PDF 文件路径
    """
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"输入文件不存在: {input_pdf_path}")

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        # 获取原页面尺寸
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        half_width = page_width / 2
        half_height = page_height / 2

        # 定义四个子区域的裁剪框（左下角x, y, 右上角x, y）
        # 将页面横向和竖向各切一刀，得到四个子区域：
        # 区域1：左下 (0, 0) 到 (half_width, half_height)        —— 左下
        # 区域2：左下 (half_width, 0) 到 (page_width, half_height) —— 右下
        # 区域3：左下 (0, half_height) 到 (half_width, page_height) —— 左上
        # 区域4：左下 (half_width, half_height) 到 (page_width, page_height) —— 右上
        regions = [
            (0, 0, half_width, half_height),
            (half_width, 0, page_width, half_height),
            (0, half_height, half_width, page_height),
            (half_width, half_height, page_width, page_height)
        ]

        for region in regions:
            # 创建一个新的空白页面，尺寸与原页面相同（或可改为子区域尺寸，这里保持原尺寸）
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=(page_width, page_height))
            c.save()
            packet.seek(0)
            new_page = PdfReader(packet).pages[0]

            # 将原页面的内容裁剪并放置到新页面
            # 使用 PyPDF2 的 add_transformation 进行裁剪
            # 注意：PyPDF2 的裁剪使用 /CropBox，这里通过修改页面对象实现
            # 方法：直接设置新页面的 /CropBox 和 /MediaBox
            from PyPDF2.generic import RectangleObject
            new_page.mediabox = RectangleObject(region)
            new_page.cropbox = RectangleObject(region)
            
            # 将原页面的内容合并到新页面（在原坐标空间下，但新页面已裁剪，会自动适配）
            # 实际上更好的方式：将原页面内容缩放平移至子区域
            # 这里采用另一种简单方法：把原页面作为模板，通过创建新页面并合并原页面的部分来实现
            # 由于直接复制复杂，我们使用更直接的方式：将原页面裁剪后复制内容
            # 但 PyPDF2 不支持直接裁剪合并，建议用 pdfplumber/PyMuPDF 更简便。
            # 作为替代，这里使用 PDF 页面对象合并的简单方法：
            # 将原页面的 /Contents 复制过来，并调整变换矩阵
            # 为了简化，我们使用另一种实现：基于 PyMuPDF(fitz) 替代
            pass  # 本方法暂不完整，见下方完整实现

    # 由于上述方式复杂，推荐使用 PyMuPDF 库实现，下面是完整可用版本
    print("请使用下方完整的 PyMuPDF 版本。")

# 更优的方案：使用 PyMuPDF (fitz)
def split_pdf_pymupdf(input_pdf_path, output_pdf_path):
    """
    使用 PyMuPDF 将 PDF 每页切成四页。
    """
    import fitz  # PyMuPDF

    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()  # 新建空白 PDF

    for page_num in range(doc.page_count):
        page = doc[page_num]
        rect = page.rect  # 原始页面尺寸
        half_width = rect.width / 2
        half_height = rect.height / 2

        # 定义四个裁剪区域
        regions = [
            fitz.Rect(0, 0, half_width, half_height),          # 左下
            fitz.Rect(half_width, 0, rect.width, half_height),  # 右下
            fitz.Rect(0, half_height, half_width, rect.height), # 左上
            fitz.Rect(half_width, half_height, rect.width, rect.height) # 右上
        ]

        for region in regions:
            # 在新建文档中添加一页，尺寸与子区域一致
            new_page = new_doc.new_page(width=region.width, height=region.height)
            # 将原页面的内容裁剪并显示到新页面
            # 使用 show_pdf_page 并指定 clip 参数来截取区域
            new_page.show_pdf_page(
                new_page.rect,   # 显示在新页面的整个区域
                doc,             # 源文档
                page_num,        # 源页码
                clip=region      # 截取的区域
            )

    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()
    print(f"切割完成，输出文件: {output_pdf_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input")
    out_path = os.path.join(script_dir, "out")

    if not os.path.isdir(input_path):
        raise FileNotFoundError(f"输入目录不存在: {input_path}")

    os.makedirs(out_path, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(input_path):
        for file in filenames:
            if not file.lower().endswith(".pdf"):
                continue
            input_file = os.path.join(dirpath, file)
            rel_path = os.path.relpath(input_file, input_path)
            output_file = os.path.join(out_path, rel_path)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            # print(input_file)
            split_pdf_pymupdf(input_file, output_file)