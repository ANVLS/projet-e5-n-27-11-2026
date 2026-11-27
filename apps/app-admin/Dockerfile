FROM python:3.11-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"
RUN adduser --disabled-password --gecos "" appuser
COPY --from=builder /opt/venv /opt/venv
COPY . .
RUN sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['*']/g" core/settings.py &&     python manage.py migrate &&     chown -R appuser:appuser /app && chmod -R u+rwX /app
USER appuser
EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
