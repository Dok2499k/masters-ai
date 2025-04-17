import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from utils.loader import load_and_split_documents
from dotenv import load_dotenv

load_dotenv()

# Get OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Directories for vectorstore and document data
VECTORSTORE_DIR = "vectorstore/"
DATA_DIR = "data/"

# Initialize embeddings
embeddings = OpenAIEmbeddings(api_key=api_key)

# Initialize ChatOpenAI without passing unsupported parameters.
llm = ChatOpenAI(
    model="gpt-4o",  # Update this as needed. Ensure your model supports the ChatCompletion API.
    temperature=0.2,
    api_key=api_key
)

# Create a custom prompt template to force the LLM to only rely on provided context.
custom_prompt = PromptTemplate(
    template="""
You are a literary assistant focused exclusively on the works of Fyodor Dostoevsky.
Use ONLY the following context from Dostoevsky's texts to answer the question.
If you cannot find the answer in the context, respond with:
"I couldn't find relevant information in Dostoevsky's works."

Context:
{context}
Question: {question}
Answer:""",
    input_variables=["context", "question"]
)

# Load or create the vectorstore.
def load_or_create_vectorstore():
    if os.path.exists(VECTORSTORE_DIR) and os.path.exists(os.path.join(VECTORSTORE_DIR, "index.faiss")):
        print("✅ Loading existing vectorstore...")
        db = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    else:
        print("🛠️ No vectorstore found. Creating a new one...")
        docs = load_and_split_documents(DATA_DIR)
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(VECTORSTORE_DIR)
    return db

# Initialize the vector DB.
db = load_or_create_vectorstore()

# Build the RetrievalQA chain using the custom prompt template.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={
         "prompt": custom_prompt  # Use our custom prompt that restricts the answer.
    }
)

def ask_question(question: str):
    # Invoke the QA chain with the query.
    result = qa_chain.invoke({"query": question})
    answer = result["result"].strip()

    # Define the fallback answer exactly as instructed in your prompt.
    fallback_text = "I couldn't find relevant information in Dostoevsky's works."
    # If the answer includes the fallback text, hide the sources.
    if fallback_text in answer:
        return answer, "", 0.0

    # Otherwise, extract sources from the retrieved documents.
    sources = []
    for doc in result["source_documents"]:
        meta = doc.metadata
        file_name = os.path.basename(meta.get("source", "Unknown file"))
        page_number = meta.get("page", "unknown page")
        sources.append(f"{file_name} p.{page_number}")

    source_text = ", ".join(sources)
    confidence = 0.7 if sources else 0.0

    return answer, source_text, confidence
