from langfuse import observe

@observe()
def test_function():
    return "Langfuse works!"

print(test_function())