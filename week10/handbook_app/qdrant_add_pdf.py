from qdrant_store import vectorstore, client
import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter, MarkdownTextSplitter
from langchain_core.documents import Document
import requests
import os
import re

PDF_URL = "https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2024-25_English.pdf"

if os.path.exists("student_handbook.pdf"):
    print("File already exists")
else:
    print("Downloading PDF")
    r = requests.get(PDF_URL)
    with open("student_handbook.pdf", "wb") as f:
        f.write(r.content)

count = client.count("polyu_handbook").count
print(count)

md_text = pymupdf4llm.to_markdown("student_handbook.pdf")

with open("student_handbook.md", "w", encoding="utf-8") as f:
    f.write(md_text)

# First, preprocess the markdown to convert **A. Title** patterns to proper headers
def preprocess_markdown_sections(text):
    """Convert **A. Title** patterns to ### headers for better splitting"""
    # Pattern to match **A. Title**, **B. Title**, etc.
    pattern = r'\*\*([A-Z]\. [^*]+)\*\*'
    
    # Find all matches to show what we're converting
    matches = re.findall(pattern, text)
    print(f"Found {len(matches)} section headers to convert:")
    for i, match in enumerate(matches[:10]):  # Show first 10
        print(f"  {i+1}. {match}")
    if len(matches) > 10:
        print(f"  ... and {len(matches) - 10} more")
    
    # Replace with ### header
    processed_text = re.sub(pattern, r'### \1', text)
    return processed_text

# Preprocess the markdown text
processed_md_text = preprocess_markdown_sections(md_text)

# Use a more careful approach - split only on main chapters first
headers_to_split_on = [
    ("######", "Chapter"),
]

chapter_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, 
    strip_headers=False,
    return_each_line=False
)

chapter_documents = chapter_splitter.split_text(processed_md_text)
print(f"Total chapters created: {len(chapter_documents)}")

# Now manually split each chapter by sections, ensuring we include content
final_documents = []

for doc in chapter_documents:
    content = doc.page_content
    
    # Split by ### headers (our converted sections)
    section_parts = re.split(r'\n(### [A-Z]\. [^\n]+)\n', content)
    
    if len(section_parts) == 1:
        # No subsections found, keep the whole chapter if it has substantial content
        if len(content.strip()) > 50:  # Only keep if there's meaningful content
            final_documents.append(doc)
    else:
        # First part (before any section header)
        if section_parts[0].strip() and len(section_parts[0].strip()) > 50:
            intro_doc = Document(
                page_content=section_parts[0].strip(),
                metadata=dict(doc.metadata)
            )
            final_documents.append(intro_doc)
        
        # Process sections with their content
        for i in range(1, len(section_parts), 2):
            if i + 1 < len(section_parts):
                section_header = section_parts[i]
                section_content = section_parts[i + 1].strip()
                
                # Only create document if there's substantial content
                if len(section_content) > 50:
                    combined_content = section_header + "\n\n" + section_content
                    
                    section_doc = Document(
                        page_content=combined_content,
                        metadata={
                            **doc.metadata,
                            "Section": section_header.replace("### ", "")
                        }
                    )
                    final_documents.append(section_doc)

print(f"Documents after section splitting: {len(final_documents)}")

# Apply size-based splitting for very large documents
size_split_documents = []
markdown_splitter = MarkdownTextSplitter(
    chunk_size=1500,  # Smaller chunks for better retrieval
    chunk_overlap=200,
    length_function=len,
)

for doc in final_documents:
    if len(doc.page_content) > 1500:
        # Split large documents while preserving metadata
        subdocs = markdown_splitter.create_documents([doc.page_content], [doc.metadata])
        size_split_documents.extend(subdocs)
    else:
        size_split_documents.append(doc)

print(f"Final documents after size-based splitting: {len(size_split_documents)}")

# Filter out documents that are too short or only contain headers
filtered_documents = []
for doc in size_split_documents:
    content = doc.page_content.strip()
    # Skip documents that are just headers or very short
    if (len(content) > 100 and 
        not re.match(r'^#{1,6}\s+\*?\*?[^*]*\*?\*?$', content.strip()) and
        not content.startswith('######') or len(content) > 200):
        filtered_documents.append(doc)

print(f"Documents after filtering short/header-only content: {len(filtered_documents)}")
final_documents = filtered_documents

# Show sample documents to verify content quality
print("\nSample documents:")
for i, doc in enumerate(final_documents[:3]):
    print(f"\nDocument {i+1}:")
    print(f"Length: {len(doc.page_content)}")
    print(f"Metadata: {doc.metadata}")
    print(f"Content preview: {doc.page_content[:200]}...")

vectorstore.add_documents(final_documents)

count = client.count("polyu_handbook").count
print("Added", len(final_documents), "documents. Total count:", count)

query = vectorstore.similarity_search("lost student id")
print(query)

vectorstore._client.close()

