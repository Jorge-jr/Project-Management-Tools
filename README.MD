# Project Management Tools

**Note: This project is currently under construction and is not yet ready for production use.**

Project Management Tools is a comprehensive toolset designed to facilitate both traditional and agile project management. Built with a focus on efficiency and flexibility, this project aims to streamline the process of managing projects, from planning and execution to monitoring and completion.

## Features

- **Comprehensive Project Management**: Manage all aspects of your projects, from planning to execution, with a single, unified toolset.
- **Support for Traditional and Agile Methodologies**: Whether you're following a traditional project management approach or an agile methodology, our tools are designed to accommodate both.
- **Built with Modern Technologies**: Leveraging the power of FastAPI, Pydantic, SQLAlchemy, Alembic, and AIOPG, our tools are built to be fast, reliable, and scalable.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 10 or higher

### Installation

1. Clone the repository:

    git clone https://github.com/Jorge-jr/Project-Management-Tools.git

2. Navigate to the project directory:

    cd project-management-tools

3. Install the required dependencies:

    pip install -r requirements.txt

4. Set up the database:
   - Create a PostgreSQL database and user.
   - Update the `.env` file with your database credentials.
   - Run the Alembic migrations:
      alembic upgrade head


### Running the Application

To start the application, run:
    uvicorn main:app --reload


The application will be available at `http://localhost:8000`.

## Usage

### API Documentation

Once the application is running, you can access the API documentation at `http://localhost:8000/docs`.


## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for providing a fast, web-based framework for building APIs.
- Pydantic for data validation and settings management using Python type annotations.
- SQLAlchemy for providing a full suite of well-known enterprise-level persistence patterns.
- Alembic for database migration.
- AIOPG for asynchronous database access.
- [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template) for providing the foundation for this project.

## Contact

If you have any questions or suggestions, please feel free to open an issue or contact the project maintainers.
