# 📚 Study-Time Optimizer

### An Intelligent Decision Support System using Linear Programming and XGBoost

A hybrid decision-support web application that helps students optimize their daily study-time allocation across multiple subjects.

The system combines:

- 📊 **Study Priority Index (SPI)** for subject prioritization
- 📐 **Linear Programming using PuLP** for optimal study-time allocation
- 🤖 **XGBoost** for experimental academic performance prediction
- 🌐 **Flask** for the web application
- 📈 **Interactive dashboard and charts** for result visualization

---

## 🚀 Project Overview

Students often struggle to decide how to distribute limited study time among multiple subjects.

A simple equal distribution of time may not be effective because subjects can differ in:

- Difficulty
- Importance
- Current performance level
- Minimum required study time
- Maximum practical study time

This project provides a data-driven approach to study planning.

The system calculates a **Study Priority Index (SPI)** for each subject, uses **Linear Programming** to determine an optimal allocation of available study hours, and then uses an **experimental XGBoost** model to predict academic performance outcomes.

---

## ✨ Key Features

### 📊 1. Study Priority Index (SPI)

Each subject receives a priority score based on:

- Subject Difficulty
- Subject Importance
- Current Student Performance

The system calculates:

```text
Performance Gap = 6 − Current Performance
Weighted Priority = (Performance Gap × Difficulty × Importance) / 10
```

**Higher SPI = Higher Priority for Study Time Allocation**

This ensures subjects where the student is struggling receive more study hours.

### 📐 2. Linear Programming Optimization

Using **PuLP** (Python Linear Programming library), the system solves:

**Objective:** Maximize total performance improvement

**Subject to:**
- Total available study hours constraint
- Minimum study time per subject (must-know concepts)
- Maximum study time per subject (diminishing returns)
- Non-negativity constraints

**Output:** Optimal study hours for each subject that maximizes learning efficiency

### 🤖 3. XGBoost Performance Prediction

An experimental machine learning model that predicts:

- Expected performance improvement per subject
- Overall academic performance after following the study plan
- Confidence scores for predictions

The model is trained on historical study data and performance outcomes.

### 🌐 4. Interactive Web Application

Built with **Flask**, featuring:

- **Subject Management** - Add/edit subjects with difficulty, importance, and current performance
- **Constraint Configuration** - Set total available study hours, min/max per subject
- **Optimization Results** - View optimal study-time allocation
- **Performance Dashboard** - Interactive charts showing:
  - Study-time distribution by subject
  - Performance gap vs. allocated time
  - Predicted performance improvements
  - XGBoost prediction confidence

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ |
| Web Framework | Flask |
| Optimization | PuLP (Linear Programming) |
| ML Prediction | XGBoost |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

---

## 📋 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/samarthdhage-20/study-time-optimizer.git
   cd study-time-optimizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

---

## 🎯 How to Use

1. **Add Subjects** - Enter subject name, difficulty (1-10), importance (1-10), and current performance (0-10)
2. **Set Available Study Hours** - Specify total hours available per day/week
3. **Configure Constraints** - Set minimum and maximum study hours per subject
4. **Run Optimization** - Click "Optimize" to generate the study plan
5. **View Results** - Analyze the recommended study-time allocation and performance predictions
6. **Export Plan** - Download your personalized study schedule

---

## 📊 Example Scenario

**Student Input:**
- Mathematics: Difficulty 8, Importance 9, Current Performance 4
- History: Difficulty 4, Importance 6, Current Performance 7
- Chemistry: Difficulty 7, Importance 8, Current Performance 5
- Total Available Hours: 12 hours/week

**System Output:**
- Mathematics: 4.5 hours (highest priority)
- Chemistry: 3.8 hours
- History: 3.7 hours

**Predicted Improvement:**
- Mathematics: +1.8 points
- Chemistry: +1.5 points
- History: +0.9 points

---

## 🧪 Algorithm Details

### Study Priority Index Formula

```
SPI = (Max_Performance - Current_Performance) × Difficulty × Importance / 10
```

### Linear Programming Model

```
Maximize: Σ (SPI_i × Hours_i) for all subjects i

Subject to:
  Σ Hours_i ≤ Total_Available_Hours
  Min_Hours_i ≤ Hours_i ≤ Max_Hours_i for all i
  Hours_i ≥ 0
```

### XGBoost Features

- Subject difficulty
- Subject importance
- Performance gap
- Allocated study hours
- Historical performance data
- Learning curve metrics

---

## 📁 Project Structure

```
study-time-optimizer/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── /backend
│   ├── spi_calculator.py  # Study Priority Index calculation
│   ├── optimizer.py       # Linear programming solver
│   ├── predictor.py       # XGBoost prediction model
│   └── utils.py           # Utility functions
├── /frontend
│   ├── /templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── results.html
│   └── /static
│       ├── /css
│       └── /js
└── /data
    ├── models/            # Trained XGBoost models
    └── historical/        # Historical study data
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Known Limitations

- XGBoost predictions are experimental and require historical data
- Linear programming assumes linear relationships between study time and performance
- Does not account for break time or fatigue factors
- Requires manual input updates for current performance

---

## 🚧 Future Enhancements

- [ ] Integration with academic calendars
- [ ] Automated performance data collection
- [ ] Mobile application
- [ ] Real-time collaboration for group study
- [ ] Advanced learning analytics
- [ ] Integration with learning management systems (LMS)
- [ ] Adaptive algorithms based on actual performance

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Samarth Dhage**

- GitHub: [@samarthdhage-20](https://github.com/samarthdhage-20)

---

## 🙏 Acknowledgments

- PuLP documentation for linear programming
- XGBoost library for machine learning
- Flask framework for web development
- The academic community for research on optimal learning

---

## 📞 Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Contact the project maintainers

---

**Happy Studying! 📚✨**
