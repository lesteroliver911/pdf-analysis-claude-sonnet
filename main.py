import anthropic
import base64
import httpx
from dotenv import load_dotenv
import os
import streamlit as st
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

# Load environment variables
load_dotenv()

class PDFProcessor:
    def __init__(self):
        # Initialize Anthropic LLM through LlamaIndex
        self.llm = Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            model="claude-3-sonnet-20240229"
        )
        # Set the LLM as default for LlamaIndex
        Settings.llm = self.llm
        
        # Set up OpenAI embeddings
        Settings.embed_model = OpenAIEmbedding(
            api_key=os.getenv('OPENAI_API_KEY'),
            model="text-embedding-3-small"
        )
        
        # Initialize cache
        self.cache = {}
        self.index_cache = {}

    def create_index_from_pdf(self, pdf_url):
        """Create a vector store index from PDF"""
        if pdf_url in self.index_cache:
            return self.index_cache[pdf_url]

        try:
            # Download PDF
            pdf_content = httpx.get(pdf_url).content
            
            # Save PDF temporarily
            temp_pdf_path = "temp.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(pdf_content)

            # Load and parse document
            documents = SimpleDirectoryReader(
                input_files=[temp_pdf_path]
            ).load_data()
            
            # Create parser
            parser = SentenceSplitter(
                chunk_size=1024,
                chunk_overlap=20
            )
            
            # Create index
            index = VectorStoreIndex.from_documents(
                documents,
                node_parser=parser,
            )

            # Cache the index
            self.index_cache[pdf_url] = index

            # Cleanup
            os.remove(temp_pdf_path)
            
            return index

        except Exception as e:
            raise Exception(f"Error creating index: {str(e)}")

    def process_pdf(self, pdf_url, query, use_cache=True):
        """Process PDF using LlamaIndex"""
        cache_key = f"{pdf_url}:{query}"
        
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Create or get index
            index = self.create_index_from_pdf(pdf_url)
            
            # Create query engine
            query_engine = index.as_query_engine(
                streaming=True,
                similarity_top_k=3,
                response_mode="tree_summarize"
            )
            
            # Query the document
            response = query_engine.query(query)
            
            if use_cache:
                self.cache[cache_key] = str(response)

            return str(response)

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def batch_process_pdfs(self, pdf_urls, query):
        """Batch process PDFs using LlamaIndex"""
        results = []
        
        for url in pdf_urls:
            try:
                result = self.process_pdf(url, query)
                results.append({
                    "url": url,
                    "result": result,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "url": url,
                    "result": str(e),
                    "status": "error"
                })
        return results

# Create a single instance of PDFProcessor
if 'processor' not in st.session_state:
    st.session_state.processor = PDFProcessor()

# Streamlit UI
st.set_page_config(page_title="PDF Analysis with Claude", layout="wide")

# Initialize variables at the top level
pdf_url = None
pdf_urls = None
use_cache = True

# Sidebar for all user inputs
with st.sidebar:
    # Title in sidebar with smaller font
    st.markdown("## PDF Analysis w/ Claude 3.5 Sonnet")
    st.markdown("---")  # Divider line
    
    st.markdown("### Input Options")
    
    # Mode Selection
    is_batch = st.radio("Processing Mode", ["Single PDF", "Batch Processing"])
    
    # Query Input (common for both modes)
    query = st.text_area(
        "Analysis Query",
        value="Analyze this document and provide a detailed summary.",
        height=100,
        help="Enter your question or analysis request"
    )
    
    # PDF Input Section
    st.markdown("### PDF Input")
    if is_batch == "Batch Processing":
        pdf_urls = st.text_area(
            "PDF URLs (one per line)",
            height=150,
            help="Enter each PDF URL on a new line"
        )
    else:
        pdf_url = st.text_input(
            "PDF URL",
            value="https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf",
            help="Enter the URL of the PDF you want to analyze"
        )
        use_cache = st.checkbox("Use cache", value=True, help="Cache results for faster repeated queries")
    
    # Process Button
    process_button = st.button("Analyze PDF(s)")
    
    # About Section at the bottom of sidebar
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses Claude 3 to analyze PDFs. You can:
    - Process single PDFs
    - Batch process multiple PDFs
    - Cache results for faster repeated queries
    
    **Limitations:**
    - Max file size: 32MB
    - Max pages: 100
    """)

# Main content area for results
if process_button:
    if is_batch == "Batch Processing":
        if pdf_urls and pdf_urls.strip():  # Check if pdf_urls exists and is not empty
            st.markdown("## Analysis Results")
            urls_list = [url.strip() for url in pdf_urls.split('\n') if url.strip()]
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner('Processing PDFs...'):
                results = st.session_state.processor.batch_process_pdfs(urls_list, query)
                
                # Results display
                for idx, result in enumerate(results):
                    progress_bar.progress((idx + 1) / len(results))
                    status_text.text(f"Processing PDF {idx + 1} of {len(results)}")
                    
                    with st.expander(f"📄 {result['url'][:50]}...", expanded=True):
                        if result['status'] == 'success':
                            st.markdown("#### Analysis")
                            st.markdown(result['result'])
                        else:
                            st.error(f"Error: {result['result']}")
                
                progress_bar.empty()
                status_text.empty()
                st.success(f"Completed analysis of {len(results)} PDFs")
        else:
            st.warning("Please enter at least one PDF URL in the sidebar")
    
    else:  # Single PDF processing
        if pdf_url and pdf_url.strip():  # Check if pdf_url exists and is not empty
            st.markdown("## Analysis Results")
            try:
                with st.spinner('Analyzing PDF...'):
                    result = st.session_state.processor.process_pdf(
                        pdf_url, 
                        query, 
                        use_cache=use_cache
                    )
                
                st.success("Analysis Complete!")
                
                # Display results in a clean format
                st.markdown("### Document Analysis")
                st.markdown(result)
                
                if use_cache:
                    st.info("ℹ️ This result is cached for faster future queries")
                    
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
        else:
            st.warning("Please enter a PDF URL in the sidebar")
else:
    # Initial state message
    st.markdown("### Welcome! 👋")
    st.markdown("""
    To get started:
    1. Choose your processing mode in the sidebar
    2. Enter the PDF URL(s)
    3. Type your analysis query
    4. Click 'Analyze PDF(s)'
    
    The analysis results will appear here.
    """)
