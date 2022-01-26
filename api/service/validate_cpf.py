def validate_cpf(cpf):
    cpf_length = 11
    if len(cpf) != cpf_length:
        return False

    if cpf in (char * cpf_length for char in "1234567890"):
        return False

    cpf_reverse = cpf[::-1]

    for i in range(2, 0, -1):
        cpf_enumerate = enumerate(cpf_reverse[i:], start=2)
        dv_calculado = sum(map(lambda el: int(el[1]) * el[0], cpf_enumerate)) * 10 % 11
        if cpf_reverse[i - 1 : i] != str(dv_calculado % 10):
            return False

    return True
