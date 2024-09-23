import json
from typing import Tuple
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Clase para gestionar el dataset
class SpiderDatasetLoader:
    def __init__(self, path: str):
        self.path = path
        self.dataset = None

    def load_dataset(self) -> Dataset:
        with open(self.path + 'train_spider.json', 'r') as f:
            spider_data_1 = json.load(f)
        with open(self.path + 'train_others.json', 'r') as f:
            spider_data_2 = json.load(f)

        spider_data = spider_data_1 + spider_data_2
#        spider_data = spider_data[:10]
        
        data_dict = {
            "question": [],
            "sql": [],
            "db_id": []
        }
        for entry in spider_data:
            data_dict["question"].append(entry["question"])
            data_dict["sql"].append(entry["query"])
            data_dict["db_id"].append(entry["db_id"])

        self.dataset = Dataset.from_dict(data_dict)
        return self.dataset

    def split_dataset(self, test_size=0.1) -> Tuple[Dataset, Dataset]:
        train_test_split = self.dataset.train_test_split(test_size=test_size)
        return train_test_split['train'], train_test_split['test']


# Clase para gestionar el modelo T5
class T5Model:
    def __init__(self, model_name="t5-small"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def preprocess_function(self, examples: Dataset) -> Dataset:
        inputs = ["translate English to SQL: " + q for q in examples["question"]]
        targets = [sql for sql in examples["sql"]]
        model_inputs = self.tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

        # Tokenizar las consultas SQL
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(targets, max_length=128, truncation=True, padding="max_length")

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def save_model(self, path: str):
        self.tokenizer.save_pretrained(path + "tokens_T5")
        self.model.save_pretrained(path + "modelo_T5")

    def load_model(self, path: str):
        self.tokenizer = T5Tokenizer.from_pretrained(path + "tokens_T5")
        self.model = T5ForConditionalGeneration.from_pretrained(path + "modelo_T5")

    def generate_sql(self, query: str) -> str:
        inputs = self.tokenizer("translate English to SQL: " + query, return_tensors="pt", max_length=128, truncation=True)
        outputs = self.model.generate(inputs["input_ids"], max_length=150)
        sql_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return sql_query


# Clase para gestionar el entrenamiento
class T5Trainer:
    def __init__(self, model: T5Model, train_dataset: Dataset, eval_dataset: Dataset):
        self.model = model
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset
        self.training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            save_steps=10_000,
            save_total_limit=2,
        )

        self.trainer = Trainer(
            model=self.model.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            tokenizer=self.model.tokenizer,
        )

    def train(self):
        self.trainer.train()


# Clase principal que orquesta el proceso
class SQLGenerator:
    def __init__(self, dataset_path: str, model_save_path: str):
        self.dataset_path = dataset_path
        self.model_save_path = model_save_path
        self.dataset_loader = SpiderDatasetLoader(dataset_path)
        self.model = T5Model()

    def run(self):
        # Cargar y dividir el dataset
        dataset = self.dataset_loader.load_dataset()
        train_dataset, eval_dataset = self.dataset_loader.split_dataset()

        # Preprocesar datasets
        tokenized_train_dataset = train_dataset.map(self.model.preprocess_function, batched=True)
        tokenized_eval_dataset = eval_dataset.map(self.model.preprocess_function, batched=True)

        # Entrenar el modelo
        trainer = T5Trainer(self.model, tokenized_train_dataset, tokenized_eval_dataset)
        trainer.train()

        # Guardar el modelo
        self.model.save_model(self.model_save_path)

    def load_trained_model(self):
        self.model.load_model(self.model_save_path)

    def generate(self, query):
        return self.model.generate_sql(query)


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar la clase principal con las rutas de los archivos
    dataset_path = '/home/julian/workspaces/prueba-python/ML/spider_data/'
    model_save_path = '/home/julian/workspaces/prueba-python/ML/Models/'

    # Crear el generador de SQL
    sql_generator = SQLGenerator(dataset_path, model_save_path)

    # Ejecutar el proceso de carga del dataset, entrenamiento y guardado del modelo
    sql_generator.run()

    # Cargar el modelo entrenado y generar una consulta SQL
    sql_generator.load_trained_model()

    # Probar con varias preguntas
    queries = [
        "List the name, born state and age of the heads of departments ordered by age.",
        "List the names of all actors.",
        "Show the movies released after 2010.",
        "Find the average salary of employees.",
        "List the names of all actors order by age",
    ]

    for query in queries:
        generated_sql = sql_generator.generate(query)
        print("Consulta SQL generada: ", generated_sql)
