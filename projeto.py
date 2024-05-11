# NÃO SE ESQUEÇA DE BAIXAR AS 6 IMAGENS DISPONÍVEIS NESSE REPOSITÓRIO 
# E DEIXÁ-LAS NO MESMO DIRETÓRIO DO PROGRAMA
# LEMBRE-SE DE ALTERAR A GOOGLE_API_KEY
# ISSO É NECESSÁRIO PARA O FUNCIONAMENTO DO CÓDIGO

# Importando as bibliotecas
import PIL.Image
import random
import google.generativeai as genai
from IPython.display import display

# Uso da chave de API
GOOGLE_API_KEY="INSIRA_SUA_CHAVE_DE_API_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)

# Parametrização do modelo - configs para a identificação do idioma.
# Para identificar o idioma, não é desejável uma alta criatividade do modelo, por isso:

generation_configIdioma = {
    'candidate_count': 1,
    'temperature':0,
    'top_p': 1,
    'top_k': 1,
}

# Parametrização do modelo - configs para descrever a imagem.
# É desejável uma alta criatividade do modelo, por isso:
generation_configDescricao = {
    'candidate_count':1,
    'temperature':1,
}

# Parâmetros de segurança estão definidos como alto para o programa poder ser usado por todas as idades.
safety_settings ={
    'HARASSMENT': 'BLOCK_ONLY_HIGH',
    'HATE':'BLOCK_ONLY_HIGH',
    'SEXUAL':'BLOCK_ONLY_HIGH',
    'DANGEROUS':'BLOCK_ONLY_HIGH',
}

# Definindo o modelo que vai ser usado para verificar a existência do idioma
modelIdioma = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_configIdioma,
                              safety_settings=safety_settings)

# Definindo o modelo que vai ser usado para descrever a imagem escolhida
modelDescricao = genai.GenerativeModel(model_name="gemini-pro-vision",
                                       generation_config=generation_configDescricao,
                                       safety_settings=safety_settings)

modelComparacao= genai.GenerativeModel(model_name="gemini-1.0-pro",
                                       generation_config=generation_configDescricao,
                                       safety_settings=safety_settings)

# Conjunto de imagens
images = ["imagem1.jpg","imagem2.jpg","imagem3.jpg","imagem4.jpg","imagem5.jpg","imagem6.jpg"]

# checa se o idioma existe, caso exista, ele irá retornar 1, caso contrário, retornará 0
def checaIdioma(text):
  display("Checando se o idioma existe....")
  # Usei o history para dar diretrizes para o modelo
  chatIdioma = modelIdioma.start_chat(history=[])
  response = chatIdioma.send_message( "Responda com sim ou não. Esse idioma " + text + " existe?")

  valida = response.candidates[0].content.parts[0].text
  print(valida)

  if "Sim" in valida:
    return 1
  else:
    return 0

# Pede para o Gemini descrever a imagem no idioma selecionado
def descricaoGemini(idioma,image):
  display("Gerando descrição da imagem, aguarde....")
  prompt = "Em "+ idioma + ", descreva a imagem"
  geminiDescreve = modelDescricao.generate_content([prompt,image])
 
  return geminiDescreve.candidates[0].content.parts[0].text

# Sorteia uma imagem para ser avaliada
def sorteio():
  imgNumber = random.randint(0,5)
  return images[imgNumber]

# Pega o input do user e valida se está ou não no idioma
def descricaoUser(idioma):
  text = input(f"Descreva a imagem em {idioma}\n")
  verifica = modelIdioma.start_chat(history=[])
  
  response = verifica.send_message("Responda com sim ou não. O texto a seguir: "+ text +"\n está em " + idioma +"?") 
    
  if "Sim" in response.candidates[0].content.parts[0].text:
    return text
  else:
    return descricaoUser(idioma)

# Dá sugestões ao usuário de como melhorar a sua escrita
def feedback(textUser, textGemini,idioma):
  display("Comparando as descrições....")
  
  prompt = "Mostre como eu posso melhorar o seguinte texto gramaticalmente e semanticamente em tópicos:\n" + textUser +"\n no contexto da imagem descrita como:" + textGemini +". Gere versões em português e em" + idioma
  feedback = modelComparacao.start_chat(history=[])
  
  response = feedback.send_message(prompt)
  
  return response.candidates[0].content.parts[0].text


# Fluxo principal do programa
def main():
  display("Seja bem-vind@, o presente programa tem como objetivo te ajudar a desenvolver sua fluência em outro idioma através da descrição de imagens.")
  print('---------------------------------------------------------------------------------------------------------------------------------------------')
  
  idioma = input("Qual idioma você deseja escolher?\n")
  num = checaIdioma(idioma)

  while num!=1:
    idioma = input("O idioma não foi encontrado, digite novamente:\n")
    num = checaIdioma(idioma)

  # Sorteiando a imagem
  print("Sorteando a imagem...")
  image_escolhida = sorteio()

  image = PIL.Image.open(image_escolhida)
  image.show()
  
  user_description = descricaoUser(idioma)
  gemini_description = descricaoGemini(idioma,image)
  
  comparacao = feedback(user_description, gemini_description, idioma)
  
  print("-----------------------------------------------------------")
  print(f"\nDescrição da imagem pelo Gemini:\n {gemini_description}\n")
  print("-----------------------------------------------------------")
  print(f"\nPontos a serem melhorados no texto:\n {comparacao}\n")
  print("-----------------------------------------------------------")
  
  repeat = input("Para continuar, digite S.\nSe quiser parar, digite N.\n")
  repeat = repeat.lower()
  
  while repeat != "n" and repeat != "s":
    repeat = input("Para continuar, digite S.\nSe quiser parar, digite N.\n")
    repeat = repeat.lower()
    
  if repeat == "s": main()

main()
