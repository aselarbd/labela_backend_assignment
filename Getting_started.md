# Assignment

## Description

This is the AutoCompany API platform. This API platform contain following features.

- A REST API to managing a products.
- User creation via API
- Clients can add, remove products to a shopping cart
- Clients can order items in shopping cart


## Prerequisites

- Docker 24.0.6


## Run Project using Docker

- `docker build -t autocompany .`
- `docker run --name autocompany_app -p 8000:80 -d autocompany`
- `Navigate to http://127.0.0.1:8000/`

## Next steps
- As first step create a user for app via following endpoint
```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@auto.com",
    "username": "admin",
    "password": "admin",
    "user_type": "COMPANY"
}'
```

- Then in every API call use this credentials
### Note that you need to set the email instead of the username for Basic Authentication.

Example  you have to generate base64 encoding of `admin@auto.com:admin` -> `YWRtaW5AYXV0by5jb206YWRtaW4`.

From this point onwards, I will refer this as `BASIC_TOKEN`

# API Documentation

### Swagger Documentation

Swagger documentation can be found here `http://127.0.0.1:8000/api/swagger`

### Redoc Documentation

Redoc documentation can be found here `http://127.0.0.1:8000/api/redoc`


# User stories

#### As a company, I want all my products in a database, so I can offer them via our new platform to customers

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/products/' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/products/' \
--header 'Authorization: Basic <BASIC_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Windshield Wipers",
    "description": "Clears rain, snow, and debris from the windshield for improved visibility while driving.",
    "price": 14.99,
    "available_quantity": 35,
    "active": true
}
'
```

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/products/<PRODUCT_ID>' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```
```bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/v1/products/<PRODUCT_ID>' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```

```bash
curl --location --request PUT 'http://127.0.0.1:8000/api/v1/products/<PRODUCT_ID>' \
--header 'Authorization: Basic <BASIC_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Air Filter v2",
    "description": "Cleans the air entering the engine to prevent damage and enhance performance.",
    "price": 15.99,
    "available_quantity": 10,
    "active": true
}
'
```

#### As a client, I want to add a product to my shopping cart, so I can order it at a later stage

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/cart/add' \
--header 'Authorization: Basic <BASIC_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "product": 8
}
'
```

#### As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/cart/remove' \
--header 'Authorization: Basic <BASIC_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "product": 1
}
'
```

#### Additional: client can view shopping cart

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/cart/' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```

#### As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car
#### As a client, I want to select a delivery date and time, so I will be there to receive the order

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/checkout' \
--header 'Authorization: Basic <BASIC_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "delivery_date": "2023-10-25T14:32:21.875481Z"
}'
```

#### As a client, I want to see an overview of all the products, so I can choose which product I want

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/products/' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```

#### As a client, I want to view the details of a product, so I can see if the product satisfies my needs

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/products/<PRODUCT_ID>' \
--header 'Authorization: Basic <BASIC_TOKEN>'
```
