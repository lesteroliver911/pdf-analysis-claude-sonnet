# PDF Analysis with Claude 3.5 Sonnet

A Streamlit application that leverages Claude 3.5 Sonnet and LlamaIndex to analyze PDF documents intelligently. The app supports both single PDF and batch processing modes, with features like response caching and detailed document analysis.

This project is inspired by and built upon Anthropic's [PDF Support Documentation](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support), implementing their best practices for PDF analysis with Claude in a user-friendly web interface.

## Features

- **Single PDF Analysis**: Process individual PDFs with custom queries
- **Batch Processing**: Analyze multiple PDFs simultaneously
- **Response Caching**: Cache results for faster repeated queries
- **Intelligent Analysis**: Powered by Claude 3.5 Sonnet and LlamaIndex
- **Vector Embeddings**: Uses OpenAI's text-embedding-3-small model for document indexing
- **User-Friendly Interface**: Clean Streamlit UI with sidebar controls

## Prerequisites

Before running the application, make sure you have:

- Python 3.8 or higher
- An Anthropic API key
- An OpenAI API key (for embeddings)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lesteroliver911/pdf-analysis-claude-sonnet.git
cd pdf-analysis-claude-sonnet
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Navigate to the app in your browser (typically http://localhost:8501)

3. Choose your processing mode:
   - Single PDF: Enter a single PDF URL and query
   - Batch Processing: Enter multiple PDF URLs (one per line)

4. Enter your analysis query

5. Click "Analyze PDF(s)" to start the analysis

## Limitations

- Maximum PDF file size: 32MB
- Maximum number of pages: 100
- Rate limits based on your Anthropic and OpenAI API quotas

## Dependencies

- anthropic
- httpx
- streamlit
- llama-index
- python-dotenv
- openai

## Project Structure

```
pdf-analysis-claude-sonnet/
├── app.py              # Main application file
├── .env               # Environment variables (create this)
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Environment Variables

The following environment variables are required:

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `OPENAI_API_KEY`: Your OpenAI API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude 3.5 Sonnet and their comprehensive [PDF support documentation](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)
- [LlamaIndex](https://www.llamaindex.ai/) for document indexing capabilities
- [OpenAI](https://openai.com/) for embedding model
- [Streamlit](https://streamlit.io/) for the web interface

## Support

For support, please open an issue in the GitHub repository.
