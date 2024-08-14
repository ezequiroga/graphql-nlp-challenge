# Python Code Challenge - GraphQL & NLP

API with three service and five endpoints.

Content:
- [Run services with Docker Compose](#run-services-with-docker-compose)
- [Endpoints](#endpoints)
  - [/graphql](#graphql)
  - [/prompt](#prompt)
- [Docs](#docs)
- [Run App service locally](#run-app-locally)
- [oAuth authentication](#oauth-authentication)

## Run services with Docker Compose

The App, the Docs and the Auth services run in Docker containers using Docker Compose. Thus, the first step is to install Docker locally.

To run the Docker Compose, you need to set the environment variable `OPENAI_API_KEY` because it is needed by the App service. To do that, run:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

> NOTE: The App service also needs the environment variables `CSV_FILE_PATH` and `OAUTH_SERVICE_URL`. For testing purpose they can ramain as they are in the `docker-compose.yaml` file

Finally, start the container running:

```bash
docker compose up --build -d
```

The services' port are:
- The App service runs on port `8000`
- The Docs service runs on port `8080`
- The Auth service runs on port `9090`

## Endpoints

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

### Docs

The Doc service runs on port `8080`.

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

## oAuth authentication

Both App endpoints `/graphql` and `/prompt` are secured by oAuth authentication.

The authentication follows two steps:
- Log in using user and pass: send a POST to the Auth service to `/token`

```bash
curl -X POST "http://localhost:9090/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user&password=pass"
```

For testing purpose it can be use: `user: challenge@user.com` and `pass: fakehashedsecret`

This endpoint returns the token that need to be use for consuming the endpoints.

- The token obteined previously must be sent in the `Authorization` header as `Authorization: Bearer token`. For instance:

```bash
curl -X POST "http://localhost:8000/prompt" \
-H "Authorization: Bearer obteined_token" \
-H "Content-Type: application/json" \
-d '{"prompt": "How many products are there?"}'
```
