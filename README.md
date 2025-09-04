CodeFrameConverter

📌 Project Overview

This project is a pipeline designed to \*\*automatically collect, refine, and convert crawled code data into high-quality datasets for LLM training\*\*.  

It follows the process of \*\*Code Crawling → DataFrame Conversion → Filtering \& Scoring → Natural Language Conversion\*\*, with the goal of generating clean and useful parallel datasets of code and text.

---

🚀 Key Features

1. Code Crawling (step0\_crawling.ipynb)  
  - Collect code from web/repositories and save it in JSON format

2. DataFrame Conversion (step1\_json\_to\_df.ipynb)
 - Convert JSON into Pandas DataFrame to organize and inspect data

3. Data Filtering (step2\_filtering.ipynb)  
 - Remove unnecessary or low-quality code  
 - Apply rule-based and condition-based filtering  

4. Scoring (step3\_scoring.ipynb)
 - Evaluate code quality and usefulness  
 - Assign scores to individual samples within the dataset  

5. Natural Language Conversion (step4\_converting.ipynb)
 - Generate natural language descriptions for code  
 - Build a parallel dataset of \*\*code–text pairs\*\*  

---

📂 Folder Structure

root/

├─ code\_converted/ # Final dataset with natural language conversion

├─ code\_filtered/ # Filtered code dataset

├─ code\_source/ # Source code dataset converted to JSON

├─ crawled\_source/ # Crawled raw source code files (starting point)

│── step0(crawling).ipynb # Code crawling

│── step1(json\_to\_df).ipynb # JSON → DataFrame

│── step2(filtering).ipynb # Code filtering

│── step3(scoring).ipynb # Code scoring

│── step4(converting).ipynb # Code-to-natural-language conversion

│── README.md


⚙️ Installation
pip install -r requirements.txt

⚙️ Output
High-quality code–natural language paired dataset for LLM training (in code\_converted folder)

