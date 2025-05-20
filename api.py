from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from chains.qa_chain import build_sql_chain
from db.redis_cache import get_cached_answer, set_cached_answer
from config.logging import logger

app = FastAPI(title="LLM Q&A API", version="1.0")
chain = build_sql_chain()

API_KEY = "my-secret-key"  # mejor en .env

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_llm(request: QueryRequest, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Pregunta vacía")

    cached = get_cached_answer(question)
    if cached:
        logger.info("Respuesta obtenida de cache")
        return {"question": question, "answer": cached.decode()}

    try:
        logger.info(f"Pregunta recibida: {question}")
        response = chain.run(question)
        set_cached_answer(question, response)
        return {"question": question, "answer": response}
    except Exception as e:
        logger.error(f"Error al procesar la pregunta: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la solicitud")
