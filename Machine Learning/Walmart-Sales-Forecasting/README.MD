# Walmart Sales Forecasting using Machine Learning

## Project Overview

This project focuses on predicting future weekly sales for Walmart stores using Machine Learning techniques. Accurate sales forecasting helps retail businesses optimise inventory management, workforce planning, budgeting, and strategic decision-making.

The project performs Exploratory Data Analysis (EDA), feature engineering, model training, evaluation, and future sales forecasting using the Random Forest Regressor algorithm.

---

## Business Problem

Retail organisations generate massive amounts of sales data every week. Predicting future sales accurately is essential for:

- Inventory optimisation
- Demand forecasting
- Supply chain management
- Resource allocation
- Revenue planning
- Seasonal trend analysis

This project aims to build a machine learning model capable of forecasting Walmart's weekly sales based on historical and economic indicators.

---

## Dataset Information

**Dataset:** Walmart Sales Dataset

The dataset contains weekly sales information along with several factors that influence sales performance.

### Features

| Feature | Description |
|----------|------------|
| Store | Store Identification Number |
| Date | Week of Sales |
| Weekly_Sales | Weekly Sales Revenue (Target Variable) |
| Holiday_Flag | Indicates Holiday Week (0 = No, 1 = Yes) |
| Temperature | Average Temperature |
| Fuel_Price | Fuel Cost in the Region |
| CPI | Consumer Price Index |
| Unemployment | Unemployment Rate |

### Target Variable

```python
Weekly_Sales
```

---

## Technologies Used

### Programming Language

- Python

### Libraries

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

### Machine Learning Algorithm

- Random Forest Regressor

### Development Environment

- Jupyter Notebook

---

## Exploratory Data Analysis (EDA)

The project includes detailed exploratory data analysis to understand sales behavior and trends.

### Analysis Performed

- Dataset inspection
- Missing value analysis
- Data type verification
- Weekly sales distribution analysis
- Store-wise sales comparison
- Time-series sales trend visualization
- Correlation analysis
- Feature relationship exploration

---

## Feature Engineering

To improve model performance, additional time-based features were extracted from the Date column.

### Generated Features

```python
Year
Month
Week
```

These features help the model capture seasonal and temporal sales patterns.

---

## Machine Learning Model

### Model Used

```python
Random Forest Regressor
```

Random Forest was selected because:

- Handles non-linear relationships effectively
- Reduces overfitting through ensemble learning
- Works well on structured/tabular datasets
- Provides strong predictive performance

---

## Project Workflow

```text
Data Collection
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Train-Test Split
        ↓
Random Forest Model Training
        ↓
Model Evaluation
        ↓
Future Sales Forecasting
        ↓
Visualization of Predictions
```

---

## Model Evaluation

The model performance was evaluated using:

### 1. Mean Absolute Error (MAE)

Measures the average prediction error.

```python
MAE = Actual Sales - Predicted Sales
```

### 2. R² Score

Measures how well the model explains variance in sales data.

```python
R² Score
```

A higher R² score indicates better predictive performance.

---

## Future Sales Forecasting

The trained model is used to forecast:

- Future weekly sales
- Store-specific sales trends
- Upcoming 12-week sales performance

The forecast results are visualized to compare historical and predicted sales trends.

---

## Project Structure

```text
Walmart-Sales-Forecasting/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── walmart_sales.csv
│
├── notebooks/
│   └── walmart_sales_forecasting.ipynb
│
└── outputs/
    ├── sales_distribution.png
    ├── sales_trend.png
    ├── forecast_results.png
    └── model_performance.png
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/Walmart-Sales-Forecasting.git
```

### Navigate to the Project Folder

```bash
cd Walmart-Sales-Forecasting
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Open Jupyter Notebook and run:

```bash
jupyter notebook
```

Then open:

```text
notebooks/walmart_sales_forecasting.ipynb
```

The notebook will:

1. Load the dataset
2. Perform EDA
3. Engineer new features
4. Train the Random Forest model
5. Evaluate performance
6. Generate future sales forecasts

---

## Key Insights

- Weekly sales vary significantly across stores.
- Economic indicators such as CPI and unemployment influence sales trends.
- Holiday weeks contribute to fluctuations in revenue.
- Time-based features improve forecasting accuracy.
- Random Forest effectively captures complex sales patterns.

---

## Future Improvements

- Hyperparameter tuning using GridSearchCV
- XGBoost implementation
- LightGBM implementation
- Seasonal decomposition analysis
- Deep Learning models (LSTM)
- Interactive dashboard using Streamlit
- Real-time forecasting pipeline

---

## Author

### Madhan Sai

Final Year B.Tech Student (CSE - Data Science)

Areas of Interest:

- Machine Learning
- Deep Learning
- Generative AI
- LLM Applications
- AI Agents

### GitHub

https://github.com/madhan-4413

---

## Contributions

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

---

## License

This project is intended for educational and learning purposes.

---

Made by Madhan Sai
