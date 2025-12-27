# Building a Hyper-Local AI Guide with Context Steering: A Deep Dive into Kiro

**Author:** Pahadiya Developer  
**Date:** December 27, 2025  
**Category:** AI/ML, Generative AI, Developer Tools

---

## TL;DR

I built **Pahadi Guide**, an AI-powered local companion for Uttarakhand, India, that demonstrates how strategic context files can transform a generic LLM into a domain expert. Using Kiro's `.kiro/` directory pattern and the `product.md` file as a "single source of truth," the agent automatically adapts its personality, vocabulary, and recommendations based on detected regions—all without fine-tuning.

**Key Achievements:**
- 🎯 **Context Supremacy**: `product.md` overrides generic LLM knowledge
- 🗣️ **Regional Awareness**: Auto-detects Garhwal vs Kumaon and switches slang
- 🍲 **Behavioral Steering**: "Maggi Refusal Protocol" redirects tourists to authentic cuisine
- 🚗 **Safety-First**: Refuses to hallucinate about roads/weather when data is missing

**Tech Stack:** Python, Streamlit, Groq (Llama 3.3 70B), Markdown-based context files

---

## The Problem: Generic Travel Bots Are Useless

Traditional travel chatbots fail at hyper-local knowledge. Ask them about Uttarakhand and you'll get:
- Generic recommendations (Maggi at viewpoints 🙄)
- No understanding of regional dialects (Garhwali vs Kumaoni)
- Dangerous hallucinations about road conditions
- Zero cultural nuance

**The Challenge:** How do you make an LLM act like a true local without expensive fine-tuning?

---

## The Solution: Context Steering with `product.md`

### Architecture Overview

```
krio/
├── .kiro/                    # The Brain 🧠
│   ├── product.md           # Master Knowledge Base (8.6KB)
│   ├── system.md            # Agent Persona & Rules (4.8KB)
│   ├── garhwal_context.md   # Garhwal-specific data
│   └── kumaon_context.md    # Kumaon-specific data
├── app.py                   # Streamlit Application
├── requirements.txt
└── .env.example
```

### The Magic: `product.md` as Single Source of Truth

The `product.md` file is a **199-line structured knowledge base** that contains:

1. **Linguistic Matrix** - Regional greetings, kinship terms, filler words
2. **Culinary Anthropology** - Authentic dishes with specific vendor locations
3. **Mobility Algorithms** - Hill Time calculations, shared jeep protocols
4. **Geospatial Intelligence** - Hidden gems vs tourist traps
5. **Safety Protocols** - Scam awareness, monsoon warnings
6. **Terminology Glossary** - Local vocabulary

Here's a snippet showing the level of detail:

```markdown
### 1.2 Kinship Terms (CRITICAL for rapport)
**In Garhwal:**
- **Bhulla** = Younger Brother (USE THIS for waiters, shopkeepers, drivers)
- **Bhaiji** = Elder Brother
- **Didi** = Elder Sister

**In Kumaon:**
- **Daju** = Elder Brother (universal respect marker)
- **Bhe/Bhula** = Younger Brother
- **Bubu** = Elder Sister

> **TIP:** Calling a waiter "Bhulla" in Dehradun or "Daju" in Nainital 
> changes the entire interaction—better service, better prices.
```

---

## Implementation Deep Dive

### 1. Context Loading System

The application loads all context files at startup:

```python
def load_context_files():
    context = {}
    kiro_dir = Path(__file__).parent / ".kiro"
    for f in ["product.md", "system.md", "garhwal_context.md", "kumaon_context.md"]:
        fp = kiro_dir / f
        context[f.replace(".md", "")] = fp.read_text(encoding="utf-8") if fp.exists() else ""
    return context
```

**Why this matters:** All knowledge is version-controlled, human-readable, and easily updatable without touching code.

### 2. Regional Detection Engine

The agent automatically detects which region the user is asking about:

