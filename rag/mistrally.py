
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings,ChatMistralAI
from langchain.text_splitter import RecursiveCharacterTextSplitter as rr
from dotenv import load_dotenv
from typing import TypedDict,Annotated,Sequence,List
from langgraph.graph.message import add_messages
from langchain_core.messages import     BaseMessage,HumanMessage,AIMessage,SystemMessage
from langchain.prompts import PromptTemplate
load_dotenv()
from langchain.tools import tool
import os
from langgraph.prebuilt import ToolNode
from langchain_google_community.search import GoogleSearchAPIWrapper
from langgraph.graph import START,END,StateGraph
search=GoogleSearchAPIWrapper(google_api_key=os.getenv("google_api_key"),google_cse_id=os.getenv("google_cse_id"))
class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage],add_messages]
    context_csv:List[str]
    context_txt:str
    context_Ai:str

@tool
def searchy(state:AgentState)-> AgentState:
    """this tool is used to search the content in internet dont hallucinate
    Args-
    question- the question you want to search in internet"""
    global search
    state['context_txt']=search.run(state['message'][-1].content)
    print("result search-", state['context_txt'])
    return state


@tool
def cutoff_calc(maths:int,phy:int,chem:int)->float:
    """this tool is used to calculate the cutoff of the student based on 12 th mark
    formula of cuttoff=(maths+(phy+chem)/2)
    Args-
    maths-mark of the maths
    phy-mark of the physics
    chem-mark of the chemistry
    """
    cuttoff=(maths+(phy+chem)/2)
    return cuttoff

tools=[searchy,cutoff_calc]






embed=MistralAIEmbeddings(model="mistral-embed",api_key=os.getenv('mistral_api'))
vectordb=Chroma(collection_name="cutoff_data",embedding_function=embed,
    persist_directory="chroma_db")
retriever=vectordb.as_retriever(search_type="similarity",search_kwargs={"k":10})
model=ChatMistralAI(model="mistral-small",api_key=os.getenv('mistral_api'),max_tokens=250,temperature=0.9).bind_tools(tools)
#print(model.invoke("what is common thing between optimus prime and you").content)

def agent(state:AgentState)-> str:
    """ this node is used to for llm connection"""
    global model,retriever
    sytem = SystemMessage(content="""
You are a responsible and helpful assistant guiding students through Tamil Nadu Engineering Admissions (TNEA) counselling.

Your capabilities include:
- A **search tool** (`searchy`) that queries the internet for college-related information. Use this tool *if you do not have enough context* from vector search.
- A **cutoff calculator** (`cutoff_calc`) to compute student cutoffs using the formula: (maths + (physics + chemistry)/2).

Guidelines:
- Use tools **before responding**, especially for college-specific queries or when information is missing or uncertain.
- **Avoid hallucinating** or assuming any data. Instead, invoke tools to search or compute.
- Prefer colleges with a cutoff **equal to or below** the student’s cutoff. Do not suggest higher-cutoff colleges.
- Respond precisely, factually, and with clarity.
- Use `searchy` to validate ownership, management, or location questions about a college.
 -in csv 0 mean o student got seat in that department so it has high chance getting seat or no seat for the category
-if studenet ask cutt of the college but didnt mention his category and cutoff show all the category cutoff
 dont ask cutoff untill they provide                         -
""")

    retrieved_docs = retriever.invoke(state["message"][-1].content)
    state["context_csv"] = retrieved_docs

    template="""You are a RAG-based agent assisting with Tamil Nadu Engineering Admissions.

Context from documents:
{context}

Web data from search tool:
{search}

Question:
{question}

Based on the above, provide a precise, factual answer. If information is missing,  invoke the searchy tool.
"""
    prompt=PromptTemplate(template=template)
    prompt=prompt.invoke({'question':state["message"][-1],'search':state["context_txt"],'context':state["context_csv"]})
    state['message'].append(HumanMessage(content=prompt.text))

    prmpt=[sytem]+state["message"]
   # print(prmpt)
    result=model.invoke(prmpt)
   # print(result.content)
    state['message'].append(AIMessage(content=result.content))
    state['context_txt']=[]

    state['context_Ai']=result.content
    return state
def shouldcontinue(state:AgentState)->str:
    last=state['message'][-1]
    if last.tool_calls:
        print('tool')
        return 'tools'
    else:
        return 'end'


#agent({"message":["what is cutoff saranathan AD "],"context_txt":"" ,'context_csv':[]})

graph=StateGraph(AgentState)
graph.add_node("rag",agent)
graph.set_entry_point('rag')

toolnode=ToolNode(tools)
graph.add_node('tool',toolnode)
graph.add_conditional_edges('rag',shouldcontinue,{'tools':'tool','end':END})
graph.add_edge('tool','rag')
app=graph.compile()

def appy(st:str):
    global app
    return app.invoke({"message":[st],"context_txt":"" ,'context_csv':[]})['context_Ai']


