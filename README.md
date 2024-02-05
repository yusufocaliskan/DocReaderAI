# Workflow of the Model

1. Get the pdf files from client
2. Extract all the text of the pages of the files
3. Combine all the extracted text and store them in an array
4. Convert the combined text in to vectors and store in FAISS database
5. Get the question of the client
6. Get the relavent text in the FAISS db.

- To get the relavent part of the extradted text based on cleint queries.
- Why do we need to do it?
  - Sending all the extracted data from cleint's uploaded files to the AI-Model (in this case Chat GGPT) is imposible, because of the token limitaion of the OpenAI
  - So we need a relavent data in the context of the client's query
  - The vectoral database FAISS would produce few nears neighbor text accourding to the client's (question)
  - Based on the result of FAISS query, at this stage, the data is still raw,
    Therefore we are preparing the raw data for Chat-GPT to generate a meaningfull response

7. Send the to chat gpt
8. Display the response

# Notes

## FAISS

- FAISS achieves optimal performance when using the CPU; increasing the CPU amount can enhance performance. (https://faiss.ai/index.html)
- Most algorithms of FAISS are implemented on the CPU
- FAISS alse uses RAM, becareful(!)
- The K parametter is the nearest neighbor that FAISS would produce (2nd and n. nearst )

@yusufocaliskan
