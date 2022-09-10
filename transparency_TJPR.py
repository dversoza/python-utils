""" This module is used to get the data from TJPR's transparency portal.
    It uses the requests module to get the data from the portal and the
    csv module to write the data to a csv file.

    The data is organized in three levels: Unidades, Subunidades and Contas.
    Unidades are the main units of the TJPR, such as the 1st, 2nd, 3rd and 4th
    Judicial Circuits. Subunidades are the subunits of the Unidades, such as
    the 1st, 2nd, 3rd and 4th District Courts. Contas are the accounts of the
    Subunidades, such as the 1st, 2nd, 3rd and 4th District Court's accounts.

    The data is organized in a list of dictionaries, where each dictionary
    represents a row of the csv file. The keys of the dictionaries are the
    column names of the csv file.

    Example:
        $ python3 transparency_TJPR.py

    Attributes:
        __author__ = "Daniel Versoza Alves"
        __email__ = "daniel@versoza.dev"
        __version__ = "1.0.0"
        __status__ = "Development"
        __date__ = "2021/10/06"
"""

import requests
import csv

BASE_URL = "https://extrajudicial.tjpr.jus.br/informacoes-das-unidades-extrajudiciais"
MENSAGEM_DE_CONFIRMAÇÃO = (
    "Gostaria de informações detalhadas a respeito de cada lançamento extraído? (s/N)\n"
)


def get_unidades():
    payload = {
        "p_p_id": "prestacaocontasunidade_WAR_PrestacaoContasUnidade",
        "p_p_lifecycle": "2",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_resource_id": "/unidadeOrganizacionalWS/listarComarcas",
        "p_p_cacheability": "cacheLevelPage",
        "p_p_col_id": "column-3",
        "p_p_col_count": "1",
    }
    unidades = requests.get(BASE_URL, payload).json()["output"]["entity"]
    return [
        {
            "unidade_id": unidade["id"],
            "unidade_nome": unidade["nomeCompleto"],
            "unidade_nome_oficial": unidade["nomeOficial"],
            "unidade_nome_usual": unidade["nomeUsual"],
            "unidade_sigla": unidade["sigla"],
        }
        for unidade in unidades
    ]


def get_subunidades(unidade):
    payload = {
        "p_p_id": "prestacaocontasunidade_WAR_PrestacaoContasUnidade",
        "p_p_lifecycle": "2",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_resource_id": "/unidadeOrganizacionalWS/listarUnidadesDaComarca",
        "p_p_cacheability": "cacheLevelPage",
        "p_p_col_id": "column-3",
        "p_p_col_count": "1",
    }
    form_data = {
        "_prestacaocontasunidade_WAR_PrestacaoContasUnidade_idComarca": unidade[
            "unidade_id"
        ],
        "_prestacaocontasunidade_WAR_PrestacaoContasUnidade_tipo": "EXTRAJUDICIAL",
    }
    r = requests.post(BASE_URL, params=payload, data=form_data)
    subunidades = r.json()["output"]["entity"]
    return [
        {
            "unidade_id": unidade["unidade_id"],
            "subunidade_id": subunidade["id"],
            "subunidade_nome": subunidade["nomeCompleto"],
            "subunidade_nome_oficial": subunidade["nomeOficial"],
            "subunidade_nome_usual": subunidade["nomeUsual"],
            "subunidade_sigla": subunidade["sigla"],
        }
        for subunidade in subunidades
    ]


