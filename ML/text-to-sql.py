import json, joblib, sys, torch
from typing import Tuple
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

#-------------------------------------------------------------------------------------------------------
def carga_spider_dataset(path: str)-> Dataset:
    def cargar_json(path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    # Leer los datos de ambos archivos JSON
    data1 = cargar_json(path+'/train_spider.json')
    data2 = cargar_json(path+'/train_others.json')

    # Concatenar las listas de datos
    spider_data = data1 + data2

    # Convertir el dataset a un formato legible por Hugging Face Dataset
    data_dict = {
        "question": [],
        "sql": [],
        "db_id": []
    }

    # Extraer las preguntas en lenguaje natural y consultas SQL
    for entry in spider_data:
        data_dict["question"].append(entry["question"])
        data_dict["sql"].append(entry["query"])
        data_dict["db_id"].append(entry["db_id"])  # La base de datos asociada

    # Convertir a Hugging Face Dataset
    return Dataset.from_dict(data_dict)


#-------------------------------------------------------------------------------------------------------
def preparar_dataset_train_eval(dataset: Dataset) -> Tuple[Dataset, Dataset, T5ForConditionalGeneration, T5Tokenizer]:
    # Dividir el dataset en 90% para entrenamiento y 10% para evaluación
    train_test_split = dataset.train_test_split(test_size=0.1)
    train_dataset = train_test_split['train']
    eval_dataset = train_test_split['test']

    # Cargar el modelo y el tokenizer T5 preentrenado
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Preprocesar el dataset para el entrenamiento
    def preprocess_function(examples):
        inputs = ["translate English to SQL: " + q for q in examples["question"]]
        targets = [sql for sql in examples["sql"]]
        model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

        # Tokenizar los resultados (SQL) también
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
    tokenized_eval_dataset = eval_dataset.map(preprocess_function, batched=True)

    return tokenized_train_dataset, tokenized_eval_dataset, model, tokenizer


#-------------------------------------------------------------------------------------------------------
def entrenar_datasets(tokenized_train_dataset: Dataset, tokenized_eval_dataset: Dataset, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer) -> Tuple[T5ForConditionalGeneration, T5Tokenizer]:

    # Crear argumentos de entrenamiento
    training_args = TrainingArguments(
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

    # Definir el trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_eval_dataset,
        tokenizer=tokenizer,
    )

    # Entrenar el modelo
    trainer.train()

    return model, tokenizer


#-------------------------------------------------------------------------------------------------------
def evaluar_texto(model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, query: str):

    # Función para generar una consulta SQL
    def generate_sql(query):
        inputs = tokenizer("translate English to SQL: " + query, return_tensors="pt", max_length=128, truncation=True)
        outputs = model.generate(inputs["input_ids"], max_length=150)
        sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return sql_query

    # Probar con una nueva pregunta
    generated_sql = generate_sql(query)
    print("Consulta en leng natural: ", query)
    print("Consulta SQL generada: ", generated_sql)


#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

path = "/home/julian/workspaces/prueba-python/ML/"

# #Cargo dataset example de Spider
# dataset = carga_spider_dataset(path + "spider_data")

# #Preparo datasets y modelo
# tokenized_train_dataset, tokenized_eval_dataset, model, tokenizer = preparar_dataset_train_eval(dataset)

# #Entreno el modelo
# model, tokenizer = entrenar_datasets(tokenized_train_dataset, tokenized_eval_dataset, model, tokenizer)

# model.save_pretrained(path + "Models/modelo_T5")
# tokenizer.save_pretrained(path + "Models/tokens_T5")

model = T5ForConditionalGeneration.from_pretrained(path + "Models/T5-base/modelo_T5")
tokenizer = T5Tokenizer.from_pretrained(path + "Models/T5-base/tokens_T5")

# Probar con varias preguntas
queries = [
    "List the name, born state and age of the heads of departments ordered by age.",
    "List the names of all actors.",
    "Show the movies released after 2010.",
    "Find the average salary of employees.",
    "List the names of all actors order by age",
]

for query in queries:
    evaluar_texto(model, tokenizer, query)
