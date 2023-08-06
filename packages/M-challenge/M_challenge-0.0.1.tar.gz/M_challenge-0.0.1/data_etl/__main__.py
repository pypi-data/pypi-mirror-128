from M_Challenge.stage_data import StageData

print('please input the following information:)')
password = (input('Database password: '))
host = int(input('Host: '))
upload_data = StageData(password, host)
data = upload_data.save_to_database()
print(f"Data extracted, processed and staged!")
