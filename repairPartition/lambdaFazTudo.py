class Event:
    def __init__(self, task_type, db_name, table_name, partition_columns, data_purge_params):
        self.task_type = task_type
        self.db_name = db_name
        self.table_name = table_name
        self.partition_columns = partition_columns
        self.data_purge_params = data_purge_params

def lambda_handler(event, context):
    # Convertendo o evento em um objeto Event
    event_obj = Event(
        event['task_type'], 
        event['db_name'], 
        event['table_name'], 
        event['partition_columns'], 
        event['data_purge_params']
    )

    # Mapeamento de tipos de tarefas para funções
    task_functions = {
        'delete_partitions': delete_partitions,
        'add_partitions': add_partitions,
        'rebuild_partitions': rebuild_partitions,
        'purge_data': purge_data
    }

    # Obtenha a função do dicionário usando o tipo de tarefa
    task_func = task_functions.get(event_obj.task_type)

    # Se a função existe, chame-a com o evento
    if task_func:
        task_func(event_obj)
    else:
        print("Task type not recognized")

# Funções de tarefa fictícias. Você preencheria com seu próprio código.
def delete_partitions(event):
    print(f"Deleting partitions from {event.db_name}.{event.table_name} with columns {event.partition_columns}")
    
def add_partitions(event):
    print(f"Adding partitions to {event.db_name}.{event.table_name} with columns {event.partition_columns}")
    
def rebuild_partitions(event):
    print(f"Rebuilding partitions in {event.db_name}.{event.table_name} with columns {event.partition_columns}")

def purge_data(event):
    print(f"Purging data in {event.db_name}.{event.table_name} with parameters {event.data_purge_params}")