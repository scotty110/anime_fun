# Generate Anime playing cards with RPC servers
Quick demo for generating a "playing card" for an anime character based off of simple characteristics. 
This demo does require a Nvidia GPU with at least 12GB of vram (I am using 3090TI). Models are run in low bit precision to help with vram usage.


## Setup
Install Python and Golang Deps
### Python 
1. `mamba env create -f enviroment.yaml`
2. Log into Huggingface: `huggingface-cli login`
3. Request access for `https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct` and `https://huggingface.co/stabilityai/stable-diffusion-3.5-large` 
Note. The inital run will take some time to download all the files. 


### Golang 
1. Install golang, provided is a script `install_go.sh` that will install golang system wide (will overwrite other go versions).
2. Run `install_twirp.generators.sh` in the middle_man folder. 


### Generate RPC servers (proto)
1. Run `source init_dir.sh` in middle_man folder
2. Activate conda env: `conda activate frieren`
3. Run `./gen.sh` inside `middle_man/rpc` folder


## Build Middle Man
Middle man is the Twirp/RPC server that is generating the playing card by managing the requests to the 2 AI models and 1 python function. 
It contains:
1. A client, what a user runs to interact with rpc servers
2. A server, which is the backend service that manages the playing card generation. 

To build the two binaries run `./build.sh` inside the middle_man folder.


## Running
You will need 5 terminals (think of servers as being on seperate machines). 
1. In each of `caption_image`, `diffusion_model` and `llm_model`, activate the `frieren` conda env (`conda activate frieren`) then run the provided `./run.sh` script. You should see some logging information appear (also the AI models will pull their respective weights if this is first time running).
2. Run `server` in `middle_man/bin`. This starts the coordination server.
3. Run `client` in `middle_man/bin`. This will prompt you for input. You can give a brief description of the character you would like to create. 

You should see logging from each of the services as the different models do their respective aspects of the task. 

