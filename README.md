# FastPay Backend

FastPay is a FastAPI-based backend application for a digital wallet and transaction system. It provides APIs to manage users, wallets, and transactions in a secure and efficient manner.

---

## Features

- **User Management**
  - Create, retrieve, update, and delete users.
  - Password handling with hashing (optional to implement).

- **Wallet Management**
  - Create wallets linked to users.
  - Retrieve wallets by wallet ID or user ID.
  - Update wallet balance and currency.
  - Delete wallets.

- **Transaction Management**
  - Record transactions between users.
  - Retrieve transactions by user ID or transaction ID.
  - Delete transactions.
  - Future implementation: auto-update wallets on transaction.

- **API Documentation**
  - Interactive API docs available via Swagger UI.

---

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MongoDB
- **ORM/ODM:** PyMongo (native MongoDB driver)
- **Python Version:** 3.10+
- **Environment Management:** Virtualenv
- **Dependencies:** See `requirements.txt`

---

## Project Structure

