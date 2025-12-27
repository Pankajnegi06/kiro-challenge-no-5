# 🏔️ Pahadi Guide - Uttarakhand Local Guide

> **Kiro Heroes Week 5 Challenge: "The Local Guide"**  
> A hyper-local AI agent that knows Uttarakhand like a true Pahadi!

## 🎯 What is this?

Pahadi Guide is an AI-powered local guide for **Uttarakhand, India** that captures nuances only a local would know. Unlike generic travel bots, it understands:

- 🗣️ **Regional Dialects** - Distinguishes between Garhwali and Kumaoni slang
- 🍲 **Authentic Cuisine** - Steers away from tourist Maggi to real Pahadi food
- 🚗 **Hill Transport** - Shared jeeps, Hill Time, and the unwritten driving code
- 📍 **Hidden Gems** - Secret spots locals love that tourists never find

## 🏗️ Architecture

```
krio/
├── .kiro/                    # Kiro Context Directory (The Brain)
│   ├── product.md           # Master Knowledge Base
│   ├── system.md            # Agent Persona & Steering
│   ├── garhwal_context.md   # Garhwal Region Specifics
│   └── kumaon_context.md    # Kumaon Region Specifics
├── app.py                   # Streamlit Application
├── requirements.txt         # Dependencies
├── .env.example            # Environment Template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Set up API Key
For full AI functionality, get a free Groq API key from [console.groq.com](https://console.groq.com/):
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

> **Note:** The app works in Demo Mode without an API key!

### 3. Run the Application
```bash
streamlit run app.py
```

## ✨ Features

### 🗣️ Slang Translator
- **Garhwali:** "Semanya, Bhulla!" (Hello, Brother!)
- **Kumaoni:** "Pailag, Daju!" (Greetings, Elder Brother!)
- Filler words: "Bal" (Garhwal) vs "Thehra" (Kumaon)

### 🍲 Street Food Recommender
- **Maggi Refusal Protocol:** Steers tourists to real Pahadi cuisine
- Recommends: Kafuli, Bhatt ki Churkani, Bal Mithai, Singori
- Authentic sources: Kheem Singh's shop in Almora (Bal Mithai legend)

### 🚗 Local Transport Guide
- **Hill Time:** Distance is irrelevant, only TIME matters (~30 km/hour)
- Shared Jeep wisdom: "How many seats empty?" not "When is next jeep?"
- **Uphill Priority Rule:** The unwritten code of the mountains

### 📍 Hidden Gems vs Tourist Traps
| Want | Skip | Visit Instead |
|------|------|---------------|
| Lake Views | Nainital Lake (crowded) | Sattal, Naukuchiatal |
| Hill Views | Gun Hill, Mussoorie | Landour (Lal Tibba) |
| Wildlife | Corbett (lottery) | Binsar, Pangot |

## 🎮 Demo Mode

Without an API key, the app runs in **Demo Mode** with pre-built responses for:
- Food recommendations (region-aware)
- Place recommendations (Garhwal vs Kumaon)
- Transport tips
- General greetings

## 🔧 How Agent Steering Works

The `.kiro/` directory implements **Context Supremacy**:

1. `product.md` - Single source of truth for all local knowledge
2. `system.md` - Defines the "Pahadi Guide" persona and rules
3. Region context files - Automatic switching based on detected location

When you ask about Almora, it detects **Kumaon** and uses appropriate slang (Daju, Thehra, Pailag).
When you ask about Mussoorie, it detects **Garhwal** and switches (Bhulla, Bal, Semanya).

## 📝 License

Built with ❤️ for the Kiro Heroes Week 5 Challenge.

---

**🏔️ Devbhoomi Uttarakhand - Land of Gods 🏔️**
