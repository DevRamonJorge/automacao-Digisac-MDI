from datetime import datetime, timedelta

def data_hora_dia_anterior(hora_str="07:00"):
    hoje = datetime.now()
    
    dia_anterior = hoje - timedelta(days=1)

    hora, minuto = map(int, hora_str.split(":"))

    resultado = datetime(
        year=dia_anterior.year,
        month=dia_anterior.month,
        day=dia_anterior.day,
        hour=hora,
        minute=minuto
    )

    print("Hoje:", hoje.strftime("%d/%m/%Y %H:%M"))
    print("Dia anterior às", hora_str + ":", resultado.strftime("%d/%m/%Y %H:%M"))

data_hora_dia_anterior()
