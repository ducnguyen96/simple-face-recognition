from src.extractor import get_all_embedding, prepare_data
from src.classification import train_classification_model


if __name__ == "__main__":
    prepare_data()

    get_all_embedding()

    train_classification_model()
