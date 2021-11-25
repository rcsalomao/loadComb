import itertools


class DeadLoad(object):
    gammaG = {
        'separado': {
            'normal': {
                'peso próprio estrutura metálica': 1.25,
                'peso próprio estrutura pré-moldada': 1.30,
                'peso próprio estrutura moldada no local': 1.35,
                'elementos construtivos industrializados': 1.35,
                'elementos construtivos industrializados com adições in loco': 1.40,
                'elementos construtivos em geral e equipamentos': 1.50,
                'efeitos de recalques de apoio': 1.2,
                'efeitos de retração dos materiais': 1.2
            },
            'especial': {
                'peso próprio estrutura metálica': 1.15,
                'peso próprio estrutura pré-moldada': 1.20,
                'peso próprio estrutura moldada no local': 1.25,
                'elementos construtivos industrializados': 1.25,
                'elementos construtivos industrializados com adições in loco': 1.30,
                'elementos construtivos em geral e equipamentos': 1.40,
                'efeitos de recalques de apoio': 1.2,
                'efeitos de retração dos materiais': 1.2
            },
            'excepcional': {
                'peso próprio estrutura metálica': 1.10,
                'peso próprio estrutura pré-moldada': 1.15,
                'peso próprio estrutura moldada no local': 1.15,
                'elementos construtivos industrializados': 1.15,
                'elementos construtivos industrializados com adições in loco': 1.20,
                'elementos construtivos em geral e equipamentos': 1.30,
                'efeitos de recalques de apoio': 0.0,
                'efeitos de retração dos materiais': 0.0
            }
        },
        'agrupado': {
            'normal': {
                'grandes pontes': 1.30,
                'edificações tipo 1': 1.35,
                'edificações tipo 2': 1.40,
                'efeitos de recalques de apoio': 1.2,
                'efeitos de retração dos materiais': 1.2
            },
            'especial': {
                'grandes pontes': 1.20,
                'edificações tipo 1': 1.25,
                'edificações tipo 2': 1.30,
                'efeitos de recalques de apoio': 1.2,
                'efeitos de retração dos materiais': 1.2
            },
            'excepcional': {
                'grandes pontes': 1.10,
                'edificações tipo 1': 1.15,
                'edificações tipo 2': 1.20,
                'efeitos de recalques de apoio': 0.0,
                'efeitos de retração dos materiais': 0.0
            }
        }
    }

    def __init__(self, loadType, value, separatedOrNot='separado'):
        self.loadType = loadType
        self.separatedOrNot = separatedOrNot
        self.value = value

    def getGamma(self, combinationType, favorable=False):
        if favorable and (self.loadType in ['efeitos de recalques de apoio', 'efeitos de retração dos materiais']):
            return 0.0
        elif favorable and not (self.loadType in ['efeitos de recalques de apoio', 'efeitos de retração dos materiais']):
            return 1.0
        else:
            return self.gammaG[self.separatedOrNot][combinationType][self.loadType]


