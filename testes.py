from datetime import datetime, timedelta

def datas_dia_anterior(hora1="07:00", hora2="22:00"):
    hoje = datetime.now()
    dia_anterior = hoje - timedelta(days=1)

    # Extrai hora e minuto da primeira hora
    h1, m1 = map(int, hora1.split(":"))
    # Extrai hora e minuto da segunda hora
    h2, m2 = map(int, hora2.split(":"))

    data_hora1 = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=h1,
        minute=m1
    )

    data_hora2 = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=h2,
        minute=m2
    )

    return data_hora1.strftime("%d/%m/%Y %H:%M"), data_hora2.strftime("%d/%m/%Y %H:%M")

# Uso:
primeira_data_07, segunda_data_22 = datas_dia_anterior()
print("Primeira data:", primeira_data_07)  # Ex: 27/05/2025 07:00
print("Segunda data:", segunda_data_22)    # Ex: 27/05/2025 22:00
