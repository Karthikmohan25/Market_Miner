# Contributing to MarketMiner 🤝

Thank you for your interest in contributing to MarketMiner! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Ecommerce_proj.git
   cd Ecommerce_proj
   ```
3. **Set up the development environment** using our quick start script:
   ```bash
   ./start-dev.sh
   ```

## 🛠 Development Setup

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📝 Making Changes

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards:
   - Use meaningful commit messages
   - Follow Python PEP 8 for backend code
   - Use ESLint/Prettier for frontend code
   - Add comments for complex logic

3. **Test your changes**:
   ```bash
   # Backend tests
   cd backend
   python test_scraper.py
   
   # Frontend tests
   cd frontend
   npm test
   ```

## 🎯 Areas for Contribution

### 🔥 High Priority
- [ ] Real-time scraping improvements
- [ ] Enhanced AI analysis features
- [ ] Mobile responsiveness improvements
- [ ] Performance optimizations

### 🌟 Feature Requests
- [ ] Additional marketplace integrations (Etsy, AliExpress)
- [ ] Advanced filtering options
- [ ] Export functionality (CSV, PDF reports)
- [ ] User authentication and saved searches
- [ ] Dark/light theme toggle

### 🐛 Bug Fixes
- [ ] Scraping reliability improvements
- [ ] UI/UX enhancements
- [ ] Error handling improvements
- [ ] Cross-browser compatibility

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update the README** if you've added new features
5. **Submit your pull request** with:
   - Clear title and description
   - Reference any related issues
   - Screenshots for UI changes

## 🎨 Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use type hints where possible
- Add docstrings for functions and classes
- Keep functions focused and small

### JavaScript/React (Frontend)
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Keep components modular and reusable

## 🧪 Testing

- Write tests for new features
- Ensure existing tests still pass
- Test across different browsers
- Test with various input scenarios

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Karthikmohan25/Ecommerce_proj/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Karthikmohan25/Ecommerce_proj/discussions)
- **Email**: [Your Email] (for sensitive issues)

## 🏆 Recognition

Contributors will be:
- Added to the README contributors section
- Mentioned in release notes
- Given credit in the project documentation

## 📄 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

Thank you for contributing to MarketMiner! 🚀