# Contributing to AI-Powered Todo Chatbot

Thank you for your interest in contributing to the AI-Powered Todo Chatbot! We welcome contributions from the community and appreciate your efforts to improve the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Pull Request Process](#pull-request-process)
6. [Community Guidelines](#community-guidelines)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-todo-chatbot.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies and set up your environment following the instructions in the README

## Development Workflow

### Setting Up Your Environment

1. Navigate to the backend directory and install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Navigate to the frontend directory and install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Set up your environment variables as described in the README

### Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines

3. Test your changes thoroughly

4. Commit your changes with a clear, descriptive commit message:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible

### JavaScript/TypeScript
- Use ESLint with the project's configuration
- Follow the Airbnb JavaScript Style Guide
- Use TypeScript for type safety where applicable
- Write JSDoc comments for exported functions

### General
- Write meaningful commit messages
- Keep pull requests focused on a single feature or bug fix
- Update documentation when adding new features

## Testing

### Backend Tests

Run backend tests using pytest:
```bash
cd backend
pytest
```

### Frontend Tests

Run frontend tests:
```bash
cd frontend
npm test
```

### Test Coverage

- Aim for at least 80% test coverage for new features
- Write unit tests for all business logic
- Include integration tests for API endpoints
- Add end-to-end tests for critical user flows

## Pull Request Process

1. Ensure your branch is up to date with the main branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main
   ```

2. Run all tests to make sure everything passes:
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

3. Create your pull request with:
   - A clear title that describes the changes
   - A detailed description of what was changed and why
   - Links to any related issues
   - Screenshots or videos if adding UI changes

4. Address any feedback from the code review process

5. Wait for approval before merging

## Community Guidelines

- Be respectful and inclusive in all interactions
- Provide constructive feedback during code reviews
- Ask questions when you're unsure about something
- Help others when they need assistance
- Follow the project's code of conduct

## Questions?

If you have any questions about contributing, feel free to open an issue or contact the maintainers.

Thank you for contributing to the AI-Powered Todo Chatbot!