def get_contas_subunidade(subunidade):
    params = {
        "p_p_id": "prestacaocontasunidade_WAR_PrestacaoContasUnidade",
        "p_p_lifecycle": "2",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_resource_id": "/unidadeOrganizacionalWS/listarPrestacaoDeContasDaUnidade",
        "p_p_cacheability": "cacheLevelPage",
        "p_p_col_id": "column-3",
        "p_p_col_count": "1",
        "detalheID": subunidade["subunidade_id"],
    }
    form_data = {
        "_prestacaocontasunidade_WAR_PrestacaoContasUnidade_idComarca": subunidade[
            "unidade_id"
        ],
        "_prestacaocontasunidade_WAR_PrestacaoContasUnidade_tipo": "EXTRAJUDICIAL",
    }
    r = requests.post(BASE_URL, params=params, data=form_data)
    contas = r.json()["output"]["entity"]
    return [
        {
            "unidade_id": subunidade["unidade_id"],
            "subunidade_id": subunidade["subunidade_id"],
            "conta_id": conta.get("id"),
            "mes": conta.get("referenciaMes"),
            "ano": conta.get("referenciaAno"),
            "receita_bruta": conta.get("valorReceitaTotal"),
            "receita_liquida": conta.get("valorReceitaTotalLiquida"),
            "outras_receitas": conta.get("valorOutrasReceitas"),
            "despesa_bruta": conta.get("valorDespesaTotal"),
            "subsidio": conta.get("valorSubsidioTotal"),
            "saldo": conta.get("saldo"),
        }
        for conta in contas
    ]


def unidades_to_csv(unidades):
    with open("unidades.csv", "w", encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "unidade_id",
            "unidade_nome",
            "unidade_nome_oficial",
            "unidade_nome_usual",
            "unidade_sigla",
        ]
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for unidade in unidades:
            print(unidade["unidade_nome"])
            writer.writerow(unidade)


def subunidades_to_csv(subunidades):
    with open("subunidades.csv", "w", encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "unidade_id",
            "subunidade_id",
            "subunidade_nome",
            "subunidade_nome_oficial",
            "subunidade_nome_usual",
            "subunidade_sigla",
        ]
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for subunidade in subunidades:
            print(subunidade["subunidade_nome"])
            writer.writerow(subunidade)


def contas_to_csv(contas):
    with open("contas.csv", "w", encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "unidade_id",
            "subunidade_id",
            "conta_id",
            "mes",
            "ano",
            "receita_bruta",
            "receita_liquida",
            "outras_receitas",
            "despesa_bruta",
            "subsidio",
            "saldo",
        ]
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for conta in contas:
            print(conta["mes"], conta["ano"], conta["receita_bruta"])
            writer.writerow(conta)


def simple_main():
    unidades = get_unidades()
    unidades_to_csv(unidades)
    subunidades = []
    for unidade in unidades:
        subunidades.extend(get_subunidades(unidade))
    subunidades_to_csv(subunidades)
    contas = []
    for subunidade in subunidades:
        contas.extend(get_contas_subunidade(subunidade))
    contas_to_csv(contas)


def detailed_main():
    unidades = get_unidades()
    with open("unidades.csv", "w", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["unidade_id", "unidade_nome"],
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(unidades)

    for unidade in unidades:
        print(unidade["unidade_id"], unidade["unidade_nome"])
        subunidades = get_subunidades(unidade["unidade_id"])
        with open("subunidades.csv", "a") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["unidade_id", "subunidade_id", "subunidade_nome"],
                delimiter=";",
                quotechar='"',
                quoting=csv.QUOTE_ALL,
                lineterminator="\n",
            )
            writer.writerows(subunidades)

        for subunidade in subunidades:
            print("\t", subunidade["subunidade_id"], subunidade["subunidade_nome"])
            contas = get_contas_subunidade(subunidade)
            with open("contas.csv", "a") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "unidade_id",
                        "subunidade_id",
                        "conta_id",
                        "mes",
                        "ano",
                        "receita_bruta",
                        "receita_liquida",
                        "outras_receitas",
                        "despesa_bruta",
                        "subsidio",
                        "saldo",
                    ],
                    delimiter=";",
                    quotechar='"',
                    quoting=csv.QUOTE_ALL,
                    lineterminator="\n",
                )
                writer.writerows(contas)


if __name__ == "__main__":
    r = input(MENSAGEM_DE_CONFIRMAÇÃO)
    if r.upper() == "S":
        detailed_main()
    else:
        simple_main()
    print("Fim")
    input()
    exit()
