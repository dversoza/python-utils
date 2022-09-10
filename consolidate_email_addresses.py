""" This module parses a folder containing CSV files (i.e. Outlook contacts export),
    and creates a consolidated CSV with all unique email found.

    Attributes:
        __author__ = "Daniel Versoza Alves"
        __email__ = "daniel@versoza.dev"
        __version__ = "1.0.0"
        __status__ = "Production"
        __date__ = "12/03/2021"
"""

import os
import re

CSV_DIR = os.getcwd()


def get_all_csv_files_from_dir(dir: str) -> list:
    """
    Recebe um diretório e retorna todos os arquivos CSV contidos nele.
    """
    return [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.csv')]


def extract_email_addresses_from_text_file(file: str) -> list:
    """
    Recebe um arquivo de texto e retorna uma lista com todos os emails
    contidos no arquivo.
    """
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        return re.findall(r'[\w\.-]+@[\w\.-]+', text)


def remove_duplicates(emails_list: list) -> list:
    """
    Recebe uma lista de emails e retorna uma lista com todos os emails
    sem duplicatas.
    """
    return list(set(emails_list))


def convert_email_address_to_dict(email: str) -> dict:
    """
    Recebe um email e retorna um dicionário com o nome do usuário e
    domínio do email.
    """
    return {
        'email': email,
        'usuário': email.split('@')[0],
        'domínio': email.split('@')[1],
        'empresa': email.split('@')[1].split('.')[0],
        'primeiro_nome': email.split('@')[0].split('.')[0],
        'ultimo_nome': email.split('@')[0].split('.')[-1],
    }


def export_dict_to_csv(emails_dict: list, file: str) -> None:
    """
    Recebe uma lista de emails e um nome de arquivo e exporta os emails
    em um arquivo CSV.
    """
    with open(file, 'w', encoding='utf-8-sig') as f:
        f.write('email;usuário;domínio;empresa;primeiro_nome;ultimo_nome\n')
        for email in emails_dict:
            f.write(f'{email["email"]};{email["usuário"]};{email["domínio"]};{email["empresa"]};{email["primeiro_nome"]};{email["ultimo_nome"]}\n')


def main():
    for csv in get_all_csv_files_from_dir(CSV_DIR):
        emails = extract_email_addresses_from_text_file(csv)
        emails = remove_duplicates(emails)
        emails_dict = [convert_email_address_to_dict(email) for email in emails]
        export_dict_to_csv(emails_dict, os.path.join('.', 'consolidar', f'clean-{csv.split("/")[-1]}'))


if __name__ == '__main__':
    main()
