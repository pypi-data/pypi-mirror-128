def ns_calc_auto():
    sleep(3)
    pyautogui.write(
        "def ns_calc(number=0, base_number_system=10, finite_number_system=10):\n"
        "try:\n"
        "alphabet = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I',\n"
        "19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R',\n"
        "28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}\n"
        "finite_number = ''\n"
        "m = 0\n"
        "for i in range(len(str(number))):\n"
        "m = max(int(str(number)[i]), m)\n\n", interval=0.05)
    pyautogui.press('backspace')
    pyautogui.write(
        "if m >= base_number_system:\n"
        "return '", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "Yt gjl[jlzofz cbcntvf cxbcktybz", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "'\n\nif finite_number_system == 1:\n"
        "return '", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "Yt djpvj;yj gthtdtcnb xbckj d cbcntve cxbcktybz c jcyjdfybtv 1", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "'\n\nif base_number_system > 36 or finite_number_system > 36:\n"
        "return '", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "Vfrcbvfkmyj ljcnegyfz cbcntvf cxbcktybz 36", interval=0.05)
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("shift")
    pyautogui.write(
        "'\n\nnumber = int(str(number), base_number_system)\n"
        "while int(number) > 0:\n"
        "if number % finite_number_system > 9:\n"
        "finite_number = alphabet[number % finite_number_system] + finite_number\n"
        "else:\n"
        "finite_number = str(number % finite_number_system) + finite_number\n", interval=0.05)
    pyautogui.press('backspace')
    pyautogui.write(
        "number //= finite_number_system\n", interval=0.05)
    pyautogui.press('backspace')
    pyautogui.write(
        "return finite_number\n"
        "except Exception as e:\n"
        "return e", interval=0.05)
