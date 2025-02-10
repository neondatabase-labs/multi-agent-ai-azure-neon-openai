import gradio as gr
import asyncio
from app.agents import manager, user_proxy


# Initialize chat history
chat_history = []


async def process_user_input(user_message, chat_history):
    """Handles user input, updates chat history, and processes agent responses asynchronously."""

    # Append user's message (appears on the left)
    chat_history.append({"role": "assistant", "content": user_message})

    # Placeholder for agent response
    chat_history.append({"role": "user", "content": "Processing..."})

    # Immediately update UI
    yield chat_history, chat_history

    # Call the agent in a background thread
    await asyncio.to_thread(user_proxy.initiate_chat, manager, message=user_message)

    # Collect messages from agents
    agent_messages = [
        msg for msg in manager.groupchat.messages if msg.get("role", "") != "System"
    ]

    # Replace "Processing..." with actual responses
    chat_history.pop(-1)

    print("Agent messages:", manager.groupchat.messages)

    # Append each agent's message
    for msg in agent_messages:
        name = msg.get("name", "Agent")
        content = msg.get("content", "")
        role = "user"  # Agents' messages appear on the right

        # Format message with agent's name
        formatted_content = f"**{name}**: {content}"

        # Append to chat history
        chat_history.append({"role": role, "content": formatted_content})

        # Update UI incrementally
        yield chat_history, chat_history

    # Final UI update
    yield chat_history, chat_history


def gradio_chat_interface():
    """Creates and returns a Gradio chat UI."""
    with gr.Blocks() as demo:
        chat_history_state = gr.State([])

        gr.Markdown("# Multi-Agent Chat Interface")

        with gr.Row():
            chatbot = gr.Chatbot(type="messages")  # Ensure correct format
        with gr.Row():
            user_input = gr.Textbox(
                placeholder="Type your message here...", show_label=False
            )
            send_button = gr.Button("Send")
            clear_button = gr.Button("Clear Chat")

        async def on_user_message(user_message, chat_history):
            """Handles user input and updates the UI incrementally."""
            if user_message:
                async for (
                    chat_history_update,
                    chat_history_state_update,
                ) in process_user_input(user_message, chat_history):
                    await asyncio.sleep(0)  # Ensure smooth async updates
                    yield (
                        gr.update(value=chat_history_update),
                        chat_history_state_update,
                    )

        send_button.click(
            on_user_message,
            inputs=[user_input, chat_history_state],
            outputs=[chatbot, chat_history_state],
        )

        user_input.submit(
            on_user_message,
            inputs=[user_input, chat_history_state],
            outputs=[chatbot, chat_history_state],
        )

        clear_button.click(
            lambda: ([], []), None, [chatbot, chat_history_state], queue=False
        )

    return demo


# Run the Gradio interface
demo = gradio_chat_interface()
demo.launch()
