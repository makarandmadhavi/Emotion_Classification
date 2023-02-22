# Emotion Classification
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Abstract">Abstract</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Abstract


Applications of facial emotion classification is gaining popularity in the world. There are many ways to train a model to classify human facial expressions by use of existing technologies. The strategy to order and recognize feelings of an individual conveyed by his facial expression is done by contrasting it to a gathered set of labelled experiences of feelings. In this paper, we propose the making of an intelligent system that will recognize and classify facial emotions. A multi-layer Convolutional Neural Network model is proposed. Another method of training using pretrained ResNet50 Model is explored. A basic live video streaming application is developed to showcase the use case of our model which will be capable of monitoring and recording facial emotions in real time from a live video stream and subsequently summarize the overall reactions at the end of the stream.

#### Data

This project was uses FER-2013 dataset. https://www.kaggle.com/datasets/msambare/fer2013

#### Publication

https://www.itm-conferences.org/articles/itmconf/abs/2022/04/itmconf_icacc2022_03055/itmconf_icacc2022_03055.html

### Built With

- TensorFlow
- Flask
- openCV

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Create and activate python  [enviornment](https://docs.python.org/3/tutorial/venv.html "enviornment")


### Installation

_clone repo and Install dependencies_

1. Clone the repo
   ```sh
   git clone https://github.com/makarandmadhavi/Emotion_Classification.git
   ```
2. Install python packages
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Running the GUI server

1. change directory to src
   ```sh
   cd src
   ```
2. start flask server
   ```sh
   python app.py
   ```

_For more examples, please refer to the [Documentation](https://example.com)_



<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


