# **Interpreter**

A light implementation

## **Getting Started**

### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/Interpreter.git
cd Interpreter
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Run the Interpreter**
You can use the following commands to run different stages of execution:

#### **Tokenize the Input**
```sh
python -m app.main tokenize input.txt
```

#### **Parse the Input**
```sh
python -m app.main parse input.txt
```

#### **Evaluate Expressions**
```sh
python -m app.main evaluate input.txt
```

#### **Run the Program**
```sh
python -m app.main run input.txt
```

## **Example Input**
A simple `input.txt` file:
```
var x = 5;
var y = 5;
print x + y;
```

## **Expected Output**
When running:
```sh
python -m app.main run input.txt
```
You should see:
```
10
```

