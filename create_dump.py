import os 

USER = "cris"

print(f"Creando copia dump con usuario {USER}...")

ans = os.system(f"mysqldump -u {USER} -p model > model_dump.sql")



if(ans == 0):
    print("\n ***Copia de la base de datos generada con éxito***\n")

else:
    print("\n ***Ha ocurrido un error durante la creación de la copia. Revisar usuario y/o contraseña***\n")