# Preprocessing of file 'preprocessing_table_SESRS-VacAplicacao.csv' from https://vacina.saude.rs.gov.br/

# main

inFileName = input("Input file name (CSV): ")
outFileName = input("Output file name (CSV): ")

try:
    with open(inFileName,"r+") as inp:
        with open(outFileName,'w+') as out:
            # first line            
            fLine = "faixaetaria,sexo,dose,cd_municipio,raca_cor,grupo,detalhegrupo,data,tp_vacina\n"
            inp.readline() # removes the first line            
            out.write(fLine)
            
            # read all lines
            lines = inp.readlines()
            cont = 0
            print("Processing... Please wait.")
            for x in lines:
                if(cont == int(len(lines)/2)):
                    print("50% complete.")
                elif(cont == int(len(lines)-1)):
                    print("100% complete.")

                #print("Processded line " + str(cont) + " from " + str(len(lines)))
                
                dataLine = x.split(';')
                
                for i in range(len(dataLine)):
                    if i >= 0 and i<=3 or i>=5 and i<=8:
                        out.write(dataLine[i]+',')
                    elif i == 9:
                        out.write(dataLine[i]+'\n')
                    elif i==9 and cont == len(lines):
                        out.write(dataLine[i])
            
                cont = cont + 1
            
except IOError:
    print("Error while opening csv file.")
