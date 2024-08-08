# Python Code Challenge - GraphQL & NLP

API with one service and two endpoints

## Run in Docker

The App service runs in a Docker container using Docker Compose. Thus, the first step is to install Docker locally.

To run the Docker Compose, you need to set the environment variable `OPENAI_API_KEY`. To do this, run:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

Finally, start the container running:

```bash
docker compose up --build -d
```

## Run locally

For development purpose, not only is the environment variable `OPENAI_API_KEY` needed but also the absolute path to the CSV file. This can be set using the `.env` file. To do this, create a copy of `.env.example` with the name `.env`:

```bash
cp .env.example .env
```

Then, set the variable properly: `CSV_FILE_PATH=/absolute/path/to/the/data.csv`

Finally, to start the app run:

```bash
python3 -m src.main
```

## App services

The App service has two endpoints:
- /graphql
- /prompt

### /graphql

This is the GraphQL endpoint. The entire schema is:

```
query {
  getItems {
    date
    clientId
    sku
    productCode
    productName
    brand
    productCategory
    mainProductCategory
    productQuantity
    productDetailQuantity
    productIncomeAmount
    addedToCartQuantity
    removedFromCartQuantity
    flagPipol
  }
}
```

### /prompt

This is the NLP service and allows the user to ask questions in natural language. It receives a JSON POST.

For instanse:

```json
{ 
    "prompt": "how many sku are there?"
}
```

The endpoints respond with plain text.

The services use an agent for consuming the OpenAI API.