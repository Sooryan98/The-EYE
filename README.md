# The-Glasses 
Millions of people miss the joy of reading a book as they turned blind earlier on in their lives. Project Glasses is aimed at enabling such blind people to regain the lost feeling of reading texts, pamphlets, flyers, etc.
The code mimics the functioning of a normal eye by processing the live video feed from the embedded camera and then once processing is finished any form of output can be given, in this case, the audio of the generated text is read out loud.

The code uses OpenCV and OCR to develop text capture from a live videoframe continuously and generate pages that can be stored locally and read again.



<img width="324" alt="image" src="https://github.com/Sooryan98/The-EYE/assets/67855335/55a9e028-367a-4963-8f7b-fcb951513bc3">

## Text recognition and filtering algorithm: 
The algorithm begins with a page control variable that dictates its behavior. If set to "Repeat," the program extracts Optical Character Recognition (OCR) from the last token of a processed file and reads the text aloud. If set to "Next," it captures video from the camera and initiates the image processing pipeline.
Image Processing and Text Extraction:
The captured image undergoes preprocessing steps, including conversion to grayscale and thresholding. Low-level text perception is achieved using the PyTesseract library. The extracted text is assigned a confidence ratio, which plays a crucial role in subsequent error filtering.
Error Filtering:
Error reduction is a key focus of our solution. The algorithm employs blur detection using a Laplacian transform function to identify and filter out blurred text. The text obtained from the initial OCR process, associated with confidence ratios, and the text obtained after blur detection are passed through a similarity detector. This enables the system to filter errors and enhance the accuracy of the final output.


## Code Design:
### Blurdetection.py
This module is responsible for detecting blur in images.

variance_of_laplacian(img): Calculates the variance of Laplacian for an image.

BGR2RGB(BGR_img): Converts an image from BGR to RGB format.

blurrinesDetection(directories, threshold): Detects blur in a set of images and displays the result.

### Audiogenerator.py
This module handles the generation of audio from text using the gTTS (Google Text-to-Speech) library.

text_reader(path_to_page): Reads text from a given file path, tokenizes it into sentences, and converts each sentence to audio.

The script continuously reads and converts sentences until interrupted.

### Page_control.py
Manages the page control flow, allowing the user to navigate between pages.
Functionality: Asks the user to input 'n' for the next page or 'r' for the previous page.
Creates folders for each page and utilizes the Buffer function from processor.py to process and display the pages.

### Processor.py
Implements the main processing logic for the text recognition device.
similar(n, sim, rate, image_frame, maxconf_id): Compares the similarity between text on different frames.

removefiles(val, k, image_frames, rate): Removes either blurred or duplicate image files based on input.

files(image_frames): Initializes the video capture and frame extraction process.

process(src_vid, rate, image_frames, final): Processes the video frames, converts to grayscale, and saves thresholded images.

get_text(n, page_path, conf_list): Extracts text from images and calculates confidence levels.

text_gen_fresh(page_path, ogtag, rate): Generates text files from fresh frames.

read_text(path_to_new, direc): Reads and prints the content of text files.

Buffer(page_folder, direc): Serves as the main entry point for processing pages.

Buffer (from processor.py)

Functionality: Calls different functions to process and analyze pages based on the direc parameter (0 for new pages, 1 for repeated pages). Coordinates the entire text recognition pipeline.
