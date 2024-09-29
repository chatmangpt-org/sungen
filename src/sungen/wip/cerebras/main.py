
def main():
    """Main function"""
    from sungen.utils.dspy_tools import init_ol
    init_ol()

    import requests

    # Define the API endpoint
    url = 'https://api.cerebras.ai/v1/chat/completions'

    # Set the headers
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer demo-xmyc249jrym6xx6r5ty3k4cfkn6rpvyj48dj5k3hffcf2pp5',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://inference.cerebras.ai',
        'priority': 'u=1, i',
        'referer': 'https://inference.cerebras.ai/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-stainless-arch': 'unknown',
        'x-stainless-lang': 'js',
        'x-stainless-os': 'Unknown',
        'x-stainless-package-version': '1.0.1',
        'x-stainless-runtime': 'browser:chrome',
        'x-stainless-runtime-version': '128.0.0'
    }

    # Define the payload with only the first 2 messages
    data = {
        "messages": [
            {
                "content": "Please try to provide useful, helpful and actionable answers.",
                "role": "system"
            },
            {
                "content": "Ridiculously fast LLM inference would unlock...",
                "role": "user"
            }
        ],
        "model": "llama3.1-8b",
        "stream": False,
        "temperature": 0.2,
        "top_p": 1,
        "max_tokens": 4096
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Print the response from the server
    print(response.json())


if __name__ == '__main__':
    main()
