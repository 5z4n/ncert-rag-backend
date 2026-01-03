from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag.main.retrieve import retrieve, answer_from_records
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    class_name: str | None = None
    subject: str | None = None

@app.post("/ask")
def ask(req: AskRequest):
    try:
        records = retrieve(req.question, req.class_name, req.subject)

        if not records:
            return {
                "answer": "No relevant NCERT content found.",
                "source": None
            }

        answer, source = answer_from_records(records, req.question)

        return {
            "answer": answer,
            "source": source
        }

    except Exception as e:
        # 🔥 THIS prevents 500 crashes
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
