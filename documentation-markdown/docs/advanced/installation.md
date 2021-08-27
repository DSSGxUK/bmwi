# Technical Documentation 

This section is for people who might want to edit the code base of the application. The repository with all the code can be found [here](https://github.com/prakharrathi25/the-tool-bmwi).

The application is built using the following tools and frameworks: 

- [Python](https://docs.python.org/3/) 
- [Streamlit](https://streamlit.io/) 
- [Pandas](https://pandas.pydata.org/docs/)
- [Statsmodels](https://www.statsmodels.org/stable/index.html) 
<!-- - [Keras]()  -->

To make edits to the tool, one must know how to work with the aforementioned frameworks. More details about each of them can be found on the links provided above. 

## About Streamlit 

This application is built using [Streamlit](https://streamlit.io/), a Python framework to build interactive web applications. It has a rich API for various interactive features which can be learnt more about [here](https://docs.streamlit.io/en/stable/api.html). It's a relatively new framework and its recommended to explore [building basic apps](https://docs.streamlit.io/en/stable/getting_started.html) with it before diving deep into the repository. 

To set up the repository on your local machine follow the installation steps below: 

## Installation Steps

To set up the application on your local machine, follow these steps. 

- Clone the repository on your local machine 

    ```
    git clone <link>
    ```

- Create a virtual environment 
    - For MacOS/Linux - ```python3 -m venv env`
    - For Windows - `py -m venv env`

The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it `env`. Read more about virtual env [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). 

> **Note:** You should exclude your virtual environment directory from your version control system using .gitignore or similar.

- Activate the virtual environment 

    - For MacOS/Linux - `source env/bin/activate`

    - For Windows - `.\env\Scripts\activate`

<br> 

- Install requirements 

```bash
pip install -r requirements.txt
```

- Run the streamlit app 

```bash
streamlit run app.py
```