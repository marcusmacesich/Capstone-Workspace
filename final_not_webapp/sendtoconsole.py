import getsessions        
from contextlib import redirect_stdout


# Mock send function (replace with your actual implementation)
def send(message):
    #print(f"Sending: {message.strip()}")
    getsessions.msg(ids[0], ids[1], message)

# Custom stream for redirecting output
class SendStream:
    def write(self, message):
        if message.strip():
            send(message)
    def flush(self):
        pass

def get_user_input_with_redirect():
    send_stream = SendStream()
    global ids 
    ids = getsessions.init_console()
    print("Type 'exit' or 'quit' to stop.")
    with redirect_stdout(send_stream):
        while True:
            user_input = input("Enter something: ")
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                getsessions.destroy(vars[0], vars[1])
                break
            print(f"You entered: {user_input}")

# Run the function
get_user_input_with_redirect()