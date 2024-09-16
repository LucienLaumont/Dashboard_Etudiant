# 🏫 **L'ETUDIANT Project : Scrapper - DataBase - Dashboard - Dockerisation**

## 📚 Overview
This repository contains a project completed during the second year of engineering studies in the Data Science and AI class at ESIEE Paris. The project was a collaborative effort between Emmanuelle Lepage (emmanuelle.lepage@edu.esiee.fr) and Me. The main objective was to develop a Dockerized dashboard application accompanied by a database populated with data scraped from a selected website.

We chose the French website "L'étudiant" to scrape information about all high schools in France. The project involves various visualizations including the distribution of public and private high schools, success rates at the baccalaureate exam, and a dynamic map displaying the location and information of all high schools in France.

## 🌐 General Context
For our project, we scraped the "L'Etudiant" website and collected information on all high schools in France. Our dashboard, created with Dash, allows us to exploit this data and highlight baccalaureate success rates across different regions and between different types of schools, whether private or public. We also display high schools on a map of France by geolocating them.

## 🛠️ Project Structure
Our data is scraped and extracted into a MongoDB database where they are stored in a "lycée" collection within the "database_étudiant" database. This connection to MongoDB is established via `Mongoclient` contained in the `pymongo` library.

Additionally, two Dockerfiles were created. The entire system is managed with Docker Compose, which integrates the two Dockerfiles and establishes an execution order for them.

### 🕷️ Web Scraping
Our scraping was performed using Scrapy. It operates through regional lists and accesses individual school details to extract structured information such as the name, baccalaureate success rate, city, etc. The data retrieval is carried out in several steps:

1. Identification of links to all regional lists.
2. In each region, the spider iterates over the lists of establishments to capture basic information contained in the "first box."
3. On the individual pages of each high school, details contained in the "second box" are extracted.

### 🍃 MongoDB
The connection to MongoDB is established by creating an instance of `Mongoclient`. The URL specifies mongo as the host because we are in a Docker environment. Subsequently, the "Database_etudiant" database and the "lycee" collection are selected.

### 🐳 Dockerization
We orchestrate three services with Docker Compose:

- **Scraper**: Allows data extraction from the online link of the L'Etudiant site. It depends on the Mongo service to store the extracted data.
- **MongoDB**: Uses the Mongo image from Docker Hub to create a MongoDB database. It is mapped to port 27017 to allow connection to the database from outside the container.
- **Dashboard**: Aims to visualize and interact with the collected data. It depends on the two previous services.

## 🚀 Running the Project with Docker

```bash
docker-compose build
docker-compose up
```

The data loading process might take some time due to a check that occurs every 20 seconds.

## 🎨 Visualizations and Features
1. **Public and Private High Schools Distribution**: A graph showing the number of public versus private high schools.
2. **Baccalaureate Success Rates**: Visualizations highlighting the success rates of high school students in the baccalaureate exam.
3. **Dynamic Map**: An interactive map displaying the location and detailed information of high schools across France.

## 💾 Installation and Setup

### Prerequisites
- **Python**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).
- **Docker**: Docker should be installed and running. Download it from [docker.com](https://www.docker.com/).
- **Scrapy**: The Scrapy library is required for web scraping.
- **Plotly and Dash**: These libraries are used for creating the interactive visualizations and the dashboard.
- **Pymongo**: Required for connecting to MongoDB.

You can install the Python libraries using pip:
```bash
pip install scrapy plotly dash pymongo
```

### Steps to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/school-dashboard.git
   cd school-dashboard
   ````
2. **Build the Docker Image**:
   ```bash
    docker-compose build
   ````
3. **Run the Docker Containers**:
   ```bash
    docker-compose up
   ````
4. **Access the Dashboard**:
  Open your web browser and navigate to http://localhost:8050 to view the dashboard.

  **It is likely that the dashboard window will not fit the dimensions of your screen. Use Ctrl - or Ctrl + to adjust the display size accordingly.**

## 📧 Contact
For any inquiries or further information, please contact [Lucien Laumont] at lucien.laumont@edu.esiee.fr or Emmanuelle Lepage at emmanuelle.lepage@edu.esiee.fr.
