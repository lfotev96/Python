
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    inputData: str

# Примерни очаквани изходи за различни входни данни
expected_outputs = {
    "1\n": "2\n",
    "2\n": "3\n",
    "3\n": "4\n"
}

@app.post("/check_code")
async def check_code(request: CodeRequest):
    try:
        # Запазване на кода във временен файл
        with open('temp_code.py', 'w') as f:
            f.write(request.code)

        # Изпълнение на кода с подадените входни данни
        result = subprocess.run(
            ['python3', 'temp_code.py'],
            input=request.inputData.encode(),
            capture_output=True,
            text=True
        )

        # Вземане на резултата
        output = result.stdout

        # Проверка на резултата спрямо очакваните изходи
        correct = 0
        total = len(expected_outputs)
        for input_data, expected_output in expected_outputs.items():
            test_result = subprocess.run(
                ['python3', 'temp_code.py'],
                input=input_data.encode(),
                capture_output=True,
                text=True
            )
            if test_result.stdout == expected_output:
                correct += 1

        # Изчисляване на процента на вярност
        accuracy = (correct / total) * 100

        # Връщане на процента на вярност
        return {"result": f"{accuracy}% вярност"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Грешка при изпълнението на кода.")
