# Image Analysis Project

## Overview
The Image Analysis Project is a web application that allows users to upload an image and then leverages Azure Vision API to analyze the uploaded image. The application extracts text content using Optical Character Recognition (OCR) and segments visual elements within the image.

## Features
- **Image Upload**: Users can upload an image via the web interface.
- **Text Extraction**: Extracts all text content from the uploaded image using Azure Vision API.
- **Visual Element Segmentation**: Basic image segmentation to isolate individual visual elements within the main image.
- **Display Results**: Displays the extracted text and visual segments on the result page.


## Installation

### Prerequisites
- Python 3.6+
- An Azure account with Computer Vision service set up
- Azure subscription key and endpoint

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/image_analysis_project.git
    cd image_analysis_project
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up Azure Computer Vision credentials:
    - Create a file named `config.py` in the project root directory with the following content:
        ```python
        AZURE_SUBSCRIPTION_KEY = "your_azure_subscription_key"
        AZURE_ENDPOINT = "your_azure_endpoint"
        ```

## Running the Application
1. Start the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Usage
1. On the home page, click the "Choose File" button to select an image from your local machine.
2. Click the "Upload Image" button to upload and analyze the image.
3. The results page will display the extracted text and segmented images.

## Detailed Report
The detailed project report can be found in the `report/` directory, which includes documentation on the approach, chosen technologies, implementation details, and challenges encountered.

## Bonus Features
- Basic HTML structure to sort the extracted content into appropriate tags like paragraphs (`<p>`) and creating and embedding static images of visual elements using `<img>` tags.

## Limitations
- The program does not handle complex layouts or intricate designs within the images.
- Advanced chart detection and conversion functionalities are not included.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
