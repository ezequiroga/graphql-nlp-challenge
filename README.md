# Python Code Challenge - GraphQL & NLP

API with two service and three endpoints.

## Run in Docker

Both the App and the Docs services run in Docker containers using Docker Compose. Thus, the first step is to install Docker locally.

To run the Docker Compose, you need to set the environment variable `OPENAI_API_KEY` because it is needed by the App service. To do that, run:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

Finally, start the container running:

```bash
docker compose up --build -d
```

Services' port:
- The App service runs on port `8000`
- The Docs service runs on port `8080`

## App endpoints

The App service runs on port `8000`

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

### Docs endpoint

The App service runs on port `8080`.

The endpoint for access the Swagger UI es `/docs`

## Run App locally

For development purpose, the App not only needs the environment variable `OPENAI_API_KEY` but also the absolute path to the CSV file. This can be set using the `.env` file. To do this, create a copy of `.env.example` with the name `.env`:

```bash
cp .env.example .env
```

Then, set the variable properly: `CSV_FILE_PATH=/absolute/path/to/the/data.csv`

Finally, to start the app run:

```bash
python3 -m src.main
```
