import json
import urllib.request
import logging
from datetime import datetime

TABELA_IRPF_BASE_URL = "https://www27.receita.fazenda.gov.br/api/simulador/tabela/"
MIN_START_YEAR = 2015
MAX_START_YEAR = datetime.now().year

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

def get_tabela_irpf(year) -> dict:
    """Fetches the IRPF table for a given year from the Receita Federal API."""
    if not (MIN_START_YEAR <= year <= MAX_START_YEAR):
        raise ValueError(f"Ano deve estar entre {MIN_START_YEAR} e {MAX_START_YEAR}")

    url = f"{TABELA_IRPF_BASE_URL}{year}"
    with urllib.request.urlopen(url) as response:
        tabela = json.loads(response.read())
        logging.debug(f"Fetched IRPF table for year {year}: {tabela}")
        return tabela

def calculate_deduction(tabela, month) -> float:
    """Retrieves the simplified monthly deduction for the given month."""
    deducao = tabela.get("vaDeducSimpMe", [0] * 12)[month - 1]
    logging.debug(f"Simplified deduction for month {month}: {deducao}")
    return deducao

def calculate_irpf_acumulado(faixas, base_calculo, month) -> float:
    """Calculates the accumulated IRPF based on income brackets (faixas)."""
    irpf_acumulado = 0
    for idx, faixa in enumerate(faixas):
        limite_atual = faixa["vaAjLimiteMe"][month - 1]
        aliquota = faixa["peFaixa"] / 100
        limite_proxima = faixas[idx + 1]["vaAjLimiteMe"][month - 1] if idx + 1 < len(faixas) else base_calculo

        faixa_valor = max(0, min(base_calculo, limite_proxima) - limite_atual)
        irpf_faixa = faixa_valor * aliquota
        irpf_acumulado += irpf_faixa
        logging.debug(f"Bracket {idx + 1}: faixa_valor={faixa_valor}, aliquota={aliquota}, irpf_faixa={irpf_faixa}")

    return round(irpf_acumulado, 2)

def calcular_irpf(year, month, valor_bruto) -> dict:
    """Calculates the IRPF based on the year, month, and gross value (valor_bruto)."""
    tabela = get_tabela_irpf(year)
    deducao_simplificada = calculate_deduction(tabela, month)
    base_calculo = valor_bruto - deducao_simplificada
    irpf_acumulado = calculate_irpf_acumulado(tabela["gpFaixasTblProg"], base_calculo, month)
    valor_liquido = round(valor_bruto - irpf_acumulado, 2)

    logging.debug(f"Year: {year}, Month: {month}, Valor Bruto: {valor_bruto}, "
                  f"Dedução Simplificada: {deducao_simplificada}, Base de Cálculo: {base_calculo}, "
                  f"IRPF Acumulado: {irpf_acumulado}, Valor Líquido: {valor_liquido}")

    return {
        "year": year,
        "month": month,
        "valor_bruto": valor_bruto,
        "deducao_simplificada_mensal": deducao_simplificada,
        "irpf": irpf_acumulado,
        "valor_liquido": valor_liquido
    }

if __name__ == "__main__":
    year = 2024
    month = 11
    valor_bruto = 10000
    resultado = calcular_irpf(year, month, valor_bruto)
    print(resultado)
