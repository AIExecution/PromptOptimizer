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

    col1, col2 = st.columns([0.6, 0.4])  # 60/40 split for better space utilization

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

        # Calculate savings
        token_savings = orig_toks - new_toks
        percent_savings = (token_savings / orig_toks) * 100
        input_cost_savings = token_savings * input_cost / 1000
        output_cost_savings = token_savings * output_cost / 1000
        total_cost_savings = input_cost_savings + output_cost_savings

        with col1:
            st.subheader("Optimized Prompt")
            st.code(optimized, language="text")

            # Add download button
            st.download_button(
                "📥 Download Optimized Prompt",
                optimized,
                file_name="optimized_prompt.txt",
            )

        with col2:
            st.subheader("💰 Optimization Results")

            # Token Savings - Percentage First
            st.markdown(
                f"""
                <div style="background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:15px;">
                    <h3 style="color:#2e86c1;margin-top:0;">Token Reduction</h3>
                    <div style="font-size:28px;font-weight:bold;color:#27ae60;text-align:center;">
                        {percent_savings:.1f}%
                    </div>
                    <div style="text-align:center;color:#7f8c8d;font-size:14px;">
                        {token_savings} tokens saved
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Cost Savings - Percentage First
            cost_percent_savings = (
                total_cost_savings
                / (orig_toks * (input_cost + output_cost) / 1000)
                * 100
            )
            st.markdown(
                f"""
                <div style="background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:15px;">
                    <h3 style="color:#2e86c1;margin-top:0;">Cost Reduction</h3>
                    <div style="font-size:28px;font-weight:bold;color:#27ae60;text-align:center;">
                        {cost_percent_savings:.1f}%
                    </div>
                    <div style="text-align:center;color:#7f8c8d;font-size:14px;">
                        ${total_cost_savings:.4f} saved per call
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Visual indicator with percentage
            st.progress(percent_savings / 100)
            st.caption(f"Prompt reduced to {100-percent_savings:.1f}% of original size")
            # Detailed Breakdown
            with st.expander("📊 Cost Analysis"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(
                        f"**Input Cost**\n\n"
                        f"Original: {format_cost(orig_toks, input_cost)}\n\n"
                        f"Optimized: {format_cost(new_toks, input_cost)}\n\n"
                        f"Saved: {format_cost(token_savings, input_cost)}"
                    )
                with col_b:
                    st.markdown(
                        f"**Output Cost**\n\n"
                        f"Original: {format_cost(orig_toks, output_cost)}\n\n"
                        f"Optimized: {format_cost(new_toks, output_cost)}\n\n"
                        f"Saved: {format_cost(token_savings, output_cost)}"
                    )

            # Optimization report
            with st.expander("🔍 Applied Optimizations"):
                st.markdown("### Common Transformations")
                st.json(
                    {
                        "Removed fillers": "e.g., 'very', 'carefully'",
                        "Shortened phrases": "'advantages/disadvantages' → 'pros/cons'",
                        "Structural changes": "Simplified JSON formatting",
                        "Verb optimization": "Converted to base forms",
                        "Preposition removal": "Dropped non-essential connectors",
                    }
                )

                st.markdown("### Share Your Savings")
                st.code(
                    f"Saved {token_savings} tokens (${total_cost_savings:.4f}) with #PromptOptimizer\n"
                    f"Optimization level: {aggressiveness*100:.0f}%"
                )


if __name__ == "__main__":
    main()
