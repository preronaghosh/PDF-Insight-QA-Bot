from app.chat.score import random_component_by_score
from langchain.chat_models import ChatOpenAI

from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain

from app.web.api import set_conversation_components, get_conversation_components


"""
    Helper function for selecting components for retrievers
""" 
def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(
        conversation_id=chat_args.conversation_id
    )
    previous_component = components[component_type]

    if previous_component:
        # this is NOT a new message
        # use the previous combination of components
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        # this is a follow up question, use random components
        random_component_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_component_name]
        return random_component_name, builder(chat_args)
    

"""
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
"""
def build_chat(chat_args: ChatArgs):
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    
    # debug
    print(f"Running chain with memory: {memory_name}, llm: {llm_name} and retriver: {retriever_name}..")
    # save this combination to the db
    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name, 
        memory=memory_name
    )
    condense_question_llm = ChatOpenAI(streaming=False)

    return StreamingConversationalRetrievalChain.from_llm(
        memory=memory,
        llm=llm,
        retriever=retriever,
        condense_question_llm=condense_question_llm
    )
