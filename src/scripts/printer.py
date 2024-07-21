def printAndReadPlateNum(maxValue):
    print('Digite o numero da placa a ser feito o ORC')
    print('- Placa disponiveis: 1 -', maxValue)
    print('- Digite 0 para calcular a media de todas as placas')
    option = input('> ')
    return option

def printPlateResult(original, result, precision):
    print('\n----------------------------------\n')
    print('Valor experado: ', original)
    print('Valor obtido: ', result)
    print('Precisao: ', precision)

def printPlateAveragePrecision(precision):
    print('\nPrecisao media geral: ', precision)