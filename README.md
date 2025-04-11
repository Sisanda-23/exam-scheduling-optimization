# Exam Scheduling with Spectral Graph Theory

📊 **Optimizing exam timetables using eigenvalue decomposition**

## 🚀 How It Works
1. Models exams as a **conflict graph**
2. Uses **Fiedler vector** (from graph Laplacian) to partition exams
3. Schedules exams while respecting constraints

## 📂 Files
- `original_implementation_exam_scheduler.py`: Initial implementation
- `docs_theory_background.md`: Math foundations

## 🔍 Insights  
- Achieved **zero hard conflicts** in sample data  
- Runtime: O(n³) (dominated by eigen-decomposition)
- 
## 🚀 Future Work  
- Scaling to 100+ exams (sparse matrices)  
- Incorporating room capacities  

## 💻 Run It
```bash
pip install -r original_implementation_requirements.txt
python original_implementation_exam_scheduler.py

