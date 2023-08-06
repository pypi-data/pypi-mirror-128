def ns_calc(number=0, base_number_system=10, finite_number_system=10):
    try:
        alphabet = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I',
                    19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R',
                    28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
        finite_number = ''
        m = 0
        for i in range(len(str(number))):
            m = max(int(str(number)[i]), m)

        if m >= base_number_system:
            return 'Неподходящая система счисления'

        if finite_number_system == 1:
            return 'Невозможно перевести число в систему счисления с основанием 1'

        if base_number_system > 36 or finite_number_system > 36:
            return 'Максимально доступная система счисления 36'

        number = int(str(number), base_number_system)
        while int(number) > 0:
            if number % finite_number_system > 9:
                finite_number = alphabet[number % finite_number_system] + finite_number
            else:
                finite_number = str(number % finite_number_system) + finite_number
            number //= finite_number_system
        return finite_number
    except Exception as e:
        return e
