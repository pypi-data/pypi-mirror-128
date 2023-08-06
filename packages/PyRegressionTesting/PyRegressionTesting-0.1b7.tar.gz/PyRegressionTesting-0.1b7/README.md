# PyRegressionTesting

# Setup on Linux
`cd /home/dev`
`wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip`
`unzip chromedriver_linux64.zip`

# Usage

## Parameters
- Config: JSON-File with Testing insctructions
- Driver: Optional Path to Chrome-Driver file
- Threads: Number of threads for parallel Tests
- Logging: Print everything to console?
- Headless: Should tests be done headless?

`PyRegressionTesting --config=/path/to/config.json --driver=/path/to/chromedriver.exe --threads=1 [--logging] [--headless]`