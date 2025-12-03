+++
title = 'How to rock: The Ultimate Guide to Creating Better AI Prompts'
date = 2025-12-03T12:45:51Z
draft = false
[taxonomies]
tags = [ "ai", "how-to-rock" ]
[extra]
header = "/assets/ultimate-guide-to-creating-better-ai-prompts/kaleidoscope.jpg"
+++

After a couple of nights fighting with LLMs, I noticed that most "bad outputs" were actually **my** lack of clarity.
This post is a brain dump so you can avoid my detours and ship prompts that behave.

<!-- more -->

TLDR: personas + context + structure beat "hey, write this for me" every single time.

# The core principle

**AI prompting is programming with words, not asking questions.** You're not chatting, you are instructing a probabilistic completion engine. Treat prompts like mini specs: inputs, constraints, outputs.

If you can't explain what you want to yourself, the model will improvise (is this a feature or a bug ? ¯\\\_(ツ)_/¯). All prompting problems are thinking problems. Write the gist in your notebook, then paste it.

## Essential techniques
- **Use personas** ([ref](https://en.wikipedia.org/wiki/Persona_(psychology)))
    - Tell the AI who it is and who it's talking to. This helps cut the noise.
- **Provide context (ABC: Always Be Contexting)** ([ref](https://medium.com/@unstitution21/why-context-is-everything-a1db99b28671))
    - Include all relevant facts, even the obvious ones.
    - Give explicit permission for the AI to say "I don't know", this reduces hallucinations.
    - Remember: any missing context, the AI will fill in with guesses.
- **Define output requirements**
    - Specify the format, tone, and any other constraints for the response.
- **Use few-shot examples**
    - Show 2–3 written samples in the style or format you want. The more concrete, the better.

## Advanced techniques
- **Chain of Thought (COT)** ([ref](https://arxiv.org/pdf/2201.11903))
    - Ask the model to show its reasoning steps before writing the final answer.
- **Tree of Thought (TOT)** ([ref](https://arxiv.org/pdf/2305.08291))
    - Request multiple solution options, then ask for a synthesis or best-of.
- **Battle of the bots (adversarial validation)** ([ref:D3](https://arxiv.org/pdf/2410.04663), [ref](https://www.mdpi.com/2076-3417/15/7/3676))
    - Set up competing personas and add a "critic" to help validate or improve outputs.


# References

- [The Ultimate Guide to AI Prompting](https://www.youtube.com/watch?v=pwWBcsxEoLk)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)


# What should you do now ?

Maybe using AI to create the prompt for you is the best thing to do :)

For that, use the following text as an instruction for llms to write the prompt for you:

(Think of it as a blog inside of a blog)

```md
# The Ultimate Guide to Creating Better AI Prompts

## The Core Principle
**AI prompting is programming with words, not asking questions.** You're not having a conversation—you're instructing a prediction engine that completes patterns based on probability.

## The Meta-Skill: Clarity of Thought
Before you write a single prompt, **think clearly about what you want**. If you can't explain it clearly to yourself, you can't prompt it. All prompting problems are actually thinking problems.

---

## Essential Techniques

### 1. **Use Personas**
Tell the AI who it should be to narrow its focus and improve responses.

**Example:** "You're a senior site reliability engineer for CloudFlare. You're writing to both customers and engineers."

**Why it works:** Gives the AI a specific perspective and expertise to draw from instead of generic knowledge.

---

### 2. **Provide Context (Most Important)**
Give the AI ALL the details it needs. Never assume it knows something—more context = fewer hallucinations.

**Key principle:** ABC = Always Be Contexting
- Include all relevant facts
- Be specific and detailed
- Don't hold back information
- Give it permission to say "I don't know" if it lacks information

**Pro tip:** Whatever context you don't provide, the AI will fill in with guesses.

---

### 3. **Define Output Requirements**
Tell the AI exactly how you want the result to look.

**Specify:**
- Format (bulleted list, under 200 words, etc.)
- Tone (professional, casual, anxious, etc.)
- Structure (timeline, sections, headers)
- Style constraints (no corporate fluff, radically transparent)

---

### 4. **Use Few-Shot Examples**
Show the AI what you want instead of just describing it. Provide 2-3 examples of the exact output style you're looking for.

**Why it works:** Removes guesswork—you're teaching by example rather than description.

---

## Advanced Techniques

### **Chain of Thought (COT)**
Ask the AI to think step-by-step before answering.

**Example:** "Before writing this email, think through it step by step..."

**Modern shortcut:** Use "Extended Thinking" or "Reasoning" mode built into most AI platforms.

---

### **Tree of Thought (TOT)**
Have the AI explore multiple approaches simultaneously, then synthesize the best path.

**Example:** "Brainstorm three distinct approaches: [A], [B], [C]. Evaluate each, then synthesize them."

---

### **Battle of the Bots (Adversarial Validation)**
Create competing personas that critique each other.

**Example:** "Generate a 3-round competition with [persona 1], [persona 2], and [critic]. Have them debate and collaborate on the final output."

**Why it works:** AI is better at critiquing than original creation.

---

## Common Mistakes to Avoid

1. **Being vague** - AI fills gaps with guesses
2. **Skipping context** - Leads to hallucinations
3. **Assuming knowledge** - AI doesn't remember everything
4. **Not defining output** - Gets generic results
5. **Messy thinking** - Creates messy prompts

---

## The Process

1. **Think first, prompt second**
2. Write down exactly what you want before prompting
3. Ask yourself: "Could a human do this with the information I've provided?"
4. If yes → the AI probably can too
5. If no → add more context and clarity

---

## Quick Wins

- **Enable web search** when you need current information
- **Save successful prompts** in a library for reuse
- **Use prompt enhancers** to improve your raw prompts
- **Treat bad outputs as skill issues** - the problem is usually your clarity, not the AI

---

## Remember

The AI can only be as clear as you are. When frustrated with results, don't blame the AI—look in the mirror. It's a skill issue. Get clearer about what you want, and the AI will get clearer in its responses.
```
