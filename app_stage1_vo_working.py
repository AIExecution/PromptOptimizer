import streamlit as st
from engine import AdvancedPromptOptimizer

MODEL_COSTS = {
    "GPT-4": (0.03, 0.06),
    "Claude": (0.02, 0.08),
    "LLaMA 2": (0.012, 0.04),
    "Custom": (None, None),
}


def format_cost(tokens, cost_per_k):
    return f"${tokens * cost_per_k / 1000:.4f}"


def main():
    st.set_page_config(layout="wide", page_title="Prompt Optimizer")
    st.title("🚀 AI Prompt Optimizer")

    col1, col2 = st.columns(2)
    with col1:
        prompt = st.text_area(
            "Original Prompt", height=200, placeholder="Paste your AI prompt here..."
        )
        aggressiveness = st.slider(
            "Optimization Level",
            0.0,
            1.0,
            0.7,
            help="Higher = more aggressive shortening",
        )
        model = st.selectbox("AI Model", list(MODEL_COSTS.keys()))

        if model == "Custom":
            input_cost = st.number_input("Input Cost ($/1K tokens)", 0.01, 1.0, 0.03)
            output_cost = st.number_input("Output Cost ($/1K tokens)", 0.01, 1.0, 0.06)
        else:
            input_cost, output_cost = MODEL_COSTS[model]

    if st.button("Optimize", type="primary"):
        optimizer = AdvancedPromptOptimizer()
        optimized, orig_toks, new_toks = optimizer.optimize(prompt, aggressiveness)

        with col2:
            st.text_area("Optimized Prompt", optimized, height=200)
            savings = orig_toks - new_toks
            st.metric(
                "Token Savings",
                f"{savings} tokens ({(savings)/orig_toks*100:.1f}%)",
                delta=f"-{savings/orig_toks*100:.1f}%",
            )

            # Cost analysis
            st.subheader("💰 Cost Analysis")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(
                    f"**Input Cost**\n\n"
                    f"Original: {format_cost(orig_toks, input_cost)}\n\n"
                    f"Optimized: {format_cost(new_toks, input_cost)}"
                )
            with col_b:
                st.markdown(
                    f"**Output Cost**\n\n"
                    f"Original: {format_cost(orig_toks, output_cost)}\n\n"
                    f"Optimized: {format_cost(new_toks, output_cost)}"
                )

            # Optimization report
            with st.expander("📝 Optimization Report"):
                st.write(f"**Original Tokens:** {orig_toks}")
                st.write(f"**Optimized Tokens:** {new_toks}")
                st.progress(savings / orig_toks)

                st.markdown("### Applied Rules")
                st.json(
                    {
                        "Removed fillers": "e.g., 'very', 'carefully'",
                        "Shortened phrases": "'advantages/disadvantages' → 'pros/cons'",
                        "Structural changes": "Simplified JSON formatting",
                    }
                )

                st.markdown("### Share Your Savings")
                st.code(
                    f"Saved {savings} tokens (${format_cost(savings, input_cost + output_cost)}) with #PromptOptimizer"
                )


if __name__ == "__main__":
    main()
