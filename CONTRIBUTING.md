# Contributing to airradar

Thank you for your interest in contributing to airradar! This document provides guidelines and information for contributors.

## 📋 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- PyQt5
- Linux environment (Ubuntu/Debian/Kali recommended)
- Root privileges for WiFi scanning capabilities

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vinothvbt/airradar.git
   cd airradar
   ```

2. **Install dependencies**
   ```bash
   sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python3 test_imports.py
   python3 validate_system.py
   ```

## 🔄 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes
- Follow the existing code style and patterns
- Add comments for complex logic
- Maintain the professional hacker-style theming
- Ensure security considerations are addressed

### 3. Test Your Changes
```bash
# Run basic tests
python3 test_imports.py
python3 test_system.py
python3 validate_system.py

# Test GUI components (requires display)
python3 test_gui.py
python3 test_ui_simple.py
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "type: brief description of changes"
```

**Commit Message Format:**
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` code formatting
- `refactor:` code restructuring
- `test:` adding tests
- `security:` security improvements

### 5. Push and Create Pull Request
```bash
git push origin your-branch-name
```

Then create a pull request through GitHub.

## 📊 Code Review Process

### Review Standards

All pull requests undergo a formal review process:

1. **Automated Checks**
   - Code quality checks (flake8, black, isort)
   - Security scanning (bandit, safety)
   - Basic functionality tests

2. **Human Review**
   - Code quality and style consistency
   - Security considerations
   - Documentation adequacy
   - Test coverage
   - User experience impact

### Review Criteria

#### ✅ Code Quality
- [ ] Follows Python PEP 8 guidelines
- [ ] Consistent with existing code style
- [ ] Proper error handling
- [ ] Meaningful variable and function names
- [ ] Appropriate comments and docstrings

#### 🔒 Security
- [ ] No hardcoded credentials or sensitive data
- [ ] Input validation where appropriate
- [ ] Secure handling of network operations
- [ ] No introduction of known vulnerabilities

#### 📚 Documentation
- [ ] Code is self-documenting or well-commented
- [ ] README updated if needed
- [ ] New features documented appropriately
- [ ] Breaking changes clearly marked

#### 🧪 Testing
- [ ] Existing tests pass
- [ ] New functionality includes tests
- [ ] Edge cases considered
- [ ] Manual testing performed

## 🎨 Code Style Guidelines

### Python Style
- Follow PEP 8 conventions
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings for public functions

### PyQt5 UI Guidelines
- Maintain the professional hacker-style theming
- Use consistent Matrix green color scheme (#00FF00)
- Ensure responsive design
- Follow existing UI patterns

### Security Coding Practices
- Validate all user inputs
- Use secure defaults
- Implement proper error handling
- Follow principle of least privilege

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Details**
   - Operating system and version
   - Python version
   - PyQt5 version
   - Wireless interface details

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Additional Context**
   - Log output or error messages
   - Configuration details
   - Network environment

## 💡 Feature Requests

For feature requests, please provide:

1. **Problem Statement**
   - What problem does this solve?
   - Why is this needed?

2. **Proposed Solution**
   - Detailed description of the feature
   - How it would work
   - User interface considerations

3. **Implementation Details**
   - Technical considerations
   - Potential challenges
   - Security implications

## 🛡️ Security

### Reporting Security Issues

For security vulnerabilities:

1. **Critical Issues**: Contact maintainers privately
2. **General Security**: Use the security issue template
3. **Follow responsible disclosure practices**

### Security Guidelines

- Never commit sensitive information
- Validate all network inputs
- Use secure coding practices
- Consider privacy implications
- Test in isolated environments

## 📝 Documentation

### Documentation Standards

- Keep README.md up-to-date
- Document new features and changes
- Use clear, concise language
- Include code examples where helpful
- Maintain professional tone

### Types of Documentation
- **README.md**: Main project documentation
- **Code Comments**: Inline documentation
- **Docstrings**: Function and class documentation
- **THEMING_AND_VIEWS.md**: UI/UX guidelines

## 🤝 Community

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- Pull Request Reviews: Code discussions
- Project Discussions: General questions and ideas

### Community Guidelines
- Be respectful and professional
- Provide constructive feedback
- Help newcomers get started
- Share knowledge and experience

## 📈 Continuous Improvement

We encourage community involvement through:

- **Code Reviews**: Participate in pull request reviews
- **Testing**: Help test new features and bug fixes
- **Documentation**: Improve and expand documentation
- **Feature Ideas**: Suggest improvements and new features
- **Bug Reports**: Help identify and reproduce issues

## 🏆 Recognition

Contributors are recognized through:
- GitHub contributor listings
- Release notes acknowledgments
- Community shout-outs for significant contributions

## 📞 Getting Help

If you need help:

1. Check existing documentation
2. Search through issues and discussions
3. Create a new issue with detailed information
4. Tag maintainers if urgent

## 🔄 Release Process

1. Features are merged into development branches
2. Testing and validation performed
3. Release candidates created
4. Final testing and documentation updates
5. Tagged releases with changelog

---

Thank you for contributing to airradar! Your contributions help make WiFi security analysis more accessible and effective for the community.

**Happy Coding! 🚀**