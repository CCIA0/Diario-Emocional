# diario_emocional_mvp

## Overview
This project is a FastAPI application designed to serve as an emotional diary and dashboard. It allows users to create, read, update, and delete journal entries while providing insights through a dashboard interface.

## Project Structure
The project is organized into the following main directories:

- **app**: Contains the main application code.
  - **api**: Contains the API endpoints for the application.
  - **core**: Contains core functionalities such as configuration and security.
  - **models**: Contains data models and schemas.
  - **services**: Contains business logic and services, including database interactions and AI functionalities.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd diario_emocional_mvp/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the FastAPI application, run the following command:
```
uvicorn app.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Usage

- **Journal Endpoints**: Use the endpoints defined in `app/api/endpoints/journal.py` to manage journal entries.
- **Dashboard Endpoints**: Use the endpoints defined in `app/api/endpoints/dashboard.py` to retrieve insights and statistics.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.