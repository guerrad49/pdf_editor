### Requirements

- **[PyPDF2](https://pypi.org/project/PyPDF2/)**

***

### Description

This module includes functions for modifying a single or multiple pdfs. All functions make use of PyPDF2 library.

***

### Flags

1. **SPLIT**

	This flag takes a base pdf (from now on refered to as *file*) and writes a pdf for each page with the format: file_page##.pdf
	> ./pdf_editor.py file -s

2. **MERGE**
  
	This flag combines multiple pdfs and yields and output named: merged_file.pdf. *Note: Regular expressions can be used for simplicity.*
	> ./pdf_editor.py file -m file2 file3
	> ./pdf_editor.py file_page01 -m file_page0[4-8].pdf

3. **REORDER**

	This flag switches the order of a subset of pages of a pdf. The user provides a comma-separated list. If the list is two-long, the two pages will be swapped. If the list is larger, the list must be in consecutive order.
	> ./pdf_editor.py file -o '2,6'
	> ./pdf_editor.py file -o '5,4,3'
  
4. **REMOVE**

	This flag deletes specific pages from the main pdf given as a comma-separated list.
	> ./pdf_editor.py file -r '2,4,8,10'