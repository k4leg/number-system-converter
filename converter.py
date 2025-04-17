def convert_base(number, from_base, to_base):
    is_negative = number.startswith('-')
    if is_negative:
        number = number[1:]  # Удаляем знак минус для обработки

    if '.' in number:
        integer_part, fractional_part = number.split('.')
    else:
        integer_part, fractional_part = number, '0'

    # Проверка длины числа
    if len(integer_part) > 64:
        raise ValueError("Число превышает допустимую длину в 64 двоичных разряда.")

    # Конвертация целой части
    decimal_integer = int(integer_part, from_base)
    converted_integer = int_to_base(decimal_integer, to_base)

    # Конвертация дробной части
    if fractional_part != '0':
        decimal_fractional = fractional_to_decimal(fractional_part, from_base)
        converted_fractional = decimal_to_fractional(decimal_fractional, to_base)
        converted_fractional = remove_trailing_zeros(converted_fractional)
        result = f"{converted_integer}.{converted_fractional}"
    else:
        result = converted_integer

    # Возвращаем отрицательное число, если исходное было отрицательным
    if is_negative:
        result = '-' + result

    return result

def int_to_base(number, base):
    if number == 0:
        return '0'
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return ''.join(str(x) for x in digits[::-1])

def fractional_to_decimal(fractional, base):
    decimal = 0
    for i, digit in enumerate(fractional):
        decimal += int(digit, base) / (base ** (i + 1))
    return decimal

def decimal_to_fractional(decimal, base):
    fractional = []
    while len(fractional) < 10:  # Ограничение до 10 знаков для дробной части
        decimal *= base
        digit = int(decimal)
        fractional.append(str(digit))
        decimal -= digit
    return ''.join(fractional)

def remove_trailing_zeros(fractional):
    # Удаляем нули в конце дробной части
    return fractional.rstrip('0')
