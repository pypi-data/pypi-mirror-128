import logging
import shutil
from typing import List, Optional

import os
import tempfile
import re
import pypdftk
import pytesseract
from wand.image import Image

from .dto import ManuscriptFile, File
from .helper import syscall

log = logging.getLogger(__name__)


class Manuscript:

    @classmethod
    def create(cls,
               files: List[File],
               create_pdf_a=True,
               create_pdf_s=True,
               create_pdf_w=True,
               create_text=True
               ) -> Optional[List[ManuscriptFile]]:
        manuscripts: List[ManuscriptFile] = list()
        temp_dir = tempfile.TemporaryDirectory()
        cls.__convert_images_to_pdf_and_text(
            files,
            temp_dir.name,
            create_pdf_a,
            create_pdf_s,
            create_pdf_w or create_text
        )

        if create_pdf_a:
            log.info("creating PDF_A")
            manuscripts.append(cls.create_pdf_a(temp_dir.name))

        if create_pdf_s:
            log.info("Creating PDF_S")
            manuscripts.append(cls.create_pdf_s(temp_dir.name))

        if create_pdf_w:
            log.info("Creating PDF_W")
            manuscripts.append(cls.create_pdf_w(temp_dir.name))

        if create_text:
            log.info("Creating Text")
            text_file = cls.create_text(temp_dir.name)
            if text_file is not None:
                manuscripts.append(text_file)

        temp_dir.cleanup()
        return manuscripts

    @classmethod
    def __convert_images_to_pdf_and_text(
            cls, files: List[File], tempdir: str, create_pdf_a: bool, create_pdf_s: bool, create_text: bool
    ) -> None:
        tot = len(files)

        for count, file in enumerate(files, start=1):
            filename = "%05d" % count
            log.info(f"Processing {file.filepath} -> {filename}.pdf ({count} of {tot})")
            if create_pdf_a:
                log.info(f"{file.identifier} - {file.filepath} to PDF_A page")
                cls.__image_to_pdf_a_page(file.filepath, filename, tempdir)

            if create_pdf_s:
                log.info(f"{file.identifier} - {file.filepath} to PDF_S page")
                cls.__image_to_pdf_s_page(file.filepath, filename, tempdir)

            if create_text:
                log.info(f"{file.identifier} - {file.filepath} to TEXT")
                cls.__image_to_text_page(file.filepath, filename, tempdir)

    @classmethod
    def create_pdf_a(cls, tempdir: str) -> ManuscriptFile:
        files = sorted([
            os.path.join(tempdir, f) for f in os.listdir(tempdir)
            if os.path.isfile(os.path.join(tempdir, f)) and re.match(r'^\d+\.pdf$', f) is not None
        ])
        log.info(f"files to create the PDF_A are {files}")
        try:
            temp_file = pypdftk.concat(files)  # TODO - typo with import of tempfile
            return ManuscriptFile(key="PDF_A", filepath=temp_file)
        except Exception as e:
            raise e

    @classmethod
    def create_pdf_s(cls, tempdir: str) -> ManuscriptFile:
        files = sorted([
            os.path.join(tempdir, f) for f in os.listdir(tempdir)
            if os.path.isfile(os.path.join(tempdir, f)) and re.match(r'^\d+S\.pdf$', f) is not None
        ])
        log.info(f"files to create the PDF_S are {files}")
        try:
            temp_file = pypdftk.concat(files)
            pdf_out_gs = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            args = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.5",
                "-dPDFSETTINGS=/ebook",
                "-dNOPAUSE",
                "-dBATCH",
                "-dQUIET",
                "-sOutputFile=" + pdf_out_gs.name,
                temp_file
            ]
            syscall(args)
            return ManuscriptFile(key="PDF_S", filepath=temp_file)
        except Exception as e:
            raise e

    @classmethod
    def create_pdf_w(cls, tempdir: str) -> ManuscriptFile:
        files = sorted([
            os.path.join(tempdir, f) for f in os.listdir(tempdir)
            if os.path.isfile(os.path.join(tempdir, f)) and re.match(r'^\d+\.txt$', f) is not None
        ])
        temp_dir_of_pdfw = tempfile.TemporaryDirectory()
        for i, f in enumerate(files, start=1):
            ps_file = tempfile.NamedTemporaryFile(suffix=".ps", delete=False)
            syscall(["enscript", "--no-header", "-p", ps_file.name, f], ignore_stderr=True)
            syscall(["ps2pdf", ps_file.name, "%s/%05d.pdf" % (temp_dir_of_pdfw.name, i)])
        temp_pdf = pypdftk.concat([
            os.path.join(temp_dir_of_pdfw.name, f)
            for f in os.listdir(temp_dir_of_pdfw.name)
        ])
        temp_dir_of_pdfw.cleanup()
        return ManuscriptFile(key="PDF_W", filepath=temp_pdf)

    @classmethod
    def create_text(cls, tempdir: str) -> Optional[ManuscriptFile]:
        files = sorted([
            os.path.join(tempdir, f)
            for f in os.listdir(tempdir)
            if os.path.isfile(os.path.join(tempdir, f)) and re.match(r'^\d+\.txt$', f) is not None
        ])
        log.info(f"files to create the TEXT are {files}")
        temp_text = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        with open(temp_text.name, 'wb') as wfd:
            for f in files:
                with open(f, 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)
        if os.stat(temp_text.name).st_size == 0:
            return None

        return ManuscriptFile(key="OCR_TEXT", filepath=temp_text.name)

    @staticmethod
    def __image_to_pdf_a_page(file, filename, tempdir):
        try:
            pdf_data = pytesseract.image_to_pdf_or_hocr(
                file,
                lang="eng",
                extension="pdf"
            )
            pdf_out = os.path.join(tempdir, "%s.pdf" % filename)
            with open(pdf_out, mode="w+b") as f:
                f.write(pdf_data)
        except Exception as e:
            raise e

    @staticmethod
    def __image_to_pdf_s_page(file, filename, tempdir):
        try:
            tmp_jpeg = tempfile.NamedTemporaryFile(suffix="jpeg")
            # first resample images to 150
            with Image(filename=file) as original:
                with original.convert('jpeg') as img:
                    img.units = "pixelsperinch"
                    img.resample(150, 150)
                    img.save(filename=tmp_jpeg.name)
            pdf_data = pytesseract.image_to_pdf_or_hocr(
                tmp_jpeg.name,
                lang="eng",
                extension="pdf"
            )
            pdf_out = os.path.join(tempdir, "%sS.pdf" % filename)
            with open(pdf_out, mode="w+b") as f:
                f.write(pdf_data)
        except Exception as e:
            raise e

    @staticmethod
    def __image_to_text_page(file, filename, tempdir):
        text_out = os.path.join(tempdir, "%s.txt" % filename)

        text_data = pytesseract.image_to_string(
            file,
            lang="eng"
        )
        with open(text_out, mode="w") as f:
            f.write(text_data)
        return text_data
