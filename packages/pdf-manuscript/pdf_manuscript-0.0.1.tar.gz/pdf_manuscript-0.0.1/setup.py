import setuptools

setuptools.setup(
    name="pdf_manuscript",
    version="0.0.1",
    author="Rui Meira",
    author_email="ruimiguelcm96@gmail.com",
    description="Package to create PDF and Text files from TIFF images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)