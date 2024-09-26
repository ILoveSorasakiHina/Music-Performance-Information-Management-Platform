FROM python:3.11

# 設置工作目錄
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 設置環境變量
ENV PYTHONUNBUFFERED=1

# 執行Django伺服器
CMD ["gunicorn", "gov_data_search.wsgi:application", "--bind", "0.0.0.0:8000"]
