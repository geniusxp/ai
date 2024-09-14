# 🎫 GeniusXP

![Capa](.github/cover.png)

## 💡 Explicação do projeto
GeniusXP é uma plataforma centralizada para gestão de eventos que simplifica operações como inscrições, pagamentos e check-in, enquanto aumenta o engajamento com enquetes e networking. A inteligência artificial da GeniusXP utiliza as preferências dos usuários para oferecer uma experiência altamente personalizada e otimizar o planejamento. Com análise de sentimento e assistência virtual, a plataforma proporciona interações mais significativas, elevando a eficiência da gestão e tornando os eventos mais impactantes para cada participante.

## 🎥 Pré-visualização do projeto integrado
https://github.com/user-attachments/assets/8e5210e5-ca94-4c4c-a912-92afa935565a


## 🧠 Análise detalhada e clara da arquitetura de IA e sua implementação
A plataforma **GeniusXP** utiliza uma arquitetura de IA voltada para análise de sentimento em mensagens enviadas no chat. Isso é feito em três etapas principais: pré-processamento de texto, transformação e modelagem, e predição de sentimentos, utilizando ferramentas como **SciKit Learn**, **NLTK**, e **Deep Translator** para maximizar a precisão e adaptar a análise ao idioma do usuário.

### 1. **Pré-processamento de Texto**
O pré-processamento de texto é essencial para garantir que os dados estejam estruturados corretamente antes da análise. Utilizamos **NLTK** (Natural Language Toolkit) para realizar tokenização, lematização e remoção de stopwords em inglês, além de outras técnicas de limpeza de texto como a remoção de pontuação, números e HTML. Isso ajuda a eliminar ruídos e padronizar o texto, o que melhora significativamente a performance do modelo.

- **Lematização**: A lematização utiliza o contexto gramatical das palavras para reduzi-las à sua forma base, com o auxílio do `WordNetLemmatizer` e `nltk.pos_tag` para identificar corretamente a função de cada palavra (adjetivo, verbo, substantivo, etc.).

### 2. **Transformação e Modelagem**
Após o pré-processamento, aplicamos o **CountVectorizer** do **SciKit Learn** para converter o texto em uma matriz de contagem de palavras, limitando o vocabulário aos termos mais relevantes. Essa abordagem transforma o conteúdo textual em um formato numérico, adequado para a modelagem preditiva.

O modelo de aprendizado de máquina utilizado é uma **Regressão Logística** ajustada com o conjunto de dados, onde o algoritmo é capaz de classificar as mensagens em diferentes categorias de sentimento (como alegria, tristeza, raiva, etc.), com base no treinamento prévio realizado com um dataset de emoções.

### 3. **Predição de Sentimentos**
Quando uma nova mensagem é enviada no chat, ela passa por uma tradução automática para o inglês utilizando o **Deep Translator**, garantindo que a análise de sentimentos seja consistente independentemente do idioma do usuário. Em seguida, a mensagem traduzida é pré-processada e alimentada no modelo treinado, que faz a predição do sentimento associado.

Esse processo contínuo de análise de sentimento em tempo real ajuda a GeniusXP a identificar as emoções predominantes nos eventos, gerando relatórios que facilitam o ajuste das estratégias de interação e engajamento dos organizadores.

## 👥 Equipe
Este projeto está sendo desenvolvido pelos seguintes membros:

- RM99565 - Erick Nathan Capito Pereira (2TDSPV)
- RM99577 - Guilherme Dias Gomes (2TDSPX)
- RM550841 - Lucas Araujo Oliveira Silva (2TDSPV)
- RM99409 - Michael José Bernardi Da Silva (2TDSPX)

## 💻 Tecnologias
As principais tecnologias, bibliotecas, ecossistemas e frameworks incluídos no projeto são:

- [Python](https://www.python.org)
- [SciKit Learn](https://scikit-learn.org/stable/)
- [Deep Translator](https://pypi.org/project/deep-translator/)
- [The Natural Language Toolkit (NLTK)](https://www.nltk.org)
- [OracleDB extension](https://pypi.org/project/oracledb/)
- [FastAPI](https://fastapi.tiangolo.com)
- [Uvicorn](https://www.uvicorn.org)
