from langchain_community.llms.ollama import Ollama

def to_precise_model(model: Ollama) -> Ollama:
    model.top_k = 0
    model.top_p = 0
    model.temperature = 0
    return model


mistral_30B = to_precise_model(Ollama(model="dolphin-mixtral"))
beagle_7B = to_precise_model(Ollama(model="beagle"))
chat_7B = to_precise_model(Ollama(model="neural-chat"))
