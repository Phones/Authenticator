import os
import logging
import locale
from datetime import datetime
from pytz import timezone as TimeZone_

# pylint: disable=invalid-name
def convert_datetime_UTC_to_UTC_3(date):
    """Convert uma data no padrão UTC para UTC-3, o fuso horario horario de brasilia

    Args:
        time (dateime): datetime

    Returns:
        datetime: Retorna a data em datetime conrvertida para o padrão de brasilia
    """
    # Converter para objeto datetime 
    date_utc = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')

    # Adicionar o fuso horário UTC ao objeto datetime
    date_utc = TimeZone_('UTC').localize(date_utc)

    # Converter para fuso horario do brasil
    date_UTC_3 =  date_utc.astimezone(TimeZone_("America/Sao_Paulo"))

    # Converter para string formatada novamente
    return date_UTC_3.strftime("%d-%m-%Y %H:%M:%S %Z%z")

def get_hour_and_date_now():
    """ Retorna a data e hora atual no formato "%d-%m-%Y %H:%M:%S"

    Returns:
        datetime: Retorna no formato datetime
    """
    # Pega a data e hora atual
    date_and_hour_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Retorna a data e hora atual convertida para o fuso horario de brasilia
    return convert_datetime_UTC_to_UTC_3(date_and_hour_now)

def get_date_now():
    # Pega a data e hora atual
    date_and_hour_now = get_hour_and_date_now()

    # Divide a string para pegar apenas a data
    date_and_hour_now = date_and_hour_now.split()

    # Retora apenas a data
    return date_and_hour_now[0]

def get_current_year():
    """
    Retorna o ano atual.
    
    Retorna o ano atual com base na data e hora do sistema.
    
    Returns:
        int: O ano atual.
    """
    return datetime.now().year

def get_current_month_name():
    # Define para o brasil, para que o nome do mes venha em portugues
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    
    # Retorna o mes atual
    return datetime.now().strftime("%B")

def check_folder_exists(folder_path):
    """
        Verifica se uma pasta existe em um diretorio especifico
    
    Args:
        folder_path (str): O caminho para a pasta
        
    Returns:
        bool: True Caso a pasta exista, False Caso a pasta não exista.
    """
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

def create_folder(folder_path):
    """
    Creates a new folder at the specified path.
    
    Args:
        folder_path (str): The path where the folder will be created.
    """
    os.makedirs(folder_path)

def check_create_folder(folder_path):
    """
    Checks if a folder exists and creates it if it doesn't.
    
    Args:
        folder_name (str): The name of the folder to be checked/created.
    """
    if not check_folder_exists(folder_path):
        create_folder(folder_path)

def get_logging_files_path():
    folder_path = "Logs"
    # Pega a data atual para adicionar ao nome do arquivo
    date_now = get_date_now()

    current_year = get_current_year()
    # Verifica se a pasta do ano atual existe e caso nao cria a pasta
    check_create_folder(f"{folder_path}/{current_year}")

    current_month = get_current_month_name()
    # Verifica se a pasta do mes atual existe e caso nao cria a pasta
    check_create_folder(f"{folder_path}/{current_year}/{current_month}")

    # Verifica se a pasta do data atual existe e caso nao cria a pasta
    check_create_folder(f"{folder_path}/{current_year}/{current_month}/{date_now}")

    # Monta o caminho para o arquivo
    logging_file_path = f"{folder_path}/{current_year}/{current_month}/{date_now}/"
    
    info_file_path = f'{logging_file_path}/info_{date_now}.log'
    error_file_path = f'{logging_file_path}/error_{date_now}.log'
    warning_file_path = f'{logging_file_path}/warning_{date_now}.log'

    return info_file_path, error_file_path, warning_file_path


def get_logger(module_name):
    # Configurar o logger principal
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    info_file_path, error_file_path, warning_file_path = get_logging_files_path()

    # Criar um handler para os logs de nível WARNING e superior
    warning_handler = logging.FileHandler(warning_file_path)
    warning_handler.setLevel(logging.WARNING)

    # Criar um handler para os logs de nível ERROR e superior
    error_handler = logging.FileHandler(error_file_path)
    error_handler.setLevel(logging.ERROR)

    # Criar um handler para os logs de nível INFO e superior
    info_handler = logging.FileHandler(info_file_path)
    info_handler.setLevel(logging.INFO)

    # Criar um formatter para os handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Definir o formatter nos handlers
    warning_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    # Adicionar os handlers ao logger
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    return logger
