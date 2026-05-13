import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(file_path, pages_per_file):
    # 打开原始PDF文件
    with open(file_path, 'rb') as infile:
        reader = PdfReader(infile)
        total_pages = len(reader.pages)

        # 创建与原文件同名的新文件夹
        file_dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)
        new_folder_path = os.path.join(file_dir, file_base)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # 分割PDF
        for start_page in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            end_page = min(start_page + pages_per_file, total_pages)

            for page in range(start_page, end_page):
                writer.add_page(reader.pages[page])

            output_filename = os.path.join(new_folder_path, f"{file_base}_{start_page // pages_per_file + 1}{file_ext}")

            with open(output_filename, 'wb') as outfile:
                writer.write(outfile)