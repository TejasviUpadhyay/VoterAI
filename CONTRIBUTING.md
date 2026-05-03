# Contributing to VotePath AI Backend

## Development Setup

### Prerequisites
- Python 3.12+
- Google Cloud SDK
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/TejasviUpadhyay/VoterAI.git
cd VoterAI

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## Code Standards

### Style Guide
- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints
- Write docstrings for all public functions

### Testing
- Write tests for all new features
- Maintain 90%+ code coverage
- Run tests before committing

### Commit Messages
- Use clear, descriptive messages
- Reference issue numbers when applicable

## Pull Request Process
1. Create feature branch
2. Write tests
3. Update documentation
4. Submit PR with description
