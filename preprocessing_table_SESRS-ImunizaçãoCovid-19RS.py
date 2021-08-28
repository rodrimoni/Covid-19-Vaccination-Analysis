# Preprocessing of file 'SESRS - Imunização Covid-19RS.csv' from https://vacina.saude.rs.gov.br/

# main

try:
    with open("antes.csv","r+", encoding="utf8") as inp:
        with open('depois.csv','w+', encoding="utf8") as out:
            # first line
            fLine = 'crs,codigo_municipio,nome_municipio,doses_destinadas,doses_aplicadas,primeira_dose,segunda_dose,dose_unica,nao_residentes,populacao_geral,pelo_menos_uma_dose,esquema_vacinal_completo\n'
            inp.readline() # removes the first line
            out.write(fLine)

            # read all lines
            lines = inp.readlines()
            cont = 0
            for x in lines:
                x = x.replace('"','')                
                x = x.replace('(',',')
                x = x.replace(')','')
                x = x.replace('%',',')                    
                x = x.replace(' - ',',', 1)
                x = x.replace(' ','')
                if cont == len(lines): # last line without \n
                    x = x.replace('\n','')
                dataLine = x.split(',')
                
                for i in range(len(dataLine)):
                    if i >= 1 and i<=5 or i>=9 and i<=12 or i==16 or i==19:
                        out.write(dataLine[i]+',')
                    elif i == 22:
                        out.write(dataLine[i])
                
                cont = cont + 1
except IOError:
    print("Arquivo não pode ser aberto para leitura.")
