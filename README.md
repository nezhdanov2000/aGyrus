# 🤖 Booking Bot - Modular AI Chatbot

A modular AI chatbot system for class booking with separate ML and GPT-2 components.

## 🚀 Quick Start

### Install Dependencies
```bash
# General dependencies
pip install -r dependencies/requirements.txt

# Logistic Regression components
pip install -r dependencies/requirements-logistic-regression.txt

# GPT-2 components (optional)
pip install -r dependencies/requirements-gpt2.txt
```

### Run the Bot
```bash
# From project root
python booking_bot.py
```

## 📁 Project Structure

```
gpt-2/
├── 🤖 booking_bot.py                    # MAIN LAUNCHER
├── 📦 dependencies/                     # Dependencies
│   ├── requirements.txt                 # General dependencies
│   ├── requirements-logistic-regression.txt # Logistic Regression dependencies
│   ├── requirements-gpt2.txt            # GPT-2 dependencies
│   └── README.md                        # Dependencies documentation
├── ⚙️ config/                           # Configuration
│   ├── bot_config.py                    # Main bot configuration
│   ├── ml_config.py                     # ML configuration
│   └── gpt2_config.py                   # GPT-2 configuration
├── 🧠 logistic_regression/              # Logistic Regression components
│   ├── intent/                          # Intent classification
│   │   └── classifier.py                # IntentClassifier class
│   ├── entity/                          # Entity extraction
│   │   └── extractor.py                 # EntityExtractor class
│   ├── utils/                           # ML utilities
│   └── __init__.py                      # Package initialization
├── 🤖 gpt2/                             # GPT-2 components and model
│   ├── components/                      # GPT-2 components
│   │   ├── download_model.py            # Model download script
│   │   ├── test_gpt2.py                 # GPT-2 testing
│   │   └── __init__.py                  # Package initialization
│   ├── model/                           # Trained GPT-2 model
│   │   └── 124M/                        # 124M parameter model
│   │       ├── model.ckpt.data-00000-of-00001
│   │       ├── model.ckpt.index
│   │       ├── model.ckpt.meta
│   │       ├── hparams.json
│   │       ├── encoder.json
│   │       ├── vocab.bpe
│   │       └── checkpoint
│   └── __init__.py                      # Package initialization
├── 💬 dialog/                           # Dialog system
│   ├── dialog/                          # Dialog management
│   │   ├── state.py                     # DialogState class
│   │   ├── schedule.py                  # ScheduleManager class
│   │   └── __init__.py                  # Package initialization
│   ├── responses/                       # Response generation
│   │   ├── generator.py                 # ResponseGenerator class
│   │   └── __init__.py                  # Package initialization
│   ├── utils/                           # Dialog utilities
│   │   └── __init__.py                  # Package initialization
│   └── __init__.py                      # Package initialization
├── 🧪 tests/                            # Tests
├── 📚 gpt2_original/                    # Original GPT-2 code (archive)
├── .gitignore                           # Git ignore rules
├── .gitattributes                       # Git attributes
└── README.md                            # This file
```

## 🤖 Bot Capabilities

- **Intent Classification**: 5 types (greeting, booking, cancellation, schedule, goodbye)
- **Entity Extraction**: Date and time recognition from natural language
- **Dialog Management**: Multi-step conversations with context preservation
- **Schedule Management**: Class booking and cancellation
- **Conflict Prevention**: Protection against double booking

## 💬 Usage Examples

```
👤 User: I want to book a class
🤖 Bot: Sure! I'd be happy to help you book a class. What date would you like to book?

👤 User: Tomorrow at 2pm
🤖 Bot: ✅ Perfect! Your class is booked for 2025-01-15 at 14:00. I'll send you a reminder. See you then!

👤 User: Show me the schedule
🤖 Bot: 📅 Available slots for the next 7 days:
Monday (2025-01-20): 09:00, 10:00, 11:00, 12:00, 13:00, 15:00, 16:00, 17:00
```

## 🔧 Technologies

- **Intent Classification**: Logistic Regression + TF-IDF
- **Entity Extraction**: Regex + Natural Language Rules
- **Dialog Management**: State Machine
- **Response Generation**: Template-based (GPT-2 integration planned)

## 📊 Supported Intents

| Intent | Examples | Description |
|--------|----------|-------------|
| `greeting` | "hello", "hi", "hey" | Welcome messages |
| `book_class` | "book a class", "schedule", "reserve" | Class booking requests |
| `cancel_class` | "cancel", "unbook", "remove booking" | Cancellation requests |
| `show_schedule` | "show schedule", "available times" | Schedule inquiries |
| `goodbye` | "bye", "see you later" | Farewell messages |

## 🧪 Testing

### Test Intent Classification
```bash
# Run the bot and test different intents
python booking_bot.py

# Example test inputs:
# - "hello" → greeting
# - "book a class" → book_class
# - "cancel my booking" → cancel_class
# - "show schedule" → show_schedule
# - "bye" → goodbye
```

### Test GPT-2 Components
```bash
# Test GPT-2 model (if implemented)
python gpt2/components/test_gpt2.py
```

## 📈 Development Roadmap

- [ ] **GPT-2 Integration**: Replace template responses with GPT-2 generated responses
- [ ] **Multi-language Support**: Add Russian and other language support
- [ ] **REST API**: Create web API for bot integration
- [ ] **Database Integration**: Add persistent storage for bookings
- [ ] **Unit Tests**: Comprehensive test coverage
- [ ] **Monitoring & Logging**: Production-ready logging and monitoring
- [ ] **Docker Support**: Containerized deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment

## 🔧 Configuration

### Bot Configuration (`config/bot_config.py`)
- Intent classification settings
- Schedule management settings
- Response templates
- File paths

### ML Configuration (`config/ml_config.py`)
- Model paths
- Training data paths
- ML-specific settings

### GPT-2 Configuration (`config/gpt2_config.py`)
- Model directory paths
- Cache settings
- GPT-2 specific parameters

## 📦 Dependencies

### General Dependencies
- `pyyaml` - Configuration management
- `python-dotenv` - Environment variables
- `pytest` - Testing framework
- `colorama` - Colored terminal output

### Logistic Regression Dependencies
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `pandas` - Data processing

### GPT-2 Dependencies
- `transformers` - Hugging Face transformers
- `torch` - PyTorch framework
- `tensorflow` - TensorFlow (optional)

## 🚀 Installation Options

### Full Installation (All Components)
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-logistic-regression.txt
pip install -r dependencies/requirements-gpt2.txt
```

### ML-Only Installation
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-logistic-regression.txt
```

### GPT-2 Only Installation
```bash
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-gpt2.txt
```

## 📄 License

[Modified MIT](./LICENSE)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Additional Resources

- [Dependencies Documentation](dependencies/README.md)
- [Original GPT-2 Repository](https://github.com/openai/gpt-2)
- [GPT-2 Paper](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

---

## 📜 GPT-2 Original Code

Original GPT-2 code is preserved in the `gpt2_original/` folder and available for experimentation.

**Status**: Archived (code provided as-is, no updates planned)

**Citation**:
```
@article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019}
}
```