mainDocReaderPromptTemplate = """
                Please use a maximum of 150 words to answer the question provided. 
                Your response should be directly relevant to the question, avoiding any extraneous information not required by the user. 
                Respond in the same language as the question to maintain consistency and understanding. 
                Critically interpret the context given to offer the most accurate and pertinent answer. 
                If the information within the context is ambiguous or incomplete, explicitly note the ambiguity or specify what additional data could render your answer more comprehensive. 
                Whenever possible, justify your answer by citing specific segments of the context. 

                Consider the reliability of the information presented in the documents, and be mindful of cultural and contextual nuances. 
                Use inclusive language and approach the context from diverse perspectives. 
                If the context includes data or statistics, analyze and summarize these to support your answer. 
                Should direct information be lacking, feel free to propose hypotheses or likely scenarios based on the provided context, clearly indicating them as speculative. 
                Indicate if further information is needed for a more detailed response, and specify what details would enable a more complete answer.

                My question is: {question}

                The context is: {docs}
            """
