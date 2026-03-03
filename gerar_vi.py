import ncorpos_vi as nvi
import json

arquivo = "valores_iniciais/amortecido_teste3.json"

gvi = nvi.Gerador(N=200, modo="sorteio_aarseth_modificado", eps=0.05)
gvi.gerar()
gvi.condicionar()

infos = {
  'G': gvi.G,
  'amortecedor': gvi.eps,
  'valores_iniciais': {
    'massas': gvi.massas.tolist(),
    'posicoes': gvi.posicoes.tolist(),
    'momentos': gvi.momentos.tolist()
  }
}

with open(arquivo, 'w') as arq:
  json.dump(infos, arq, indent=2)