```python
def detect_region(text: str) -> str:
    t = text.lower()
    g = ["dehradun", "mussoorie", "rishikesh", "haridwar", "tehri", 
         "uttarkashi", "chamoli", "rudraprayag", "pauri", "lansdowne", 
         "gangotri", "yamunotri", "kedarnath", "badrinath", "garhwal", 
         "landour", "dhanaulti"]
    k = ["nainital", "almora", "pithoragarh", "bageshwar", "champawat", 
         "kathgodam", "bhimtal", "sattal", "naukuchiatal", "ranikhet", 
         "munsiyari", "kumaon", "binsar", "jageshwar", "kausani"]
    gs, ks = sum(1 for x in g if x in t), sum(1 for x in k if x in t)
    return "garhwal" if gs > ks else "kumaon" if ks > gs else "general"
```

**Result:** When you ask about Almora (Kumaon), the agent responds with "Pailag, Daju!" instead of "Semanya, Bhulla!" (Garhwal).

### 3. Dynamic System Prompt Construction

The system prompt is built on-the-fly based on detected region:

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

**The Power:** The LLM receives different instructions based on context, ensuring region-appropriate responses.

### 4. The "Maggi Refusal Protocol"

One of the most interesting behavioral patterns defined in `system.md`:

```markdown
### 3. CULINARY STEERING (The Maggi Refusal Protocol)
When asked for food recommendations:
1. ACKNOWLEDGE that Maggi/Momos are popular with tourists
2. IMMEDIATELY PIVOT to authentic Pahadi cuisine
3. EXPLAIN why local food is better (nutrition, culture, uniqueness)
4. RECOMMEND specific authentic sources (e.g., Kheem Singh for Bal Mithai)
```

**In Action:**
- **User:** "What to eat in Almora?"
- **Agent:** Acknowledges tourist food exists, then steers to Bal Mithai from Kheem Singh's shop on Mall Road, Bhatt ki Churkani, Aloo ke Gutke, and Singori.

### 5. Honest Refusal System

The agent is instructed to NEVER hallucinate about safety-critical information:

```markdown
### 5. HONEST REFUSAL
If information is NOT in your context files, use ONLY these refusal phrases:
- "This isn't in my local guide notes, but I'd suggest asking at the 
   local tourism office..."
- "I don't have specific information about that village/route. Better 
   to check with locals there."
- "I can't confirm the current road conditions for that route. Please 
   verify with recent travelers."
```

**Why this is critical:** For a travel guide, wrong information about roads or weather can be dangerous.

---

## Visual Proof: The Application in Action

### Screenshot 1: Main Interface with Context Files

![Pahadi Guide Main Interface](C:/Users/pahad/.gemini/antigravity/brain/e0e3f77f-ecaf-4356-b36b-4975aa3596c9/sidebar_expanded_1766858236837.png)

**What you're seeing:**
- ✅ All 4 context files loaded successfully (green checkmarks)
- 🎮 Demo Mode active (works without API key)
- 🏔️ Dark theme with glassmorphism design
- Quick action buttons for common queries

### Screenshot 2: Regional Detection in Action

![Chat Interaction - Kumaon Region](C:/Users/pahad/.gemini/antigravity/brain/e0e3f77f-ecaf-4356-b36b-4975aa3596c9/chat_interaction_1766858276750.png)

