# FAQ-Discord-Bot

## Getting Started

### Prerequisites

Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Code4GovTech/FAQ-Discord-Bot/
    cd FAQ-Discord-Bot
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1. **Environment Variables**

   Create a `.env` file in the root directory of the project and add the following keys:

    ```env
    DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
    APIURL="YOUR_API_URL"
    CHANNELID="YOUR_CHANNEL_ID"
    ```

    Replace `YOUR_DISCORD_BOT_TOKEN`, `YOUR_API_URL`, and `YOUR_CHANNEL_ID` with your actual values.

2. **Menu Structure**

   Create a JSON file named `menu_structure.json` in the root directory. Define your menu and options structure in this file. Here is an example:

    ```json
    {
        "menu": {
            "option1": "Description for option 1",
            "option2": "Description for option 2",
            "option3": {
                "suboption1": "Description for suboption 1",
                "suboption2": "Description for suboption 2"
            }
        }
    }
    ```

### Running the Bot

Create a file named `bot.py` and implement the necessary code for the bot functions. After completing the code, you can run the bot with the following command:

```sh
python3 bot.py
