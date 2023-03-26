import openai


openai.api_key = "GET UR OWN KEY"



def getchatcompletion(prompt):
    
    # Define the prompt and the maximum length of the generated response
    # prompt = "Hello, how are you today?"
    max_tokens = 50

    # Generate a response from the ChatGPT model
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.3,
        max_tokens=max_tokens
    )

    # Print the generated response text
    print ("chatgpt completion says ... ")
    print(response.choices[0].text.strip())
    
    return response.choices[0].text.strip()



def getchatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": prompt},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)
    
    return result



# res = getchatgpt("tell me about the rainforest in 50 words or less")
