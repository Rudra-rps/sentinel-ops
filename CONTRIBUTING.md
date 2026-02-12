# Contributing to SentinelOps

First off, thanks for taking the time to contribute! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, Kubernetes version)
- **Logs** (from `logs/` directory)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear use case** - Why is this enhancement useful?
- **Describe the solution** - How should it work?
- **Alternatives considered** - What other approaches did you think about?

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Add tests if you've added code functionality
3. Ensure tests pass
4. Update documentation
5. Write a clear commit message

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/sentinelops
cd sentinelops

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

#### Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions/classes
- Keep functions focused and small

#### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: short summary (50 chars or less)
- Body: detailed explanation (if needed)

Example:
```
Add ML-based predictive scaling

- Implement LSTM model for load prediction
- Add training pipeline
- Update decision engine to use predictions
- Add tests for prediction accuracy
```

## Project Structure

```
agents/          - Autonomous agents (monitor, scaler, healer)
mcp_server/      - FastAPI REST API
tools/           - Utility modules (k8s, prometheus, chaos)
demo/            - Demo manifests
logs/            - Runtime logs
tests/           - Test suite (coming soon)
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=mcp_server --cov=tools

# Run specific test
pytest tests/test_scaler_agent.py
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update API docs if endpoints change

## Questions?

Feel free to open a discussion or reach out via email.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
