# Technical Blog Submission for AWS Builder Center

## 📝 Blog Details

**Title:** Building a Hyper-Local AI Guide with Context Steering: A Deep Dive into Kiro

**Author:** Pahadiya Developer

**Date:** December 27, 2025

**Category:** AI/ML, Generative AI, Developer Tools

**Reading Time:** ~15 minutes

---

## 📂 Submission Files

### Main Blog Files
1. **`technical_blog_aws.html`** - Fully formatted HTML version with embedded styling
2. **`technical_blog_aws.md`** - Markdown version for easy editing

### Visual Assets (Screenshots)
All screenshots are located in: `C:/Users/pahad/.gemini/antigravity/brain/e0e3f77f-ecaf-4356-b36b-4975aa3596c9/`

1. **`sidebar_expanded_1766858236837.png`** - Shows the main interface with:
   - All 4 context files loaded (✅ green checkmarks)
   - Demo Mode status
   - Quick action buttons
   - Dark glassmorphism theme

2. **`chat_interaction_1766858276750.png`** - Demonstrates regional detection:
   - User query: "What to eat in Almora?"
   - Agent detects Kumaon region
   - Uses appropriate slang: "Pailag, Daju!" and "thehra"
   - Recommends specific vendors (Kheem Singh's shop)
   - Shows "Maggi Refusal Protocol" in action

### Video Recording
- **`pahadi_guide_demo_1766858215706.webp`** - Browser recording showing the complete interaction flow

---

## 🎯 What This Blog Demonstrates

### Core Concept: Context Steering with product.md

The blog explains how I used **Kiro's `.kiro/` directory pattern** to transform a generic LLM into a hyper-local expert for Uttarakhand, India, without any fine-tuning.

### Key Technical Achievements Explained:

1. **Context Supremacy**
   - `product.md` as single source of truth (8.6KB, 199 lines)
   - Overrides generic LLM knowledge with specific local information
   - Version-controlled, human-readable knowledge base

2. **Regional Awareness**
   - Automatic detection of Garhwal vs Kumaon regions
   - Dynamic switching of slang, greetings, and cultural references
   - Example: "Bhulla" (Garhwal) vs "Daju" (Kumaon)

3. **Behavioral Steering**
   - "Maggi Refusal Protocol" - redirects tourists from generic food to authentic cuisine
   - Structured response templates defined in `system.md`
   - Explicit refusal patterns for missing information

4. **Safety-First Design**
   - Agent refuses to hallucinate about roads, weather, or safety-critical info
   - Honest admission when data is not in context files
   - Prevents dangerous misinformation

---

## 📊 Blog Structure

### 1. Introduction
- Problem statement: Generic travel bots fail at hyper-local knowledge
- The challenge: Making LLMs act local without fine-tuning

### 2. Architecture Deep Dive
```
.kiro/
├── product.md           # Master Knowledge Base
├── system.md            # Agent Persona & Rules
├── garhwal_context.md   # Garhwal-specific data
└── kumaon_context.md    # Kumaon-specific data
```

### 3. Implementation Details
- Context loading system
- Regional detection engine
- Dynamic system prompt construction
- The "Maggi Refusal Protocol"
- Honest refusal system

### 4. Visual Proof
- Screenshot 1: Main interface with context files
- Screenshot 2: Regional detection in action

### 5. Key Learnings
- Structured knowledge beats raw data
- Explicit instructions create consistency
- Context supremacy principle
- Demo mode for accessibility

### 6. Performance & Scalability
- Context file sizes
- Token efficiency (~3,500 tokens)
- Response time (~2-3 seconds with Groq)
- Scalability strategy for new regions

### 7. Challenges & Solutions
- Preventing slang mixing
- Keeping knowledge current
- Balancing personality vs accuracy

### 8. Lessons for Builders
- Start with the knowledge base
- Make context human-readable
- Build fallbacks from day one
- Test regional edge cases

---

## 🔑 Key Code Examples Included

### 1. Context Loading
```python
def load_context_files():
    context = {}
    kiro_dir = Path(__file__).parent / ".kiro"
    for f in ["product.md", "system.md", "garhwal_context.md", "kumaon_context.md"]:
        fp = kiro_dir / f
        context[f.replace(".md", "")] = fp.read_text(encoding="utf-8") if fp.exists() else ""
    return context
```

### 2. Regional Detection
```python
def detect_region(text: str) -> str:
    t = text.lower()
    g = ["dehradun", "mussoorie", "rishikesh", ...]  # Garhwal keywords
    k = ["nainital", "almora", "pithoragarh", ...]   # Kumaon keywords
    gs, ks = sum(1 for x in g if x in t), sum(1 for x in k if x in t)
    return "garhwal" if gs > ks else "kumaon" if ks > gs else "general"
```

### 3. Dynamic System Prompt
```python
def get_system_prompt(ctx: dict, region: str) -> str:
    base = ctx.get("system", "")
    prod = ctx.get("product", "")
    if region == "garhwal":
        rc, ri = ctx.get("garhwal_context", ""), "GARHWAL: Use Bhulla, Bal, Semanya."
    elif region == "kumaon":
        rc, ri = ctx.get("kumaon_context", ""), "KUMAON: Use Daju, Thehra, Pailag."
    else:
        rc, ri = ctx.get("garhwal_context", "") + ctx.get("kumaon_context", ""), "GENERAL"
    return f"{base}\n\n{ri}\n\n{prod}\n\n{rc}"
```

---

## 📈 product.md Structure Explained

The blog includes detailed examples from `product.md`:

### 1. Linguistic Matrix
- Regional greetings (Garhwali vs Kumaoni)
- Kinship terms (Bhulla, Daju, Didi, Bubu)
- Filler words (Bal, Thehra)
- Common phrases with translations

### 2. Culinary Anthropology
- The "Maggi Refusal Protocol"
- Sweet Trinity (Bal Mithai, Singori, Chocolate)
- Savory staples with specific vendors
- Street food intelligence by city

### 3. Mobility Algorithms
- Hill Time Rule (30 km/hour average)
- Shared jeep ecosystem
- The "Hill Code" for self-driving
- Common routes with realistic times

### 4. Geospatial Intelligence
- Hidden gems vs tourist traps
- Landour deep dive
- Nainital beyond the lake

### 5. Safety & Social Protocols
- Scam awareness
- Social etiquette
- Monsoon warnings

---

## 🎨 Design Highlights

The HTML blog features:
- **Premium dark theme** with glassmorphism effects
- **Custom CSS variables** for consistent theming
- **Google Fonts** (Inter + Space Mono)
- **Gradient text effects** for headings
- **Syntax-highlighted code blocks** with language labels
- **Responsive tables** for data presentation
- **Screenshot galleries** with detailed captions
- **Tag system** for categorization

---

## 💡 Why This Blog Matters for AWS Builder Center

### 1. Practical Implementation
- Real working code, not just theory
- Complete architecture explained
- Copy-paste ready examples

### 2. Novel Approach
- No fine-tuning required
- No vector databases needed
- Simple markdown-based context steering

### 3. Scalability Insights
- How to add new regions
- Version control for knowledge
- Non-technical team contribution

### 4. Safety & Ethics
- Honest refusal patterns
- Preventing hallucinations
- Safety-critical information handling

### 5. Developer Experience
- Demo mode for instant testing
- Human-readable context files
- Easy maintenance and updates

---

## 🚀 Quick Start for Readers

The blog includes a complete quick start guide:

```bash
git clone https://github.com/yourusername/pahadi-guide
cd pahadi-guide
pip install -r requirements.txt
streamlit run app.py
```

**Optional:** Get free Groq API key from [console.groq.com](https://console.groq.com/)

---

## 📊 Metrics & Performance

| Metric | Value |
|--------|-------|
| product.md size | 8.6 KB (199 lines) |
| system.md size | 4.8 KB (121 lines) |
| Total context | ~13 KB |
| Average system prompt | ~3,500 tokens |
| Response time (Groq) | ~2-3 seconds |
| Context window used | <3% of 128K |

---

## 🏆 Key Takeaways for Readers

1. **Context is King** - Well-structured context files can replace expensive fine-tuning
2. **Markdown > JSON** - Human-readable formats enable team collaboration
3. **Explicit > Implicit** - Define exact behaviors in system prompts
4. **Safety First** - Build refusal patterns for missing data
5. **Demo Mode Matters** - Instant gratification improves adoption

---

## 📝 Tags

#AI #GenerativeAI #LLM #ContextSteering #Kiro #Streamlit #Python #TravelTech #LocalKnowledge #Uttarakhand #AWS #BuilderCenter #Groq #Llama

---

## 📧 Contact Information

**Author:** Pahadiya Developer  
**Project:** Pahadi Guide - Uttarakhand Local AI Companion  
**Challenge:** Kiro Heroes Week 5  
**Theme:** The Local Guide

---

## ✅ Submission Checklist

- [x] Technical blog written (HTML + Markdown)
- [x] Screenshots captured showing UI and functionality
- [x] Code examples included with explanations
- [x] Architecture diagram provided
- [x] product.md usage explained in detail
- [x] Visual proof of regional detection
- [x] Performance metrics included
- [x] Challenges and solutions documented
- [x] Quick start guide provided
- [x] Tags and metadata added

---

## 🎯 Blog Highlights

### Most Interesting Sections:

1. **The "Maggi Refusal Protocol"** - Shows how behavioral steering works
2. **Regional Detection Engine** - Demonstrates automatic context switching
3. **Visual Proof Screenshots** - Shows the agent correctly using Kumaoni slang
4. **product.md Structure** - Reveals the knowledge organization strategy
5. **Honest Refusal System** - Explains safety-first design

---

## 📖 How to View the Blog

### Option 1: HTML Version (Recommended)
Open `technical_blog_aws.html` in any modern browser for the full experience with:
- Premium dark theme
- Embedded screenshots
- Syntax-highlighted code
- Responsive design

### Option 2: Markdown Version
Open `technical_blog_aws.md` in any markdown viewer or editor for:
- Easy editing
- Plain text format
- Version control friendly

---

## 🔗 Related Files in Repository

- `app.py` - Main Streamlit application
- `.kiro/product.md` - Master knowledge base (featured in blog)
- `.kiro/system.md` - Agent persona and rules (featured in blog)
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies

---

**Built with ❤️ for Devbhoomi Uttarakhand 🏔️**

**Submitted for Kiro Heroes Week 5 Challenge**
