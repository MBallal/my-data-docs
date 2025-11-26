#!/usr/bin/env python3
import pdfplumber
import sys
import re

pdf_path = "Star schema _ the complete reference -- Christopher Adamson -- The Complete Reference, 1, 2010 -- McGraw-Hill Osborne Media -- 9780071744324 -- 50bb5de0889b8387087a8944b4be4cc3 -- Anna's Archive.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        chapter9_text = []
        in_chapter9 = False
        chapter9_start_pattern = re.compile(r'Chapter\s+9|CHAPTER\s+9', re.IGNORECASE)
        chapter10_start_pattern = re.compile(r'Chapter\s+10|CHAPTER\s+10', re.IGNORECASE)
        
        print(f"Total pages: {len(pdf.pages)}", file=sys.stderr)
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Check if we're starting Chapter 9
                if chapter9_start_pattern.search(text) and not in_chapter9:
                    in_chapter9 = True
                    print(f"Found Chapter 9 start at page {i+1}", file=sys.stderr)
                
                # Check if we're starting Chapter 10 (end of Chapter 9)
                if chapter10_start_pattern.search(text) and in_chapter9:
                    print(f"Found Chapter 10 start at page {i+1} (end of Chapter 9)", file=sys.stderr)
                    break
                
                if in_chapter9:
                    chapter9_text.append(f"--- Page {i+1} ---\n{text}\n")
        
        if chapter9_text:
            print("".join(chapter9_text))
        else:
            print("Chapter 9 not found. Listing all chapter headings:", file=sys.stderr)
            # Try to find all chapters
            for i, page in enumerate(pdf.pages[:50]):  # Check first 50 pages
                text = page.extract_text()
                if text:
                    matches = re.findall(r'Chapter\s+\d+|CHAPTER\s+\d+', text, re.IGNORECASE)
                    if matches:
                        print(f"Page {i+1}: {matches}", file=sys.stderr)
                        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
