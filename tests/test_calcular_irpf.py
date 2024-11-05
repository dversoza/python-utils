import pytest
from unittest.mock import patch, MagicMock
import json
from services.calcular_irpf import (
    get_tabela_irpf, calcular_irpf, calculate_deduction, calculate_irpf_acumulado
)

@pytest.fixture
def mock_irpf_data():
    """Provides mock IRPF data for testing."""
    return {
        "vaDeducSimpMe": [500] * 12,
        "gpFaixasTblProg": [
            {"vaAjLimiteMe": [1903.98] * 12, "peFaixa": 7.5},
            {"vaAjLimiteMe": [2826.65] * 12, "peFaixa": 15.0},
            {"vaAjLimiteMe": [3751.05] * 12, "peFaixa": 22.5},
            {"vaAjLimiteMe": [4664.68] * 12, "peFaixa": 27.5},
        ]
    }

@patch('services.calcular_irpf.urllib.request.urlopen')
def test_get_tabela_irpf(mock_urlopen, mock_irpf_data):
    # Mock the context manager behavior of urlopen
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_irpf_data).encode('utf-8')
    mock_urlopen.return_value.__enter__.return_value = mock_response

    tabela = get_tabela_irpf(2024)
    assert tabela == mock_irpf_data

def test_calculate_deduction(mock_irpf_data):
    assert calculate_deduction(mock_irpf_data, 1) == 500
    assert calculate_deduction(mock_irpf_data, 6) == 500

def test_calculate_irpf_acumulado(mock_irpf_data):
    faixas = mock_irpf_data["gpFaixasTblProg"]
    base_calculo = 5000
    month = 11
    irpf_acumulado = calculate_irpf_acumulado(faixas, base_calculo, month)
    assert irpf_acumulado == pytest.approx(505.64, rel=1e-2) # 505.64

@patch('services.calcular_irpf.get_tabela_irpf')
def test_calcular_irpf(mock_get_tabela, mock_irpf_data):
    mock_get_tabela.return_value = mock_irpf_data
    year = 2024
    month = 11
    valor_bruto = 10000
    resultado = calcular_irpf(year, month, valor_bruto)

    assert resultado["year"] == year
    assert resultado["month"] == month
    assert resultado["valor_bruto"] == valor_bruto
    assert resultado["deducao_simplificada_mensal"] == 500
    assert resultado["irpf"] == pytest.approx(1743.14, rel=1e-2)
    assert resultado["valor_liquido"] == pytest.approx(8256.8, rel=1e-2)


def test_calculate_deduction_edge_case():
    tabela = {"vaDeducSimpMe": [0] * 12}  # No deduction available
    assert calculate_deduction(tabela, 1) == 0

def test_calculate_irpf_acumulado_edge_case(mock_irpf_data):
    faixas = mock_irpf_data["gpFaixasTblProg"]
    base_calculo = 1000  # Below the lowest limit
    month = 11
    irpf_acumulado = calculate_irpf_acumulado(faixas, base_calculo, month)
    assert irpf_acumulado == pytest.approx(0, abs=1e-2)
