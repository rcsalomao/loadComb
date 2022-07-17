from loadComb import DeadLoad, LiveLoad, generateUltimaCombo, generateServiceCombo


cargasPermanentes = [
    DeadLoad("elementos construtivos industrializados com adições in loco", 100),
    DeadLoad("elementos construtivos industrializados com adições in loco", 200),
    DeadLoad("elementos construtivos industrializados com adições in loco", 300),
]
cargasVariáveis = [
    LiveLoad("ações variáveis em geral", "edificações de acesso restrito", 10),
    LiveLoad("ações variáveis em geral", "edificações de acesso público", 20),
    LiveLoad("vento", "vento", 15),
]

# bla = generateUltimaCombo(cargasPermanentes)
# bla = generateUltimaCombo(None, cargasVariáveis)
# bla = generateUltimaCombo(cargasPermanentes, cargasVariáveis)

# bla = generateServiceCombo(cargasPermanentes)
# bla = generateServiceCombo(None, cargasVariáveis)
bla = generateServiceCombo(cargasPermanentes, cargasVariáveis)

for b in bla:
    print(b)

print(len(bla))
