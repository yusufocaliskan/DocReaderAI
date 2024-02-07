mainDocReaderPromptTemplate = """
   
    Use maximum of 150 words to answer my question. 
    Also answer with same language User using in the question
    Use the following pieces of context and try your best to answer user question.
    If data is tabular, analyze data as tabular data not text or pdf.

    My question is: {question}

    The context is: {docs}
"""
