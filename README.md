# topicExtraction application

Language: Python
External libraries: PDFMiner, Pychant, del.dat as our own created file which contains the filtered whitelist words. 

This application is aimed for automated topic extraction process

Instructions:

1. Specify the target directory in line 386 to set up the checking path for the application
2. run the program with any python support IDE
2. choose the grams that will be used for checking the words length from 1-5
3. The application will traverse every PDF file under the specified directory (will check inside any folder if there is any sub-directory here)
4. After every single PDF is checked, the application will output two txt files which includes the file name of the PDF. For example, for one PDF called "file.pdf", the application will generate two txt files as "file.pdf.txt" and "file.pdf.result.txt" under the PDF's current directory. The first file is the txt version of the PDF file, and the second file is the topics that extracted for the file.
5. After the whole directories' files are checked, the application will put all the whitelist words into one file called "all_white.txt". this txt will be generated and placed in the same directory as the topicExtraction.py locates.
