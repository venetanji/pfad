from langchain_core.documents import Document
from weaviate_store import vectorstore
import pymupdf4llm
from langchain.text_splitter import MarkdownHeaderTextSplitter
import requests
import os

PDF_URL = "https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2024-25_English.pdf"

if os.path.exists("student_handbook.pdf"):
    print("File already exists")
else:
    print("Downloading PDF")
    r = requests.get(PDF_URL)
    with open("student_handbook.pdf", "wb") as f:
        f.write(r.content)

count = vectorstore._collection.aggregate.over_all(total_count=True)
print(count)

md_text = pymupdf4llm.to_markdown("student_handbook.pdf")
headers_to_split_on = [
    ("######", "Header"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
documents = splitter.split_text(md_text)

vectorstore.add_documents(documents)

count = vectorstore._collection.aggregate.over_all(total_count=True)
print("Added", len(documents), "documents. Total count:", count)

query = vectorstore.similarity_search("lost student id")
print(query)

vectorstore._client.close()