class LiveLoad(object):
    gammaQ = {
        'separado': {
            'normal': {
                'ações truncadas': 1.2,
                'temperatura': 1.2,
                'vento': 1.4,
                'ações variáveis em geral': 1.5,
            },
            'especial': {
                'ações truncadas': 1.1,
                'temperatura': 1.0,
                'vento': 1.2,
                'ações variáveis em geral': 1.3,
            },
            'excepcional': {
                'ações variáveis em geral': 1.0,
            }
        },
        'agrupado': {
            'normal': {
                'pontes e edificações tipo 1': 1.5,
                'edificações tipo 2': 1.4
            },
            'especial': {
                'pontes e edificações tipo 1': 1.3,
                'edificações tipo 2': 1.2
            },
            'excepcional': {
                'estruturas em geral': 1.0,
            }
        }
    }

    phi0 = {
        'edificações de acesso restrito': 0.5,
        'edificações de acesso público': 0.7,
        'bibliotecas,arquivos,depósitos,oficinas e garagens': 0.8,
        'vento': 0.6,
        'temperatura': 0.6,
        'passarelas de pedestres': 0.6,
        'pontes rodoviárias': 0.7,
        'pontes ferroviárias não especializadas': 0.8,
        'pontes ferroviárias especializadas': 1.0,
        'vigas de rolamentos de pontes rolantes': 1.0
    }

    phi1 = {
        'edificações de acesso restrito': 0.4,
        'edificações de acesso público': 0.6,
        'bibliotecas,arquivos,depósitos,oficinas e garagens': 0.7,
        'vento': 0.3,
        'temperatura': 0.5,
        'passarelas de pedestres': 0.4,
        'pontes rodoviárias': 0.5,
        'pontes ferroviárias não especializadas': 0.7,
        'pontes ferroviárias especializadas': 1.0,
        'vigas de rolamentos de pontes rolantes': 0.8
    }

    phi2 = {
        'edificações de acesso restrito': 0.3,
        'edificações de acesso público': 0.4,
        'bibliotecas,arquivos,depósitos,oficinas e garagens': 0.6,
        'vento': 0.0,
        'temperatura': 0.3,
        'passarelas de pedestres': 0.3,
        'pontes rodoviárias': 0.3,
        'pontes ferroviárias não especializadas': 0.5,
        'pontes ferroviárias especializadas': 0.6,
        'vigas de rolamentos de pontes rolantes': 0.5
    }

    def __init__(self, gammaLoadType, phiLoadType, value, separatedOrNot='separado', shortDuration=False, earthquake=False, fire=False):
        self.gammaLoadType = gammaLoadType
        self.phiLoadType = phiLoadType
        self.value = value
        self.separatedOrNot = separatedOrNot
        self.shortDuration = shortDuration
        self.earthquake = earthquake
        self.fire = fire
        assert((earthquake+fire) < 2)
        if (earthquake or fire):
            assert(shortDuration)

    def getGamma(self, combinationType, favorable=False):
        if favorable:
            return 0.0
        else:
            return self.gammaQ[self.separatedOrNot][combinationType][self.gammaLoadType]

    def getPhi0(self, combinationType, mainLoad):
        if combinationType == 'especial' and mainLoad.shortDuration:
            return self.phi2[self.phiLoadType]
        elif combinationType == 'excepcional' and mainLoad.shortDuration:
            if mainLoad.earthquake:
                return 0.0
            elif mainLoad.fire:
                return 0.7 * self.phi2[self.phiLoadType]
            else:
                return self.phi2[self.phiLoadType]
        else:
            return self.phi0[self.phiLoadType]

    def getPhi1(self, favorable=False):
        if favorable:
            return 0.0
        else:
            return self.phi1[self.phiLoadType]

    def getPhi2(self, favorable=False):
        if favorable:
            return 0.0
        else:
            return self.phi2[self.phiLoadType]


def appendCombo(out, ll, nLLV, tol):
    res = True
    for o in out:
        residue = 0.0
        for v in range(nLLV):
            residue += abs(o[v]-ll[v])
        if residue < tol:
            res = False
    return res


def checkSeparatedOrNotLoadVector(loadVector):
    firstLoad = loadVector[0]
    for load in loadVector:
        assert(firstLoad.separatedOrNot == load.separatedOrNot)


def generateDeadLoadUltimaCombo(deadLoadVector, combinationType):
    assert(combinationType in ['normal', 'especial', 'excepcional'])
    nDLV = len(deadLoadVector)
    combosFavUnfav = list(itertools.product([True, False], repeat=nDLV))
    out = []
    for i in range(len(combosFavUnfav)):
        dl = []
        for j in range(nDLV):
            dl.append(deadLoadVector[j].getGamma(combinationType, combosFavUnfav[i][j]) * deadLoadVector[j].value)
        out.append(dl)
    return out


def generateLiveLoadUltimaCombo(liveLoadVector, combinationType, tol=1e-8):
    assert(combinationType in ['normal', 'especial', 'excepcional'])
    nLLV = len(liveLoadVector)
    combosFavUnfav = list(itertools.product([True, False], repeat=(nLLV)))
    out = []
    for i in range(len(combosFavUnfav)):
        for k in range(nLLV):
            ll = []
            for j in range(nLLV):
                ll.append(liveLoadVector[j].getGamma(combinationType, combosFavUnfav[i][j]) * liveLoadVector[j].getPhi0(combinationType, liveLoadVector[k]) * liveLoadVector[j].value)
            ll[k] = liveLoadVector[k].getGamma(combinationType, combosFavUnfav[i][k])*liveLoadVector[k].value
            if appendCombo(out, ll, nLLV, tol):
                out.append(ll)
    return out


def generateUltimaCombo(deadLoadVector=None, liveLoadVector=None, combinationType='normal', tol=1e-8):
    if deadLoadVector is not None:
        checkSeparatedOrNotLoadVector(deadLoadVector)
    if liveLoadVector is not None:
        checkSeparatedOrNotLoadVector(liveLoadVector)
        if (deadLoadVector is not None) and (liveLoadVector[0].separatedOrNot == 'agrupado'):
            assert(deadLoadVector[0].separatedOrNot == 'agrupado')

    out = []
    if (deadLoadVector is not None) and (liveLoadVector is None):
        dlUltimaCombo = generateDeadLoadUltimaCombo(deadLoadVector, combinationType)
        for dl in dlUltimaCombo:
            out.append((dl,))
    elif (deadLoadVector is None) and (liveLoadVector is not None):
        llUltimaCombo = generateLiveLoadUltimaCombo(liveLoadVector, combinationType, tol)
        for ll in llUltimaCombo:
            out.append((ll,))
    elif (deadLoadVector is None) and (liveLoadVector is None):
        print("Não há carregamentos para processar :c")
        exit(2)
    else:
        dlUltimaCombo = generateDeadLoadUltimaCombo(deadLoadVector, combinationType)
        llUltimaCombo = generateLiveLoadUltimaCombo(liveLoadVector, combinationType, tol)
        for dl in dlUltimaCombo:
            for ll in llUltimaCombo:
                out.append((dl, ll))

    return out