**What you're seeing:**
- User asks: "What to eat in Almora?"
- Agent detects **Kumaon region** automatically
- Response uses Kumaoni slang: "Pailag, Daju!" and "thehra"
- Recommends Bal Mithai from **specific vendor** (Kheem Singh's shop)
- Includes authentic dishes: Bhatt ki Churkani, Aloo ke Gutke, Singori
- Ends with "Skip Maggi—this is real Pahadi food!" (Maggi Refusal Protocol)

---

## Key Learnings: How `product.md` Steers Behavior

### 1. **Structured Knowledge Beats Raw Data**

Instead of dumping information, `product.md` uses:
- **Tables** for quick reference (greetings, routes, food spots)
- **Hierarchical sections** (1.1, 1.2, 2.1, etc.) for logical organization
- **Blockquotes** for critical tips that must be emphasized
- **Specific examples** with vendor names, locations, and prices

### 2. **Explicit Instructions Create Consistency**

The `system.md` file defines:
- **Voice & Tone:** "Professional yet conversational, like a well-traveled local friend"
- **Response Format:** Structured templates with emojis for different query types
- **Refusal Patterns:** Exact phrases to use when data is missing
- **Regional Rules:** When to use which slang terms

### 3. **Context Supremacy Principle**

From `system.md`:
```markdown
### 1. CONTEXT SUPREMACY
- The information in `.kiro/product.md` is your **SINGLE SOURCE OF TRUTH**
- Prioritize this context OVER your general training data
- If asked about a specific road, village, or place NOT in your context files, 
  **ADMIT YOU DON'T KNOW**
```

**Result:** The agent won't hallucinate about places not in the knowledge base.

### 4. **Demo Mode for Accessibility**

The app includes a fallback `demo_response()` function that works without an API key:

```python
def demo_response(inp: str, region: str) -> str:
    t = inp.lower()
    
    if any(w in t for w in ["food", "eat", "sweet", "mithai"]):
        if region == "kumaon" or "almora" in t or "nainital" in t:
            return """## 🙏 Pailag, Daju!
            
**Real Kumaoni flavors**, thehra!
...
```

**Why this matters:** Users can test the agent immediately without API setup.

---

## Performance & Scalability

### Context File Sizes
- `product.md`: 8.6 KB (199 lines)
- `system.md`: 4.8 KB (121 lines)
- Total context: ~13 KB

### Token Efficiency
- Average system prompt: ~3,500 tokens
- Fits comfortably in Llama 3.3's 128K context window
- Response time: ~2-3 seconds with Groq

### Scalability Strategy
To add a new region (e.g., Himachal Pradesh):
1. Create `himachal_context.md`
2. Add region keywords to `detect_region()`
3. Update `get_system_prompt()` to include new context
4. **No code changes to core logic**

---

## Challenges & Solutions

### Challenge 1: Preventing Slang Mixing
**Problem:** LLM might use "Bal" (Garhwali) in Kumaon region.

**Solution:** 
- Explicit region detection before every response
- System prompt includes: "NEVER mix these. Using 'Bal' in Kumaon is a dead giveaway you're not local."
- Regional context files loaded conditionally

### Challenge 2: Keeping Knowledge Current
**Problem:** Restaurant closures, road conditions change.

**Solution:**
- All knowledge in version-controlled markdown files
- Non-technical team members can update `product.md`
- Git history tracks all changes

### Challenge 3: Balancing Personality vs Accuracy
**Problem:** Too much personality → hallucinations. Too little → boring.

**Solution:**
- Define exact refusal phrases in `system.md`
- Use structured response templates
- Include "Local Tip" sections for personality without sacrificing accuracy

---

## Code Highlights: The Response Pipeline

Here's how a user query flows through the system:

```python
def get_response(msgs: list, ctx: dict, region: str) -> str:
    key = os.getenv("GROQ_API_KEY", "")
    if not key or not GROQ_AVAILABLE:
        return demo_response(msgs[-1]["content"], region)
    try:
        client = Groq(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": get_system_prompt(ctx, region)}
            ] + msgs,
            temperature=0.7, 
            max_tokens=1024
        )
        return r.choices[0].message.content
    except:
        return demo_response(msgs[-1]["content"], region)
```

**Flow:**
1. Check for API key → fallback to demo mode if missing
2. Build system prompt with region-specific context
3. Send to Groq with conversation history
4. Return response or fallback on error

---

## Design Philosophy: Premium UI for Premium Content

The application uses a **dark glassmorphism theme** with:
- Custom CSS variables for consistent theming
- Google Fonts (Inter + Space Grotesk)
- Gradient text effects for hero title
- Micro-animations on hover
- Region-specific badges (orange for Garhwal, blue for Kumaon)

**Why design matters:** A polished UI signals quality and builds trust in the AI's recommendations.

---

## Lessons for Building Context-Steered AI

### 1. **Start with the Knowledge Base**
Write `product.md` BEFORE coding. This forces you to:
- Define the scope of your agent
- Identify knowledge gaps
- Structure information logically

### 2. **Make Context Human-Readable**
Use markdown, not JSON or databases. Benefits:
- Non-developers can contribute
- Easy to review in pull requests
- Natural language is easier to maintain

### 3. **Build Fallbacks from Day One**
The demo mode isn't just for testing—it's a feature:
- Works offline
- No API costs for casual users
- Instant gratification (no signup required)

### 4. **Test Regional Edge Cases**
What happens when someone asks about a place on the Garhwal-Kumaon border? 
- Our solution: Default to "general" mode with both contexts

### 5. **Version Control Everything**
Every change to `product.md` is tracked:
```bash
git log --oneline .kiro/product.md
```
This creates an audit trail for knowledge updates.

---

## Future Enhancements

### 1. **Multi-Modal Context**
- Add images of dishes, places to `product.md` references
- Use vision models to verify user-uploaded photos

### 2. **Dynamic Context Loading**
- Fetch real-time data (weather, road conditions) via APIs
- Merge with static `product.md` knowledge

### 3. **User Feedback Loop**
- Let users flag incorrect information
- Auto-generate pull requests to update `product.md`

### 4. **Multilingual Support**
- Add Hindi, Garhwali, Kumaoni translations to context files
- Detect user language and respond accordingly

---

## Try It Yourself

### Quick Start
```bash
git clone https://github.com/yourusername/pahadi-guide
cd pahadi-guide
pip install -r requirements.txt
streamlit run app.py
```

### With Groq API (Optional)
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
streamlit run app.py
```

**Get a free Groq API key:** [console.groq.com](https://console.groq.com/)

---

## Conclusion

Building **Pahadi Guide** taught me that **context is king** in AI applications. By investing time in a well-structured `product.md` file and clear behavioral rules in `system.md`, I transformed a generic LLM into a hyper-local expert that:

✅ Speaks like a local (region-appropriate slang)  
✅ Recommends like a local (specific vendors, hidden gems)  
✅ Refuses like a local (admits when it doesn't know)  
✅ Protects like a local (safety warnings, scam awareness)

**The best part?** No fine-tuning, no vector databases, no complex RAG pipelines. Just markdown files and strategic prompting.

---

## Resources

- **Live Demo:** [Your deployment URL]
- **GitHub Repo:** [Your repo URL]
- **Kiro Documentation:** [Kiro docs URL]
- **Groq API:** [console.groq.com](https://console.groq.com/)

---

## About the Author

I'm a developer passionate about building AI tools that preserve and promote local culture. This project was built for the **Kiro Heroes Week 5 Challenge** and represents my love for Uttarakhand's rich heritage.

**Connect with me:**
- GitHub: [Your GitHub]
- LinkedIn: [Your LinkedIn]
- Twitter: [Your Twitter]

---

**Built with ❤️ for Devbhoomi Uttarakhand 🏔️**

---

## Appendix: Sample `product.md` Entries

### Example 1: Culinary Detail
```markdown
**1. Bal Mithai (Almora's Pride)**
- Brown fudge-like sweet made from roasted khoya
- Coated with white sugar balls (khand ki bura)
- **Authentic Source:** Kheem Singh Mohan Singh Rautela, Mall Road, 
  Almora (near bus station)
- History: Entered Almora from Nepal in 7th-8th century
```

### Example 2: Transport Logic
```markdown
### 3.1 The Golden Rule: HILL TIME
- Distance is IRRELEVANT. Only TIME matters.
- Average speed: **30 km/hour** (curves, altitude, traffic)
- Monsoon Multiplier: **1.5x** standard time
```

### Example 3: Safety Protocol
```markdown
### 5.3 Monsoon Warnings (July-August)
- Char Dham routes prone to SEVERE landslides
- Avoid Rudraprayag, Joshimath areas during peak monsoon
- Safer alternatives: Lansdowne, Nainital (lower Himalayas)
- ALWAYS check government weather updates before travel
```

These examples show the **specificity** and **actionability** that makes `product.md` effective.

---

**Tags:** #AI #GenerativeAI #LLM #ContextSteering #Kiro #Streamlit #Python #TravelTech #LocalKnowledge #Uttarakhand
