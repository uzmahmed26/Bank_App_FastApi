🚀 Features

User Authentication
Authenticate a single user by name and PIN. Authenticate multiple users simultaneously.

Bank Transfer
Transfer money from one user to another. Validates authentication, user existence, and sufficient funds.

Balance Check
View balance for a single user. Get updated account details for all users.

Run the FastAPI server
uv run uvicorn account:app --reload

Open your browser to view docs
http://127.0.0.1:8000/docs

🔗 API Endpoints
Method Endpoint Description POST /authenticate Authenticate one user POST /authenticate-both Authenticate two users at once POST /bank-transfer Transfer balance between users GET /balance/{name} Check balance of a specific user GET /update-accounts Get updated account details (both)

📌 Notes

The authentication is stored temporarily in memory using a Python set(). The user database is simulated using a Python dictionary.