def generateDeadLoadServiceCombo(deadLoadVector):
    out = []
    for dl in deadLoadVector:
        out.append(dl.value)
    return out


def generateLiveLoadServiceCombo(liveLoadVector, combinationType, tol=1e-8):
    assert(combinationType in ['quase permanente', 'frequente', 'raro'])
    nLLV = len(liveLoadVector)
    combosFavUnfav = list(itertools.product([True, False], repeat=(nLLV)))
    out = []
    if combinationType == 'quase permanente':
        for i in range(len(combosFavUnfav)):
            ll = []
            for j in range(nLLV):
                ll.append(liveLoadVector[j].getPhi2(combosFavUnfav[i][j]) * liveLoadVector[j].value)
            if appendCombo(out, ll, nLLV, tol):
                out.append(ll)
    elif combinationType == 'frequente':
        for i in range(len(combosFavUnfav)):
            for k in range(nLLV):
                ll = []
                for j in range(nLLV):
                    ll.append(liveLoadVector[j].getPhi2(combosFavUnfav[i][j]) * liveLoadVector[j].value)
                ll[k] = liveLoadVector[k].getPhi1(combosFavUnfav[i][k]) * liveLoadVector[k].value
                if appendCombo(out, ll, nLLV, tol):
                    out.append(ll)
    elif combinationType == 'raro':
        for i in range(len(combosFavUnfav)):
            for k in range(nLLV):
                ll = []
                for j in range(nLLV):
                    ll.append(liveLoadVector[j].getPhi1(combosFavUnfav[i][j]) * liveLoadVector[j].value)
                ll[k] = liveLoadVector[k].value if combosFavUnfav[i][k] else 0.0
                if appendCombo(out, ll, nLLV, tol):
                    out.append(ll)
    return out


def generateServiceCombo(deadLoadVector=None, liveLoadVector=None, combinationType='frequente', tol=1e-8):
    if deadLoadVector is not None:
        checkSeparatedOrNotLoadVector(deadLoadVector)
    if liveLoadVector is not None:
        checkSeparatedOrNotLoadVector(liveLoadVector)
        if (deadLoadVector is not None) and (liveLoadVector[0].separatedOrNot == 'agrupado'):
            assert(deadLoadVector[0].separatedOrNot == 'agrupado')

    out = []
    if (deadLoadVector is not None) and (liveLoadVector is None):
        dlServiceCombo = generateDeadLoadServiceCombo(deadLoadVector)
        out.append((dlServiceCombo,))
    elif (deadLoadVector is None) and (liveLoadVector is not None):
        llServiceCombo = generateLiveLoadServiceCombo(liveLoadVector, combinationType, tol)
        for ll in llServiceCombo:
            out.append((ll,))
    elif (deadLoadVector is None) and (liveLoadVector is None):
        print("Não há carregamentos para processar :c")
        exit(2)
    else:
        dlServiceCombo = generateDeadLoadServiceCombo(deadLoadVector)
        llServiceCombo = generateLiveLoadServiceCombo(liveLoadVector, combinationType, tol)
        for ll in llServiceCombo:
            out.append((dlServiceCombo, ll))

    return out


if __name__ == "__main__":
    cargasPermanentes = [DeadLoad('elementos construtivos industrializados com adições in loco', 100),
                         DeadLoad('elementos construtivos industrializados com adições in loco', 200),
                         DeadLoad('elementos construtivos industrializados com adições in loco', 300)]
    cargasVariáveis = [LiveLoad('ações variáveis em geral', 'edificações de acesso restrito', 10),
                       LiveLoad('ações variáveis em geral', 'edificações de acesso público', 20),
                       LiveLoad('vento', 'vento', 15)]

    # bla = generateDeadLoadUltimaCombo(cargasPermanentes, 'normal')
    # bla = generateLiveLoadUltimaCombo(cargasVariáveis, 'normal')
    # bla = generateUltimaCombo(cargasPermanentes)
    # bla = generateUltimaCombo(None, cargasVariáveis)
    # bla = generateUltimaCombo(cargasPermanentes, cargasVariáveis)

    # bla = generateDeadLoadServiceCombo(cargasPermanentes)
    # bla = generateLiveLoadServiceCombo(cargasVariáveis, 'frequente')
    # bla = generateServiceCombo(cargasPermanentes)
    # bla = generateServiceCombo(None, cargasVariáveis)
    bla = generateServiceCombo(cargasPermanentes, cargasVariáveis)

    for b in bla:
        print(b)

    print(len(bla))
