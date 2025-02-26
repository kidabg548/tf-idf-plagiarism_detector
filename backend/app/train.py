import logging
from models import train_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting training process...")
        train_model()  # Call the function to train the model
        logging.info("Training completed successfully.")
    except Exception as e:
        logging.error(f"Error during training: {e}")

if __name__ == "__main__":
    main()
