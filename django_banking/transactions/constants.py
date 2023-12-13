DEPOSIT = 1
WITHDRAWAL = 2
INTEREST = 3
AQUISICAO = 4
RESGATE = 5
FUNDOS = 6
ACOES = 7
TITULOS_PUBLICOS = 8
CRIPTO = 9

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, 'Aquisição'),
    (WITHDRAWAL, 'Resgate'),
    (INTEREST, 'Interest'),
)

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, 'Aquisição'),
    (WITHDRAWAL, 'Resgate'),
    (INTEREST, 'Interest'),
)

OPERATION_TYPE_CHOICES = (
    (AQUISICAO, 'Aquisição'),
    (RESGATE, 'Resgate')
)

TIPOS_ATIVOS = (
    (FUNDOS, 'Fundos'),
    (ACOES, 'Ações'),
    (TITULOS_PUBLICOS, 'Títulos Públicos'),
    (CRIPTO, 'Criptomoedas')
)