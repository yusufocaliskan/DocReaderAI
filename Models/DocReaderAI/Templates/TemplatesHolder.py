class TemplatesHolder:

    mainDocReaderTemplate = """
        You are a document reader, read the context and answer the question in a polite manner.
        Use maximum of 150 words to answer my question. 
        Also answer with same language User using in the question
        Use the following pieces of context and try your best to answer user question.
        If data is tabular, analyze data as tabular data not text or pdf.


        My question is: {question}
        Before i give you some context, let me explain the shape of the context that you would need know
        when answering the question, 

        Document Example:
                Document- 
                Document<no> Source: <source> 
                Document<no> Page: <source> 
                Document <no> Content:<source> 

        Each document has owen content, metadata, source and page number, pay attention the exxample of the documents when answerig,
        and try to not to confues other documents if the question is one the one specific document. 
        The context is: {docs}
        
    """
    meaninfulNamesGeneratorPromptTemplate = """
        You are a pdf reader. Read the content create
        a meaning full file name base on the content
        If you can't, find the title of the  content
        The content is: {docs}
    """
    summarizTextTemplate = """
        Summarize the content. Remember the person name and file name 

        The context is: {docs}

        Example:
        - Person Name and file name:
            the summarize content about person
        - The second Person Name and file name:
            the summarize content about person
    """
