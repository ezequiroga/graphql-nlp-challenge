from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "How many sku are there?",
                }
            ],
        }
    }
