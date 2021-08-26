
![bmwi](https://socialify.git.ci/DSSGxUK/bmwi/image?font=Bitter&forks=1&issues=1&logo=https%3A%2F%2Fwww.dssgfellowship.org%2Fwp-content%2Fuploads%2F2019%2F11%2Fdssglogonounivfb.png&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Light)

# 📊 BMWI Prediction and Visualisation Tool 

## 📖 Resources 

You can find all the relevant links for project here:- 

* **Regional Unemployment Forecasting Tool**: [here](https://bmwi-tool.herokuapp.com/)

* **Documentation**: [here](https://dssgxuk.github.io/bmwi/) 

* **Video Tutorials**: The tutorials to understand how the application works can be found [here](https://www.youtube.com/playlist?list=PLzWRWFPEUpHbwIHq0T6M72B1_5N04hD0Q)

## 🚀 About the Project 

This project is a collaboration between [German Federal Ministry for Economic Affairs and Energy (BMWi)](https://www.bmwi.de/Navigation/EN/Home/home.html) and [Data Science for Social Good Fellowship, UK](https://warwick.ac.uk/research/data-science/warwick-data/dssgx/). The goal of the project is to build a bottom-up forecasting model for predicting economic development in Germany based on regional data. The bottom-up approach focusses on the predictions at the Kreis (county) level rather than a federal level and provides an alternate approach to forecasting. The project draws on fine-grained data on the demographic, economic and sectoral structure of regions with the aim of improving economic forecasts during times of shocks. The unemployment rate in the different regions of Germany has been used as a proxy for the economic development in that region. 

## 🧰 About the tool 

This is a forecasting tool built using Streamlit to forecast the unemployment rate for the next three months at the Kreis level in Germany. The purpose of the tool is to provide a complete pipeline from data analysis to model predictions in a simple easy-to-acess UI.

## Project Overview

The following diagram shows the tool architecture which includes the data processing, predictions and deployment.

![architecture](./img/architecture.jfif)

<!-- ## 🧩 Components

The different components of the this application are:

![user-workflow](./img/flowchart.png) -->

## 🖥️ Dashboard

The dashboard of the tool is built using [Streamlit](https://streamlit.io/). 

![dashboard](./img/dashboard.png)

## ⚡ How to Run 

* Clone the repository - `git clone https://github.com/DSSGxUK/bmwi.git`
* Install the dependencies - `pip install -r requirements.txt`
* Run the application - `streamlit run app.py`

## ⚒️ Contributors 

The **fellows** undertaking this project are: 

<table>
  <tr>
    <td align="center"><a href="https://github.com/amitSasson"><img src="https://avatars.githubusercontent.com/u/44767201?v=4" width="100px;" alt=""/><br /><sub><b>Amit Sasson</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/CinnyLin"><img src="https://avatars.githubusercontent.com/u/45028889?v=4" width="100px;" alt=""/><br /><sub><b>Cinny Lin</b></sub></a><br /></td>
    <td align="center"><a href="https://prakharrathi25.netlify.app/"><img src="https://avatars.githubusercontent.com/u/38958532?v=4" width="100px;" alt=""/><br /><sub><b>Prakhar Rathi</b></sub></a><br /></td> 
    <td align="center"><a href="https://github.com/VighneshNatarajanGanesh"><img src="https://media-exp1.licdn.com/dms/image/C5603AQE4UR-P4qFxrQ/profile-displayphoto-shrink_400_400/0/1622238265212?e=1633564800&v=beta&t=OCqJpAhZ1-YXfb4QHyQ9sSLg9Ydd3bARHFBADDXLT84" width="100px;" alt=""/><br /><sub><b>Vighnesh Natarajan Ganesh</b></sub></a><br /></td> 
  </tr>
</table>

The **mentors** for this project are:

<table>
  <tr>
    <td align="center"><a href="mailto:doschmund.kwiatkowski@gmail.com"><img src="https://warwick.ac.uk/research/data-science/warwick-data/dssgx/2021-fellows-mentors/doschmund.png" width="100px;" alt=""/><br /><sub><b>Doschmund Kwiatkowski</b></sub></a><br /></td> 
    <td align="center"><a href="https://www.linkedin.com/in/yurii-tolochko-050376162/"><img src="https://media-exp1.licdn.com/dms/image/C4D03AQGhssWzzWDb7g/profile-displayphoto-shrink_200_200/0/1565367212984?e=1635379200&v=beta&t=YzVcRBEO0PRId__SS6UlEl51e8Ia-pjp2Xy0A60dGpg" width="100px;" alt=""/><br /><sub><b>Yurii Tolochko</b></sub></a><br /></td> 
  </tr>
</table>
