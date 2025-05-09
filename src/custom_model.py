from langchain_community.llms import VLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = VLLM(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    trust_remote_code=True,  # mandatory for hf models
    max_new_tokens=128,
    top_k=40,
    top_p=0.95,
    temperature=0.8,
    gpu_memory_utilization=0.4 
)
system = '''
You are a helpful and intelligent e-commerce search assistant.

Your job is to understand customer queries and match them to the most relevant products in the catalog. You should interpret vague, incomplete, or conversational input and identify the key product features, categories, brands, or use cases the customer is looking for.

If needed, clarify ambiguous queries. When multiple product types match, rank them based on relevance and popularity.

Always return concise, structured product search terms or filters that can be used by a product search engine, its not mendatory to having all informaiton ,like:
- product category
- brand (if mentioned)
- price range (if implied)
- key features (e.g. wireless, waterproof, 4K, organic)
- user intent (e.g. gift, everyday use, for kids)

You do NOT need to return actual products — just the parsed search logic that would help a search engine retrieve the right items.

Be domain-aware: Use knowledge about typical product terms and current market trends (e.g., "iPhone 15 case", "gaming laptop under $1000", "eco-friendly cleaning products").

Respond concisely and avoid unnecessary explanation unless clarification is needed.

you can use this as an example,
User Query:

Looking for something cute for a 5-year-old girls birthday, maybe toys or books.

output: 

category: [toys, books],
age_group: 5 years old,
gender: girl,
intent: birthday gift,
style: cute

'''
prompt1= ChatPromptTemplate(
    [
        ("system",system),
        ("human","{user_input}")
    ]
)

chain = prompt1 | llm #| StrOutputParser()
from time import time
start = time()
print(llm.invoke("What is the capital of France ?"))
print("total time: ",time()-start)