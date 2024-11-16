from backend.models.HealthcareLLMChat.src.model.chat_pipeline import ChatPipeline
from backend.models.RAG.src.main import main as rag_main
from backend.config.config import Config

class IntegratedPipeline:
    def __init__(self, api_key: str = None):
        self.chat_pipeline = ChatPipeline(api_key)
        
    def run_conversation_and_analysis(self):
        # Start chat conversation
        print("Assistant:", self.chat_pipeline.start_conversation())
        
        while True:
            # Get user input
            user_input = input("\nUser: ")
            
            # Check for exit condition
            if user_input.lower() in ['quit', 'exit', 'bye']:
                # Generate symptom summary
                print("\nGenerating symptom summary...")
                summary = self.chat_pipeline.generate_summary()
                print("\nSYMPTOM SUMMARY:")
                print(summary)
                
                # Use summary as query for RAG system
                print("\nGenerating medical analysis based on similar cases...")
                medical_analysis = rag_main(summary)
                print("\nMEDICAL ANALYSIS:")
                print(medical_analysis)
                break
                
            # Continue conversation
            response = self.chat_pipeline.get_response(user_input)
            print("Assistant:", response)

if __name__ == "__main__":
    Config.validate_env_vars()
    pipeline = IntegratedPipeline(Config.OPENAI_API_KEY)
    pipeline.run_conversation_and_analysis() 