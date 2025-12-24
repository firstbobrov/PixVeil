import os

def clean_temp(target="all"):
    """Очищает папку ../Temp"""
    temp = "../Temp"
    
    if not os.path.exists(temp):
        return print("Папка Temp не найдена")
    
    if target == "all":
        for f in os.listdir(temp):
            p = os.path.join(temp, f)
            if os.path.isfile(p):
                os.remove(p)
        print("Все файлы удалены")
    else:
        p = os.path.join(temp, target)
        if os.path.exists(p):
            os.remove(p)
            print(f"Файл {target} удален")
        else:
            print(f"Файл {target} не найден")

#clean_temp("test.png")  # Удалить test.png
#clean_temp("all")       # Удалить всё

clean_temp("all")
