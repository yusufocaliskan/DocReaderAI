# Workflow of the Model

1. Get the pdf files from client
2. Extract all the text of the pages of the files
3. Combine all the extracted text and store them in an array
4. Convert the combined text in to vectors and store in FAISS database
5. Get the question of the client
6. Get the relavent text in the FAISS db.[^1]

- 6.1 - To get the relavent part of the extradted text based on cleint queries.

  - 6.2 Why do we need to do it?

    - 6.2.1 - Sending all the extracted data from cleint's uploaded files to the AI-Model (in this case Chat GGPT) is imposible, because of the token limitaion of the OpenAI
    - 6.2.2 - So we need a relavent data in the context of the client's query
    - 6.2.3 - The vectoral database FAISS would produce few nears neighbor text accourding to the client's (question)
    - 6.2.4 - Based on the result of FAISS query, at this stage, the data is still raw,
      Therefore we are preparing the raw data for Chat-GPT to generate a meaningfull response

7. Send the to chat gpt
8. Display the response

# Notes

## FAISSS

- FAISS alse uses RAM, becareful(!)
- FAISS achieves optimal performance when using the CPU; increasing the CPU amount can enhance performance. (https://faiss.ai/index.html)
- Most algorithms of FAISS are implemented on the CPU
- Tre K parametter is the nearest neighbor that FAISS would produce (2nd and n. nearst )

## Usefull Links

- Faiss Doc --> https://faiss.ai/index.html
- How Language Models Use Long Contexts --> https://arxiv.org/pdf/2307.03172.pdf
- MultiVector --> https://python.langchain.com/docs/modules/data_connection/retrievers/multi_vector
- Ensemble Reciever: --> https://python.langchain.com/docs/modules/data_connection/retrievers/ensemble
  - Helps to combine docs that extracted from different docs
- LongContextReorder() : ReOrdering relavent documents is to get better performance : -->https://python.langchain.com/docs/modules/data_connection/retrievers/long_context_reorder
- Compare Multiple Large Files : https://www.youtube.com/watch?v=UmvqMscxwoc&list=PLY_VzrnxwMWhD4EgclTv0jymk84xRp3ab&index=3
- Prompt Engineering : https://www.promptingguide.ai/models/chatgpt

@yusufocaliskan
